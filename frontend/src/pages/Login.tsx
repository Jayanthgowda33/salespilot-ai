import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed. Check your backend is running.");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-app px-4">
      {/* soft green glow behind the card */}
      <div className="fixed w-72 h-72 bg-accent/20 rounded-full blur-3xl -z-10" />

      <form
        onSubmit={handleSubmit}
        className="animate-fadeInUp animate-glow bg-panel border border-panelBorder p-8 rounded-2xl shadow-xl w-full max-w-sm space-y-5"
      >
        <div>
          <h1 className="text-2xl font-bold text-white">
            Sales<span className="text-accent">Pilot</span> AI
          </h1>
          <p className="text-gray-400 text-sm mt-1">Log in to your account</p>
        </div>

        {error && (
          <p className="text-red-400 text-sm bg-red-950/40 border border-red-900 rounded-lg px-3 py-2">
            {error}
          </p>
        )}

        <div className="space-y-3">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-app border border-panelBorder text-white placeholder-gray-500 rounded-lg px-3 py-2.5 focus:outline-none focus:border-accent transition-colors"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-app border border-panelBorder text-white placeholder-gray-500 rounded-lg px-3 py-2.5 focus:outline-none focus:border-accent transition-colors"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-accent text-black rounded-lg py-2.5 font-semibold hover:bg-accentSoft transition-colors"
        >
          Log in
        </button>

        <p className="text-sm text-gray-500 text-center">
          No account?{" "}
          <Link to="/signup" className="text-accentSoft hover:text-accent">
            Sign up
          </Link>
        </p>
      </form>
    </div>
  );
}
