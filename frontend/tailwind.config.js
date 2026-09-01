
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Geist Variable"', 'system-ui', 'sans-serif'],
        display: ['"Geist Variable"', 'serif'], // para números grandes
      },
    },
  },
  plugins: [],
};
