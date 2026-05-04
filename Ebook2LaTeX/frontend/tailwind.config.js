/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary palette
        primary: {
          50:  "#f0f4ff",
          100: "#dce8ff",
          300: "#93b4fd",
          500: "#4f7df3",
          600: "#3b63d9",
          700: "#2e4fb0",
          900: "#1a2f6b",
        },
        // Surface / dark mode
        surface: {
          900: "#0d1117",
          800: "#161b22",
          700: "#21262d",
          600: "#30363d",
          500: "#444c56",
        },
        // Accent
        accent: {
          400: "#e879f9",
          500: "#d946ef",
          600: "#c026d3",
        },
        // Status
        success: "#22c55e",
        warning: "#f59e0b",
        danger:  "#ef4444",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular"],
      },
      boxShadow: {
        glow:    "0 0 20px rgba(79,125,243,0.35)",
        "glow-sm": "0 0 10px rgba(79,125,243,0.2)",
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px)",
      },
      backgroundSize: {
        grid: "40px 40px",
      },
      animation: {
        "fade-in":    "fadeIn 0.4s ease-out",
        "slide-up":   "slideUp 0.35s ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4,0,0.6,1) infinite",
      },
      keyframes: {
        fadeIn:  { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        slideUp: { "0%": { opacity: 0, transform: "translateY(16px)" }, "100%": { opacity: 1, transform: "translateY(0)" } },
      },
    },
  },
  plugins: [],
};

