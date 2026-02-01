import { Link } from "react-router-dom";
import squishyLogo from "@/assets/squishy-logo.png";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <Link to="/" className="flex items-center gap-3">
            <img
              src={squishyLogo}
              alt="Squishy Logo"
              className="h-8 w-auto object-contain"
            />
          </Link>

          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <Link to="/" className="hover:text-primary transition-colors">
              Home
            </Link>
            <Link to="/workshop" className="hover:text-primary transition-colors">
              Workshop
            </Link>
            <a href="#" className="hover:text-primary transition-colors">
              Documentation
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              Contact
            </a>
          </div>

          <p className="text-sm text-muted-foreground">
            © 2026 Squishy. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
