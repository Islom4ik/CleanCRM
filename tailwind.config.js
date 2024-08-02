/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    fontFamily: {
      'Cormorant-Upright': ['light', 'normanl','medium', 'semibold','bold'],
    },
    extend: {
      colors: {
        'dark': '#283036',
        'primary': '#171D7D',
        'secondary': '#c4e3eb'
      }
    },
  },
  plugins: [],
}

