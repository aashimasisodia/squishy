import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Send, Loader2, Sparkles, RotateCcw } from "lucide-react";
import PythonEditor from "@/components/workshop/PythonEditor";

const Workshop = () => {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedGif, setGeneratedGif] = useState<string | null>(null);
  const [generatedCode, setGeneratedCode] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setGeneratedGif(null);
    setGeneratedCode(null);

    try {
      // 1. Send generation request
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error("Failed to start generation");
      }

      const data = await response.json();
      const id = data.id;
      console.log("Generation started with ID:", id);

      // 2. Poll for status
      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await fetch(`http://localhost:8000/status/${id}`);
          const statusData = await statusRes.json();

          if (statusData.status === "completed") {
            clearInterval(pollInterval);

            // 3. Fetch results
            const gifUrl = `http://localhost:8000/gif/${id}?t=${Date.now()}`;

            // Preload the image to prevent race conditions or 404s
            const preloadImage = (url: string) => {
              return new Promise<void>((resolve, reject) => {
                const img = new Image();
                img.onload = () => resolve();
                img.onerror = () => reject();
                img.src = url;
              });
            };

            // Try to load the image, retrying a few times if necessary
            let retries = 5;
            while (retries > 0) {
              try {
                await preloadImage(gifUrl);
                break;
              } catch (e) {
                retries--;
                if (retries === 0) console.error("Failed to preload generated GIF");
                await new Promise(r => setTimeout(r, 500));
              }
            }

            setGeneratedGif(gifUrl);

            const codeRes = await fetch(`/api/code/${id}`);
            const codeText = await codeRes.text();
            setGeneratedCode(codeText);

            setIsGenerating(false);
          } else if (statusData.status === "failed") {
            clearInterval(pollInterval);
            setIsGenerating(false);
            console.error("Generation failed:", statusData.error);
            // Ideally show error toast here
          }
        } catch (err) {
          console.error("Polling error:", err);
          clearInterval(pollInterval);
          setIsGenerating(false);
        }
      }, 2000);

    } catch (error) {
      console.error("Error:", error);
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setPrompt("");
    setGeneratedGif(null);
    setGeneratedCode(null);
  };

  const examplePrompts = [
    "A long flexible rod that moves forward using an internal traveling sinusoidal with noticeable bending wave along its body (snake-like locomotion). Make sure it has high amplitude low frequency relative to its length",
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <main className="flex-1 pt-24 pb-12">
        <div className="container mx-auto px-6">
          <div className="max-w-7xl mx-auto">
            {/* Header */}
            <div className="text-center mb-12">
              <h1 className="font-display text-4xl md:text-5xl font-bold mb-4">
                <span className="text-gradient">Workshop</span>
              </h1>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Describe your soft object in natural language and let our agentic AI bring it to life.
              </p>
            </div>

            <Tabs defaultValue="design" className="space-y-6">
              <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 bg-card border border-border">
                <TabsTrigger value="design" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                  Design Studio
                </TabsTrigger>
                <TabsTrigger value="code" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                  Python Script
                </TabsTrigger>
              </TabsList>

              {/* Design Studio Tab */}
              <TabsContent value="design" className="mt-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Input Panel */}
                  <div className="card-gradient rounded-2xl border border-border p-6 space-y-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl orange-gradient flex items-center justify-center">
                        <Sparkles className="w-5 h-5 text-primary-foreground" />
                      </div>
                      <div>
                        <h2 className="font-display font-semibold">Design Input</h2>
                        <p className="text-sm text-muted-foreground">Describe your soft object</p>
                      </div>
                    </div>

                    <Textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Describe the soft object you want to model..."
                      className="min-h-[200px] bg-background/50 border-border focus:border-primary resize-none"
                    />

                    {/* Example prompts */}
                    <div className="space-y-2">
                      <p className="text-xs text-muted-foreground uppercase tracking-wide">Try an example:</p>
                      <div className="flex flex-wrap gap-2">
                        {examplePrompts.map((example, i) => (
                          <button
                            key={i}
                            onClick={() => setPrompt(example)}
                            className="text-xs px-3 py-1.5 rounded-full bg-secondary text-secondary-foreground hover:bg-primary hover:text-primary-foreground transition-colors"
                          >
                            Example {i + 1}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="flex gap-3">
                      <Button
                        variant="hero"
                        size="lg"
                        className="flex-1"
                        onClick={handleGenerate}
                        disabled={isGenerating || !prompt.trim()}
                      >
                        {isGenerating ? (
                          <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Generating...
                          </>
                        ) : (
                          <>
                            <Send className="w-5 h-5" />
                            Generate
                          </>
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="lg"
                        onClick={handleReset}
                        disabled={isGenerating}
                      >
                        <RotateCcw className="w-5 h-5" />
                      </Button>
                    </div>
                  </div>

                  {/* Output Panel */}
                  <div className="card-gradient rounded-2xl border border-border p-6 space-y-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-secondary flex items-center justify-center">
                        <svg className="w-5 h-5 text-muted-foreground" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                          <line x1="8" y1="21" x2="16" y2="21" />
                          <line x1="12" y1="17" x2="12" y2="21" />
                        </svg>
                      </div>
                      <div>
                        <h2 className="font-display font-semibold">3D Visualization</h2>
                        <p className="text-sm text-muted-foreground">Your soft robot animation</p>
                      </div>
                    </div>

                    <div className="aspect-square rounded-xl bg-background/50 border border-border flex items-center justify-center overflow-hidden">
                      {isGenerating ? (
                        <div className="text-center space-y-4">
                          <div className="w-16 h-16 mx-auto rounded-full orange-gradient animate-pulse-glow flex items-center justify-center">
                            <Loader2 className="w-8 h-8 text-primary-foreground animate-spin" />
                          </div>
                          <div>
                            <p className="font-display font-medium">AI agent is working...</p>
                            <p className="text-sm text-muted-foreground">Reasoning and generating your model</p>
                          </div>
                        </div>
                      ) : generatedGif ? (
                        <div className="w-full h-full flex items-center justify-center bg-black">
                          <img
                            key={generatedGif}
                            src={generatedGif}
                            alt="Generated Simulation"
                            className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                          />
                        </div>
                      ) : (
                        <div className="text-center space-y-4 p-8">
                          <div className="w-24 h-24 mx-auto rounded-2xl bg-card border border-border flex items-center justify-center">
                            <svg className="w-12 h-12 text-muted-foreground/50" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                              <line x1="12" y1="22.08" x2="12" y2="12" />
                            </svg>
                          </div>
                          <div>
                            <p className="font-display font-medium text-muted-foreground">No visualization yet</p>
                            <p className="text-sm text-muted-foreground">
                              Enter a description and let our agentic AI model your soft object
                            </p>
                          </div>
                        </div>
                      )}
                    </div>

                    {generatedGif && (
                      <div className="flex gap-3">
                        <Button
                          variant="outline"
                          size="lg"
                          className="flex-1"
                          onClick={async () => {
                            if (generatedGif) {
                              try {
                                const response = await fetch(generatedGif);
                                const blob = await response.blob();
                                const url = window.URL.createObjectURL(blob);
                                const link = document.createElement('a');
                                link.href = url;
                                link.download = `simulation-${Date.now()}.gif`;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                                window.URL.revokeObjectURL(url);
                              } catch (error) {
                                console.error('Download failed:', error);
                                window.open(generatedGif, '_blank');
                              }
                            }
                          }}
                        >
                          Download GIF
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </TabsContent>

              {/* Python Script Tab */}
              <TabsContent value="code" className="mt-6">
                <div className="max-w-5xl mx-auto">
                  <PythonEditor
                    key={generatedCode}
                    initialCode={generatedCode || undefined}
                  />
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Workshop;
