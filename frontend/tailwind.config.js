/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'honda-red': '#CC0000',
        'whatsapp': '#25D366',
        'whatsapp-dark': '#128C7E',
      }
    },
  },
  plugins: [],
}
