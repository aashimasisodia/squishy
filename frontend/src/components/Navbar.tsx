import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import squishyLogo from "@/assets/squishy-logo.png";

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <img
            src={squishyLogo}
            alt="Squishy Logo"
            className="h-10 w-auto object-contain transition-transform group-hover:scale-105"
          />
        </Link>

        <div className="flex items-center gap-2">
          <Link to="/">
            <Button
              variant={location.pathname === "/" ? "default" : "ghost"}
              size="sm"
            >
              Home
            </Button>
          </Link>
          <Link to="/workshop">
            <Button
              variant={location.pathname === "/workshop" ? "hero" : "hero-outline"}
              size="sm"
            >
              Workshop
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
