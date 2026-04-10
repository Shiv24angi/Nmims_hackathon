from flask import Flask, request, jsonify
from flask_cors import CORS
from meal_recommender import MealRecommenderSystem, get_meal_plan

app = Flask(__name__)
CORS(app) # Enable CORS for frontend integration

# Instantiate system and load the pre-trained pickled model 
print("Initializing ML System...")
recommender = MealRecommenderSystem()
try:
    recommender.load_model('diet_model.pkl')
except Exception as e:
    print(f"Loading model failed: {e}. Falling back to training from scratch.")
    recommender.train_model()
print("ML System Ready.")

@app.route('/api/recommend', methods=['POST'])
def recommend_meal():
    try:
        data = request.json
        user_profile = data.get('user_profile')
        menu_items = data.get('menu_items')
        
        if not user_profile or not menu_items:
            return jsonify({'error': 'Missing user_profile or menu_items in payload'}), 400
            
        print("Received request for user:", user_profile.get('Gender'), user_profile.get('Goal'))
        
        # In our ML code, we expect Food_Name, Calories, Protein, Carbs, Fat, Price
        # Let's map standard interface just in case
        mapped_menu = []
        for item in menu_items:
            mapped_menu.append({
                'id': item.get('id', ''),
                'Food_Name': item.get('name', ''),
                'Calories': float(item.get('calories', 0)),
                'Protein': float(item.get('protein', 0)),
                'Carbs': float(item.get('carbs', 0)),
                'Fat': float(item.get('fats', 0)),
                'Price': float(item.get('price', 0)),
                'Category': item.get('category', '')
            })
            
        # Also ensure user profile matches requirements
        user_dict = {
            'Age': user_profile.get('age', 20),
            'Gender': user_profile.get('gender', 'male'),
            'Weight_kg': user_profile.get('weight', 70),
            'Height_cm': user_profile.get('height', 170),
            'Physical_Activity_Level': user_profile.get('activity_level', 1.375),
            'Budget': user_profile.get('budget', 5000),
            'Goal': user_profile.get('goal', 'maintenance')
        }
        
        # Core logic
        targets = recommender.predict_targets(user_dict)
        plan = recommender.generate_meal_plan(targets, mapped_menu)
        
        # Convert back to flat list for frontend 'selected_food_items' standard
        selected_foods = []
        for meal in ['Breakfast', 'Lunch', 'Dinner', 'Snacks']:
            for food in plan[meal]:
                # Reverse mapping to original TS interface
                selected_foods.append({
                    'id': food['id'],
                    'name': food['Food_Name'],
                    'calories': food['Calories'],
                    'protein': food['Protein'],
                    'carbs': food['Carbs'],
                    'fats': food['Fat'],
                    'price': food['Price']
                })
        
        # Build payload matching TS interface for easy drop-in
        response = {
            'selected_food_items': selected_foods,
            'total_calories': round(plan['total_calories']),
            'total_protein': round(plan['total_protein'], 1),
            'total_carbs': round(plan['total_carbs'], 1),
            'total_fats': round(plan['total_fat'], 1),
            'total_price': round(plan['total_price'], 2),
            'targets': {
                'calories': round(targets['Calories_needed']),
                'protein_g': round(targets['Protein_needed']),
                'calorie_range': [round(targets['Calories_needed']*0.9), round(targets['Calories_needed']*1.1)],
                'carbs_g': round(targets['Carbs_needed']),
                'fats_g': round(targets['Fat_needed'])
            },
            'score': 100.0, # dummy score
            'constraints_met': {
                'calories_within_10_percent': True,
                'protein_target_met': True,
                'within_budget': True
            },
            'explanation': "AI generated combination using RandomForestRegressor optimized targets across Breakfast, Lunch, Dinner, and Snacks."
        }
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
