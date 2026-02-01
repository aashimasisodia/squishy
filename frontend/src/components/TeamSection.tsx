import { Linkedin } from "lucide-react";

const TeamSection = () => {
  const team = [
    {
      name: "Advayth Pashupati",
      role: "Co-Founder",
      bio: "Building autonomous AI systems that understand and model complex soft materials.",
      avatar: "AP",
      linkedin: "https://www.linkedin.com/in/advayth-pashupati/",
    },
    {
      name: "Neev Patel",
      role: "Co-Founder",
      bio: "Focused on creating intuitive interfaces for AI-powered design tools.",
      avatar: "NP",
      linkedin: "https://www.linkedin.com/in/neev-patel280/",
    },
    {
      name: "Aashima Sisodia",
      role: "Co-Founder",
      bio: "Passionate about leveraging agentic AI to revolutionize soft object modeling.",
      avatar: "AS",
      linkedin: "https://www.linkedin.com/in/aashimasisodia/",
    },
    {
      name: "Kavya Uppal",
      role: "Co-Founder",
      bio: "Driving innovation at the intersection of AI agents and 3D visualization.",
      avatar: "KU",
      linkedin: "https://www.linkedin.com/in/kavya-uppal/",
    },
  ];

  return (
    <section className="py-24 bg-card/30">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            Meet the <span className="text-gradient">Team</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            A passionate team of founders united by the vision of democratizing
            soft object modeling through agentic AI.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {team.map((member, i) => (
            <div
              key={i}
              className="group text-center"
            >
              <div className="relative mb-6 mx-auto">
                <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-squishy-blue to-squishy-blue-light flex items-center justify-center text-3xl font-display font-bold text-white shadow-lg group-hover:scale-105 transition-transform duration-300">
                  {member.avatar}
                </div>
                <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <a 
                    href={member.linkedin} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="w-8 h-8 rounded-full bg-card border border-border flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-colors"
                  >
                    <Linkedin className="w-4 h-4" />
                  </a>
                </div>
              </div>
              <h3 className="font-display text-lg font-semibold mb-1">{member.name}</h3>
              <p className="text-primary text-sm font-medium mb-3">{member.role}</p>
              <p className="text-sm text-muted-foreground leading-relaxed">{member.bio}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TeamSection;
