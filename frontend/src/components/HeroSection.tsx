import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { ArrowRight, Sparkles } from "lucide-react";
import heroImage from "@/assets/hero-soft-robotics.png";

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Hero background image */}
      <div className="absolute inset-0 z-0">
        <img
          src={heroImage}
          alt="Soft robotics visualization"
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/60 to-background" />
      </div>
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-primary/10 blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-primary/5 blur-3xl animate-float" style={{ animationDelay: "-3s" }} />
        <div className="absolute top-1/2 right-1/3 w-48 h-48 rounded-full bg-primary/8 blur-2xl animate-bounce-slow" />
        <div className="absolute top-1/3 right-1/4 w-32 h-32 rounded-full bg-primary/15 blur-2xl animate-drift" style={{ animationDelay: "-2s" }} />
        <div className="absolute bottom-1/3 left-1/3 w-24 h-24 rounded-full bg-primary/12 blur-xl animate-drift" style={{ animationDelay: "-5s" }} />
        
        {/* Floating particles */}
        <div className="absolute top-20 left-1/5 w-2 h-2 rounded-full bg-primary/40 animate-float" style={{ animationDelay: "-1s" }} />
        <div className="absolute top-1/3 right-1/5 w-3 h-3 rounded-full bg-primary/30 animate-float" style={{ animationDelay: "-4s" }} />
        <div className="absolute bottom-1/4 left-1/4 w-2 h-2 rounded-full bg-primary/50 animate-bounce-slow" style={{ animationDelay: "-2s" }} />
        <div className="absolute top-2/3 right-1/3 w-1.5 h-1.5 rounded-full bg-primary/60 animate-drift" style={{ animationDelay: "-3s" }} />
        <div className="absolute bottom-1/3 right-1/4 w-2.5 h-2.5 rounded-full bg-primary/35 animate-float" style={{ animationDelay: "-6s" }} />
        
        {/* Spinning ring */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-primary/5 rounded-full animate-spin-slow" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] border border-primary/3 rounded-full animate-spin-slow" style={{ animationDirection: "reverse", animationDuration: "30s" }} />
      </div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border mb-8">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm text-muted-foreground">Agentic AI for Soft Object Modeling</span>
          </div>

          <h1 className="font-display text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="text-gradient">Agentic AI</span> for{" "}
            Soft Object Modeling
          </h1>

          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
            Transform your ideas into 3D soft object visualizations instantly.
            Our autonomous AI agent interprets your natural language and brings complex models to life.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/workshop">
              <Button variant="hero" size="xl" className="group">
                Start Creating
                <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link to="/docs">
              <Button variant="hero-outline" size="xl">
                Learn More
              </Button>
            </Link>
          </div>

          {/* Feature highlights */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "Natural Language", desc: "Just describe your design in plain English" },
              { title: "Agentic AI", desc: "Autonomous agents reason and iterate on your model" },
              { title: "3D Visualization", desc: "See soft objects come to life with matplotlib animations" },
            ].map((feature, i) => (
              <div
                key={i}
                className="card-gradient rounded-2xl p-6 border border-border hover:border-primary/30 transition-all duration-300 hover:-translate-y-2 hover:shadow-lg hover:shadow-primary/10 animate-fade-in-up group"
                style={{ animationDelay: `${i * 150}ms` }}
              >
                <h3 className="font-display font-semibold text-lg mb-2 group-hover:text-primary transition-colors duration-300">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
