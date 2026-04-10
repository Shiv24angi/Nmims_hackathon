import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class MealRecommenderSystem:
    def __init__(self):
        self.pipeline = None
        
        # Categorical and numerical columns defined
        self.categorical_cols = [
            'Gender', 'Disease_Type', 'Severity', 'Dietary_Restrictions', 
            'Allergies', 'Preferred_Cuisine', 'Goal'
        ]
        
        self.numerical_cols = [
            'Age', 'Weight_kg', 'Height_cm', 'BMI', 'Physical_Activity_Level',
            'Daily_Caloric_Intake', 'Cholesterol', 'Blood_Pressure', 'Glucose',
            'Weekly_Exercise_Hours', 'Adherence_to_Diet_Plan', 
            'Dietary_Nutrient_Imbalance_Score', 'Budget'
        ]

    def _generate_synthetic_data(self, n_samples=1000):
        np.random.seed(42)
        
        data = {
            'Age': np.random.randint(18, 65, n_samples),
            'Gender': np.random.choice(['male', 'female'], n_samples),
            'Weight_kg': np.random.uniform(50, 120, n_samples),
            'Height_cm': np.random.uniform(150, 200, n_samples),
            'Disease_Type': np.random.choice(['None', 'Diabetes', 'Hypertension'], n_samples),
            'Severity': np.random.choice(['Low', 'Medium', 'High'], n_samples),
            'Physical_Activity_Level': np.random.choice([1.2, 1.375, 1.55, 1.725, 1.9], n_samples),
            'Daily_Caloric_Intake': np.random.uniform(1500, 3500, n_samples),
            'Cholesterol': np.random.uniform(150, 250, n_samples),
            'Blood_Pressure': np.random.uniform(90, 140, n_samples),
            'Glucose': np.random.uniform(70, 130, n_samples),
            'Dietary_Restrictions': np.random.choice(['None', 'Vegan', 'Vegetarian'], n_samples),
            'Allergies': np.random.choice(['None', 'Nuts', 'Dairy', 'Gluten'], n_samples),
            'Preferred_Cuisine': np.random.choice(['Indian', 'Italian', 'Mexican', 'Asian'], n_samples),
            'Weekly_Exercise_Hours': np.random.uniform(0, 14, n_samples),
            'Adherence_to_Diet_Plan': np.random.uniform(0.1, 1.0, n_samples),
            'Dietary_Nutrient_Imbalance_Score': np.random.uniform(0, 10, n_samples),
            'Budget': np.random.uniform(3000, 10000, n_samples),
            'Goal': np.random.choice(['fat_loss', 'muscle_gain', 'maintenance'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # 2. FEATURE ENGINEERING
        # Compute BMI if not present (we overwrite it to be accurate)
        df['BMI'] = df['Weight_kg'] / ((df['Height_cm'] / 100) ** 2)
        
        # 3. TARGET CREATION based on scientifically valid formulas
        targets = []
        for _, row in df.iterrows():
            # BMR using Mifflin-St Jeor Equation
            if row['Gender'] == 'male':
                bmr = (10 * row['Weight_kg']) + (6.25 * row['Height_cm']) - (5 * row['Age']) + 5
            else:
                bmr = (10 * row['Weight_kg']) + (6.25 * row['Height_cm']) - (5 * row['Age']) - 161
                
            # Adjust calories using activity level
            maintenance_calories = bmr * row['Physical_Activity_Level']
            
            # Apply Goal multiplier
            if row['Goal'] == 'fat_loss':
                calories_needed = maintenance_calories - 500
                protein_multiplier = 2.0
            elif row['Goal'] == 'muscle_gain':
                calories_needed = maintenance_calories + 500
                protein_multiplier = 2.2
            else: # maintenance
                calories_needed = maintenance_calories
                protein_multiplier = 1.6
                
            # Ensure minimum safe calories
            calories_needed = max(1200, calories_needed)
            
            # Protein based on goal (1.2–2.2 g/kg)
            protein_needed = row['Weight_kg'] * protein_multiplier
            
            # Fat = 20–30% calories (let's use 25%)
            fat_calories = calories_needed * 0.25
            fat_needed = fat_calories / 9  # 9 cals per gram of fat
            
            # Carbs = remaining calories
            protein_calories = protein_needed * 4 # 4 cals per gram of protein
            remaining_calories = max(0, calories_needed - fat_calories - protein_calories)
            carbs_needed = remaining_calories / 4 # 4 cals per gram of carbs
            
            targets.append({
                'Calories_needed': calories_needed,
                'Protein_needed': protein_needed,
                'Carbs_needed': carbs_needed,
                'Fat_needed': fat_needed
            })
            
        df_targets = pd.DataFrame(targets)
        return df, df_targets

    def train_model(self):
        print("Generating dataset and targets...")
        X, y = self._generate_synthetic_data(n_samples=2000)
        
        # Preprocessor: OneHotEncoding for categories, Normalization for numericals
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numerical_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.categorical_cols)
            ])
        
        # 4. MODEL: RandomForestRegressor for multi-output regression
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
        # Split dataset (80/20)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training RandomForestRegressor model...")
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f"Model trained successfully. Test RMSE: {rmse:.2f}")

    def load_model(self, filepath="diet_model.pkl"):
        import joblib
        import os
        if not os.path.exists(filepath):
            raise Exception(f"Model file '{filepath}' not found.")
        print(f"Loading trained model from {filepath}...")
        self.pipeline = joblib.load(filepath)
        print("Model loaded successfully.")

    def predict_targets(self, user_dict):
        if not self.pipeline:
            raise Exception("Model is not trained. Call train_model() first.")
            
        # Wrap into dataframe
        user_df = pd.DataFrame([user_dict])
        
        # Re-compute BMI if missing
        if 'BMI' not in user_df.columns or pd.isna(user_df['BMI'].iloc[0]):
            user_df['BMI'] = user_df['Weight_kg'] / ((user_df['Height_cm'] / 100) ** 2)
            
        # Predict
        preds = self.pipeline.predict(user_df)[0]
        return {
            'Calories_needed': preds[0],
            'Protein_needed': preds[1],
            'Carbs_needed': preds[2],
            'Fat_needed': preds[3]
        }

    # 6. MEAL GENERATION LOGIC
    def generate_meal_plan(self, predicted_targets, food_dataset):
        """
        Greedy approach to select Breakfast, Lunch, Dinner, Snacks
        """
        target_calories = predicted_targets['Calories_needed']
        target_protein = predicted_targets['Protein_needed']
        
        # Safe bounds
        min_cals = target_calories * 0.90
        max_cals = target_calories * 1.10
        
        # For a simple greedy approach, let's distribute target macros:
        # Breakfast: 25%, Lunch: 35%, Dinner: 30%, Snack: 10%
        meal_distributions = {
            'Breakfast': 0.25,
            'Lunch': 0.35,
            'Dinner': 0.30,
            'Snacks': 0.10
        }
        
        # Group foods by synthetic category or simple split if no category mechanism
        # For this logic, we just assume food_dataset has a 'category' or we assign them
        
        meal_plan = {
            'Breakfast': [],
            'Lunch': [],
            'Dinner': [],
            'Snacks': [],
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fat': 0,
            'total_price': 0
        }

        # Filter valid items
        valid_foods = [f for f in food_dataset if f.get('Calories', 0) > 0]
        if not valid_foods:
            return meal_plan

        import random

        # Greedy selection to get close to targets per meal
        for meal_name, pct in meal_distributions.items():
            meal_cals_target = target_calories * pct
            meal_protein_target = target_protein * pct
            
            # Simple stochastic greedy search
            best_item = None
            best_score = float('inf')
            
            for _ in range(50): # try 50 random items
                item = random.choice(valid_foods)
                # Score = penalty for deviating from target (more weight to calories)
                cal_diff = abs(item['Calories'] - meal_cals_target)
                prot_diff = abs(item['Protein'] - meal_protein_target) * 4 # 4 cals per g
                
                score = cal_diff + prot_diff
                if score < best_score:
                    best_score = score
                    best_item = item
            
            if best_item:
                meal_plan[meal_name].append(best_item)
                meal_plan['total_calories'] += best_item['Calories']
                meal_plan['total_protein'] += best_item['Protein']
                meal_plan['total_carbs'] += best_item['Carbs']
                meal_plan['total_fat'] += best_item['Fat']
                meal_plan['total_price'] += best_item.get('Price', 0)

        # 7. OUTPUT -> Dict returned to API
        return meal_plan

# 8. BONUS: get_meal_plan function
def get_meal_plan(user_input_dict, food_data):
    system = MealRecommenderSystem()
    try:
        system.load_model('diet_model.pkl')
    except Exception as e:
        print(f"Model load failed: {e}. Training dynamically instead.")
        system.train_model()
    
    # Fill in missing mock fields for the user if they're coming from a lightweight frontend profile
    defaults = {
        'Disease_Type': 'None',
        'Severity': 'Low',
        'Physical_Activity_Level': 1.375,
        'Daily_Caloric_Intake': 2000,
        'Cholesterol': 180,
        'Blood_Pressure': 120,
        'Glucose': 90,
        'Dietary_Restrictions': 'None',
        'Allergies': 'None',
        'Preferred_Cuisine': 'Indian',
        'Weekly_Exercise_Hours': 3,
        'Adherence_to_Diet_Plan': 0.8,
        'Dietary_Nutrient_Imbalance_Score': 2.0,
        'Budget': 5000,
        'Goal': 'maintenance'
    }
    
    for k, v in defaults.items():
        if k not in user_input_dict:
            user_input_dict[k] = v
            
    # Predict
    targets = system.predict_targets(user_input_dict)
    
    # Generate Meal Plan
    plan = system.generate_meal_plan(targets, food_data)
    
    return {
        'targets': targets,
        'meal_plan': plan
    }

if __name__ == "__main__":
    # Test Run
    sample_user = {
        'Age': 25,
        'Gender': 'male',
        'Weight_kg': 75,
        'Height_cm': 180,
        'Physical_Activity_Level': 1.55,
        'Goal': 'muscle_gain'
    }
    
    sample_foods = [
        {'Food_Name': 'Eggs & Toast', 'Calories': 350, 'Protein': 20, 'Carbs': 30, 'Fat': 15, 'Price': 50},
        {'Food_Name': 'Chicken Salad', 'Calories': 500, 'Protein': 40, 'Carbs': 20, 'Fat': 25, 'Price': 150},
        {'Food_Name': 'Pasta', 'Calories': 600, 'Protein': 15, 'Carbs': 80, 'Fat': 10, 'Price': 120},
        {'Food_Name': 'Protein Shake', 'Calories': 200, 'Protein': 25, 'Carbs': 10, 'Fat': 5, 'Price': 80}
    ]
    
    result = get_meal_plan(sample_user, sample_foods)
    import json
    print(json.dumps(result, indent=2))
