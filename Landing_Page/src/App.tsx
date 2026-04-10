import SmoothScrollHero from "@/components/ui/smooth-scroll-hero";

// The user prompt specifically says: "3. Use lucide-react icons for svgs or logos if component requires them"
import { Sparkles, Activity, QrCode as LucideQrCode, Leaf as LucideLeaf, Droplet, UserCircle2, BrainCircuit, Pointer, CreditCard as LucideCreditCard, TrendingUp, GraduationCap, Building2, CheckCircle2, LogIn } from "lucide-react";

function App() {
  return (
    <div className="bg-[#111] min-h-screen text-slate-100 font-sans">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 flex items-center justify-between px-8 py-4 backdrop-blur-md bg-black/30 border-b border-green-500/20">
        <div className="flex items-center gap-2 text-green-400 font-bold text-xl">
          <LucideLeaf className="fill-green-400" />
          <span>NutriSense</span>
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium">
          <a href="#about" className="hover:text-green-400 transition-colors">About</a>
          <a href="#features" className="hover:text-green-400 transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-green-400 transition-colors">How It Works</a>
        </div>
        <div className="flex gap-4">
          <a href="/login" className="px-5 py-2 text-sm font-medium hover:text-green-400 transition-colors">Login</a>
          <a href="/signup" className="px-5 py-2 text-sm bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors font-medium">Sign Up</a>
        </div>
      </nav>

      {/* 1. Hero Section using SmoothScrollHero */}
      <SmoothScrollHero
        scrollHeight={1500}
        desktopImage="https://images.unsplash.com/photo-1543353071-873f17a7a088?q=80&w=2670&auto=format&fit=crop"
        mobileImage="https://images.unsplash.com/photo-1543353071-873f17a7a088?q=80&w=1000&auto=format&fit=crop"
        initialClipPercentage={25}
        finalClipPercentage={75}
      />

      {/* 2. About / Overview Section */}
      <section className="py-24 px-6" id="about">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">Welcome to NutriSense</h2>
          <p className="text-lg text-gray-400 leading-relaxed">
            We use data-driven AI to suggest meals that align with your body metrics and daily schedule. This isn't just a food menu—it's a personalized health system directly integrated into your campus cafeteria.
          </p>
        </div>
      </section>

      {/* 3. Features Section */}
      <section className="py-24 px-6 bg-[#0a0a0a]" id="features">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">What You Get Inside</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Sparkles className="w-8 h-8 text-green-400 mb-4" />}
              title="AI Food Recommendations"
              desc="Tailored meals depending on your biometrics and goals."
            />
            <FeatureCard
              icon={<Activity className="w-8 h-8 text-pink-400 mb-4" />}
              title="Health & Calorie Tracking"
              desc="Automated logging every time you grab a meal."
            />
            <FeatureCard
              icon={<LucideQrCode className="w-8 h-8 text-purple-400 mb-4" />}
              title="Smart Payments"
              desc="Frictionless checkout using integrated QR codes."
            />
            <FeatureCard
              icon={<LucideLeaf className="w-8 h-8 text-green-500 mb-4" />}
              title="Food Waste Reduction"
              desc="Optimized portion suggestions to help the environment."
            />
            <FeatureCard
              icon={<Droplet className="w-8 h-8 text-blue-400 mb-4" />}
              title="Cycle-Aware Suggestions"
              desc="Contextual macro adjustments based on hormonal phases."
            />
          </div>
        </div>
      </section>

      {/* 4. How It Works Section */}
      <section className="py-24 px-6" id="how-it-works">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">The Experience</h2>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <FlowStep icon={<UserCircle2 />} title="Login" step={1} />
            <div className="w-1 h-8 md:w-8 md:h-1 bg-green-500/20" />
            <FlowStep icon={<BrainCircuit />} title="AI Suggestions" step={2} />
            <div className="w-1 h-8 md:w-8 md:h-1 bg-green-500/20" />
            <FlowStep icon={<Pointer />} title="Select Food" step={3} />
            <div className="w-1 h-8 md:w-8 md:h-1 bg-green-500/20" />
            <FlowStep icon={<LucideCreditCard />} title="Pay" step={4} />
            <div className="w-1 h-8 md:w-8 md:h-1 bg-green-500/20" />
            <FlowStep icon={<TrendingUp />} title="Track Health" step={5} />
          </div>
        </div>
      </section>

      {/* 5. Impact Section */}
      <section className="py-24 px-6 bg-[#0a0a0a]" id="impact">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">The Impact</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="p-8 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center">
              <GraduationCap className="w-12 h-12 text-green-400 mb-6" />
              <h3 className="text-2xl font-semibold mb-6">For Students</h3>
              <ul className="space-y-4 w-full">
                <ImpactItem text="Healthier eating habits" />
                <ImpactItem text="Better mental focus through customized macros" />
                <ImpactItem text="Transparent calorie tracking" />
              </ul>
            </div>
            <div className="p-8 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center">
              <Building2 className="w-12 h-12 text-blue-400 mb-6" />
              <h3 className="text-2xl font-semibold mb-6">For Cafeteria Admin</h3>
              <ul className="space-y-4 w-full">
                <ImpactItem text="Radically reduced food waste" />
                <ImpactItem text="Predictive inventory planning" />
                <ImpactItem text="Real-time popularity analytics" />
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/*  Final CTA Section */}
      <section className="py-32 px-6">
        <div className="max-w-4xl mx-auto text-center p-12 rounded-3xl bg-gradient-to-br from-green-500/20 to-blue-500/20 border border-green-500/30">
          <h2 className="text-4xl font-bold mb-4">Start Your Smart Eating Journey</h2>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">Access your personalized health dashboard and make every meal count.</p>
          <div className="flex gap-4 justify-center">
            <button className="px-8 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-all shadow-lg flex items-center gap-2">
              <LogIn className="w-5 h-5" /> Login Here
            </button>
            <button className="px-8 py-3 bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded-lg font-medium transition-all shadow-lg">
              Sign Up Now
            </button>
          </div>
        </div>
      </section>

      <footer className="text-center py-8 text-gray-500 text-sm border-t border-white/10">
        <p>&copy; 2026 NutriSense. Preview Landing Page.</p>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:-translate-y-1 transition-all duration-300 cursor-pointer">
      {icon}
      <h3 className="text-xl font-semibold mb-2 text-gray-100">{title}</h3>
      <p className="text-sm text-gray-400">{desc}</p>
    </div>
  )
}

function FlowStep({ icon, title, step }: { icon: React.ReactNode, title: string, step: number }) {
  return (
    <div className="flex flex-col items-center gap-4 group">
      <div className="w-16 h-16 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-300 group-hover:scale-110 group-hover:bg-green-500/20 group-hover:text-green-400 transition-all shadow-xl">
        <div className="[&>svg]:w-6 [&>svg]:h-6">
          {icon}
        </div>
      </div>
      <div className="text-center">
        <div className="text-xs text-green-400 font-medium mb-1">STEP {step}</div>
        <h4 className="font-semibold text-gray-200">{title}</h4>
      </div>
    </div>
  )
}

function ImpactItem({ text }: { text: string }) {
  return (
    <li className="flex items-center gap-3 text-gray-300 bg-black/40 p-3 rounded-lg border border-white/5">
      <CheckCircle2 className="w-5 h-5 text-green-400 shrink-0" />
      <span>{text}</span>
    </li>
  )
}

export default App;
