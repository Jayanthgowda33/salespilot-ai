import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const linkClass = (path: string) =>
    `transition-colors ${
      location.pathname === path
        ? "text-accent font-semibold"
        : "text-gray-400 hover:text-accentSoft"
    }`;

  return (
    <nav className="bg-panel border-b border-panelBorder px-6 py-4 flex justify-between items-center">
      <span className="font-bold text-lg text-white">
        Sales<span className="text-accent">Pilot</span> AI
      </span>
      <div className="flex gap-6 items-center text-sm">
        <Link to="/dashboard" className={linkClass("/dashboard")}>Dashboard</Link>
        <Link to="/leads" className={linkClass("/leads")}>Leads</Link>
        <button
          onClick={() => { logout(); navigate("/login"); }}
          className="text-gray-500 hover:text-red-400 transition-colors"
        >
          Log out
        </button>
      </div>
    </nav>
  );
}
