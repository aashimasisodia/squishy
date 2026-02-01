import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Copy, Download, FileCode2, Check } from "lucide-react";

interface PythonEditorProps {
  initialCode?: string;
}

const defaultPythonCode = `please generate a soft object and the python code will be displayed here
`;

const PythonEditor = ({ initialCode = defaultPythonCode }: PythonEditorProps) => {
  const [copied, setCopied] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);

  // Use initialCode directly since it's read-only
  const code = initialCode;

  const handleScroll = () => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const element = document.createElement("a");
    const file = new Blob([code], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = `simulation-${Date.now()}.py`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Simple line numbers
  const lineCount = code.split("\n").length;

  return (
    <div className="card-gradient rounded-2xl border border-border overflow-hidden h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-background/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
            <FileCode2 className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h2 className="font-display font-semibold text-sm">Python Script</h2>
            <p className="text-xs text-muted-foreground">View generated code</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleCopy} className="h-8 px-3 text-xs">
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                Copy
              </>
            )}
          </Button>
          <Button variant="hero" size="sm" onClick={handleDownload} className="h-8 px-3 text-xs">
            <Download className="w-3.5 h-3.5" />
            Download
          </Button>
        </div>
      </div>

      {/* Editor Area */}
      <div className="flex-1 overflow-hidden relative aspect-video">
        <div className="absolute inset-0 flex">
          <textarea
            ref={textareaRef}
            onScroll={handleScroll}
            value={code}
            readOnly
            className="flex-1 h-full pl-12 pr-4 py-4 bg-transparent font-mono text-sm leading-6 text-foreground resize-none focus:outline-none placeholder:text-muted-foreground z-10 cursor-default"
            spellCheck={false}
            style={{
              tabSize: 4,
            }}
          />
          {/* Line Numbers - absolutely positioned to scroll with content */}
          <div className="absolute left-0 top-0 bottom-0 w-10 bg-background/30 border-r border-border py-4 select-none overflow-hidden pointer-events-none z-0">
            <div
              ref={lineNumbersRef}
              className="font-mono text-xs text-muted-foreground/50 leading-6 text-right pr-2 h-full overflow-hidden"
            >
              {Array.from({ length: lineCount }, (_, i) => (
                <div key={i}>{i + 1}</div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between px-4 py-2 border-t border-border bg-background/30 text-xs text-muted-foreground">
        <span>Python 3.11</span>
        <span>{lineCount} lines</span>
      </div>
    </div>
  );
};

export default PythonEditor;
