/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Custom palette for the dark theme. Use these class names
        // everywhere instead of the default slate/gray so the whole
        // app stays visually consistent: bg-app, bg-panel, text-accent, etc.
        app: "#0a0a0a",          // page background (near-black)
        panel: "#141414",        // card / panel background
        panelBorder: "#242424",  // subtle borders on cards
        accent: "#22c55e",       // primary green (buttons, highlights)
        accentSoft: "#4ade80",   // lighter green (secondary text/links)
        accentDim: "#14532d",    // dark green (badges, hover backgrounds)
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        glow: {
          "0%, 100%": { boxShadow: "0 0 20px rgba(34,197,94,0.15)" },
          "50%": { boxShadow: "0 0 35px rgba(34,197,94,0.35)" },
        },
      },
      animation: {
        fadeInUp: "fadeInUp 0.5s ease-out",
        glow: "glow 3s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
