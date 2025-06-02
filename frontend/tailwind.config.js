/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1a56db",
        secondary: "#7e3af2",
        accent: "#0694a2",
        danger: "#e02424",
        success: "#0e9f6e",
        warning: "#ff5a1f",
        dark: "#121212",
      },
    },
  },
  plugins: [],
}

