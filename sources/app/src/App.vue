<template>
  <RouterView />
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAppStore } from './stores/app'
import { useColorStore } from './stores/color'

const appStore = useAppStore()
const colorStore = useColorStore()

onBeforeMount(() => {
  appStore.init()
})

function getPrimaryColor(lightness) {
  return colorStore.getPrimaryColor(lightness)
}

function getSecondaryColor(lightness) {
  return colorStore.getSecondaryColor(lightness)
}

function getPrimaryAlphaColor(lightness,alpha) {
  return colorStore.getAlphaColor("primaryColor", lightness, alpha)
}


</script>

<style scoped></style>
<style lang="postcss">
@import 'style/style.css';
* {
  --sl-color-primary-50: v-bind(getPrimaryColor(83));
  --sl-color-primary-100: v-bind(getPrimaryColor(78));
  --sl-color-primary-200: v-bind(getPrimaryColor(68));
  --sl-color-primary-300: v-bind(getPrimaryColor(58));
  --sl-color-primary-400: v-bind(getPrimaryColor(48));
  --sl-color-primary-500: v-bind(getPrimaryColor(43));
  --sl-color-primary-600: v-bind(getPrimaryColor(38));
  --sl-color-primary-700: v-bind(getPrimaryColor(28));
  --sl-color-primary-800: v-bind(getPrimaryColor(18));
  --sl-color-primary-900: v-bind(getPrimaryColor(8));
  --sl-color-primary-950: v-bind(getPrimaryColor(3));

  --sl-color-secondary-50: v-bind(getSecondaryColor(60));
  --sl-color-secondary-100: v-bind(getSecondaryColor(55));
  --sl-color-secondary-200: v-bind(getSecondaryColor(45));
  --sl-color-secondary-300: v-bind(getSecondaryColor(35));
  --sl-color-secondary-400: v-bind(getSecondaryColor(25));
  --sl-color-secondary-500: v-bind(getSecondaryColor(20));
  --sl-color-secondary-600: v-bind(getSecondaryColor(15));
  --sl-color-secondary-700: v-bind(getSecondaryColor(5));
  --sl-color-secondary-800: v-bind(getSecondaryColor(0));
  --sl-color-secondary-900: v-bind(getSecondaryColor(0));
  --sl-color-secondary-950: v-bind(getSecondaryColor(0));

  --sl-input-border-color-focus: var(--sl-color-primary-500);
  --sl-input-focus-ring-color: v-bind(getPrimaryAlphaColor(43, 40));
}
</style>

