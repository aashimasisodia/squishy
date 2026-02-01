import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { ArrowRight, MessageSquare, Brain, Code, FileCode, Eye } from "lucide-react";

const Documentation = () => {
  const pipelineSteps = [
    {
      icon: MessageSquare,
      title: "Natural Language Input",
      description: "Users describe their soft object in plain English. Our agentic AI parses intent, extracts geometric parameters, and understands material properties from conversational input.",
      color: "from-blue-500 to-blue-600",
    },
    {
      icon: Brain,
      title: "Cosserat Rod Theory",
      description: "The AI agent translates your description into Cosserat rod representations—a mathematical framework that models slender, deformable structures with bending, twisting, and stretching capabilities.",
      color: "from-purple-500 to-purple-600",
    },
    {
      icon: Code,
      title: "PyElastica Integration",
      description: "We leverage PyElastica, an open-source simulation platform for Cosserat rod dynamics. The agent generates simulation parameters and boundary conditions automatically.",
      color: "from-primary to-squishy-orange-glow",
    },
    {
      icon: FileCode,
      title: "Python Script Generation",
      description: "The agentic AI writes custom Python scripts that define your soft object, run the simulation, and export results to DAT/STL file formats for 3D visualization and fabrication.",
      color: "from-green-500 to-green-600",
    },
    {
      icon: Eye,
      title: "Web Rendering",
      description: "Matplotlib generates animated GIFs showing deformation and movement. These visualizations are rendered directly in your browser for immediate feedback and iteration.",
      color: "from-pink-500 to-pink-600",
    },
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <main className="flex-1 pt-24 pb-12">
        <div className="container mx-auto px-6">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="font-display text-4xl md:text-5xl font-bold mb-4">
              How <span className="text-gradient">Squishy</span> Works
            </h1>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Our agentic AI pipeline transforms natural language into physics-accurate
              soft object simulations using cutting-edge computational mechanics.
            </p>
          </div>

          {/* Visual Flowchart */}
          <div className="max-w-5xl mx-auto mb-20">
            <div className="card-gradient rounded-2xl border border-border p-8 md:p-12">
              <h2 className="font-display text-2xl font-bold text-center mb-8">
                The Squishy Pipeline
              </h2>
              
              {/* Flowchart */}
              <div className="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-2">
                {pipelineSteps.map((step, i) => (
                  <div key={i} className="flex items-center gap-2 md:gap-4">
                    <div className="flex flex-col items-center text-center">
                      <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-lg mb-3`}>
                        <step.icon className="w-8 h-8 text-white" />
                      </div>
                      <span className="text-xs font-medium max-w-[100px] leading-tight">{step.title}</span>
                    </div>
                    {i < pipelineSteps.length - 1 && (
                      <ArrowRight className="w-6 h-6 text-muted-foreground hidden md:block" />
                    )}
                  </div>
                ))}
              </div>

              {/* Mobile arrows */}
              <div className="md:hidden flex flex-col items-center gap-2 my-4">
                {pipelineSteps.slice(0, -1).map((_, i) => (
                  <ArrowRight key={i} className="w-6 h-6 text-muted-foreground rotate-90" />
                ))}
              </div>
            </div>
          </div>

          {/* Detailed Steps */}
          <div className="max-w-4xl mx-auto space-y-8 mb-20">
            <h2 className="font-display text-3xl font-bold text-center mb-12">
              Deep Dive: Each Stage Explained
            </h2>
            
            {pipelineSteps.map((step, i) => (
              <div
                key={i}
                className="card-gradient rounded-2xl border border-border p-8 hover:border-primary/30 transition-all duration-300"
              >
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0">
                    <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-lg`}>
                      <step.icon className="w-7 h-7 text-white" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-sm font-mono text-primary">Step {i + 1}</span>
                      <h3 className="font-display text-xl font-semibold">{step.title}</h3>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Technical Details Grid */}
          <div className="max-w-5xl mx-auto mb-20">
            <h2 className="font-display text-3xl font-bold text-center mb-12">
              Core Technologies
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Cosserat Rod Theory Card */}
              <div className="card-gradient rounded-2xl border border-border p-8">
                <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-6">
                  <span className="text-2xl">📐</span>
                </div>
                <h3 className="font-display text-xl font-semibold mb-4">Cosserat Rod Theory</h3>
                <p className="text-muted-foreground mb-4 leading-relaxed">
                  A continuum mechanics framework for modeling slender, flexible structures. 
                  Unlike simple beam theory, Cosserat rods capture:
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Bending in multiple planes
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Torsion and twisting
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Shear deformation
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Large geometric nonlinearities
                  </li>
                </ul>
              </div>

              {/* PyElastica Card */}
              <div className="card-gradient rounded-2xl border border-border p-8">
                <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center mb-6">
                  <span className="text-2xl">🐍</span>
                </div>
                <h3 className="font-display text-xl font-semibold mb-4">PyElastica Platform</h3>
                <p className="text-muted-foreground mb-4 leading-relaxed">
                  An open-source Python library for simulating assemblies of soft, slender structures. 
                  Key capabilities include:
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Real-time physics simulation
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Contact and collision handling
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Muscle activation models
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Fluid-structure interaction
                  </li>
                </ul>
              </div>

              {/* Agentic AI Card */}
              <div className="card-gradient rounded-2xl border border-border p-8">
                <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mb-6">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="font-display text-xl font-semibold mb-4">Agentic AI</h3>
                <p className="text-muted-foreground mb-4 leading-relaxed">
                  Our autonomous AI agents don't just respond—they reason, plan, and iterate. 
                  The agent workflow includes:
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Intent parsing from natural language
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Multi-step reasoning chains
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Self-correction and validation
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    Code generation and execution
                  </li>
                </ul>
              </div>

              {/* Output Formats Card */}
              <div className="card-gradient rounded-2xl border border-border p-8">
                <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center mb-6">
                  <span className="text-2xl">📁</span>
                </div>
                <h3 className="font-display text-xl font-semibold mb-4">Output Formats</h3>
                <p className="text-muted-foreground mb-4 leading-relaxed">
                  Squishy generates multiple output formats for visualization and manufacturing:
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <strong>GIF:</strong> Animated matplotlib visualizations
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <strong>DAT:</strong> Simulation data files
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <strong>STL:</strong> 3D printable mesh files
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <strong>Python:</strong> Reproducible scripts
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Architecture Diagram */}
          <div className="max-w-4xl mx-auto">
            <div className="card-gradient rounded-2xl border border-border p-8 md:p-12">
              <h2 className="font-display text-2xl font-bold text-center mb-8">
                System Architecture
              </h2>
              
              <div className="bg-background/50 rounded-xl p-6 border border-border">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Frontend Layer */}
                  <div className="space-y-4">
                    <div className="text-center p-4 rounded-xl bg-blue-500/10 border border-blue-500/30">
                      <h4 className="font-display font-semibold text-blue-400 mb-2">Frontend</h4>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="p-2 bg-background rounded-lg">React UI</div>
                        <div className="p-2 bg-background rounded-lg">Natural Language Input</div>
                        <div className="p-2 bg-background rounded-lg">GIF Renderer</div>
                      </div>
                    </div>
                  </div>

                  {/* AI Layer */}
                  <div className="space-y-4">
                    <div className="text-center p-4 rounded-xl bg-primary/10 border border-primary/30">
                      <h4 className="font-display font-semibold text-primary mb-2">AI Agent</h4>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="p-2 bg-background rounded-lg">Intent Parser</div>
                        <div className="p-2 bg-background rounded-lg">Code Generator</div>
                        <div className="p-2 bg-background rounded-lg">Validation Loop</div>
                      </div>
                    </div>
                  </div>

                  {/* Simulation Layer */}
                  <div className="space-y-4">
                    <div className="text-center p-4 rounded-xl bg-green-500/10 border border-green-500/30">
                      <h4 className="font-display font-semibold text-green-400 mb-2">Simulation</h4>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="p-2 bg-background rounded-lg">PyElastica Engine</div>
                        <div className="p-2 bg-background rounded-lg">Cosserat Solver</div>
                        <div className="p-2 bg-background rounded-lg">File Export</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Flow arrows */}
                <div className="hidden md:flex justify-center items-center gap-4 mt-6 text-muted-foreground">
                  <span className="text-sm">User Input</span>
                  <ArrowRight className="w-4 h-4" />
                  <span className="text-sm">AI Processing</span>
                  <ArrowRight className="w-4 h-4" />
                  <span className="text-sm">Simulation</span>
                  <ArrowRight className="w-4 h-4" />
                  <span className="text-sm">Visualization</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Documentation;
