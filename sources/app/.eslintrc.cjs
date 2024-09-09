/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-prettier/skip-formatting'
  ],
  parserOptions: {
    ecmaVersion: 'latest'
  },
  rules: {
    "vue/html-self-closing": 0,
    "no-unused-vars": 1,
    "vue/order-in-components": 0,
    "vue/no-deprecated-slot-attribute": 0,
    "vue/no-setup-props-destructure": 1
  }
}
