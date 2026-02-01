import { Cpu, Lightbulb, Zap, Layers } from "lucide-react";

const AboutSection = () => {
  const features = [
    {
      icon: Lightbulb,
      title: "Intuitive Design",
      description: "Describe your soft object concept in natural language. No CAD experience required.",
    },
    {
      icon: Cpu,
      title: "Agentic AI",
      description: "Autonomous AI agents reason, plan, and iterate to generate accurate 3D soft object models.",
    },
    {
      icon: Zap,
      title: "Real-Time Visualization",
      description: "Watch your designs come to life with animated matplotlib GIFs showing deformation and movement.",
    },
    {
      icon: Layers,
      title: "Autonomous Iteration",
      description: "Our agents refine models through multi-step reasoning. Each iteration takes seconds, not hours.",
    },
  ];

  return (
    <section className="py-24 relative">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            The Future of{" "}
            <span className="text-gradient">Soft Object Modeling</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Squishy uses agentic AI to bridge the gap between imagination and engineering,
            making soft object modeling accessible to everyone.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {features.map((feature, i) => (
            <div
              key={i}
              className="group card-gradient rounded-2xl p-8 border border-border hover:border-primary/40 transition-all duration-500 hover:-translate-y-2 hover:shadow-lg hover:shadow-primary/10 animate-fade-in-up"
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 group-hover:bg-primary/30 transition-all duration-300 group-hover:animate-pulse-glow">
                <feature.icon className="w-7 h-7 text-primary group-hover:animate-wiggle" />
              </div>
              <h3 className="font-display text-xl font-semibold mb-3 group-hover:text-primary transition-colors duration-300">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
