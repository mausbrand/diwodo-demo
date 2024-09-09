<template>
  <RouterView />
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAppStore } from './stores/app'

const appStore = useAppStore()

onBeforeMount(() => {
  appStore.init()
})
</script>

<style scoped></style>
<style lang="postcss">
@import 'style/style.css';
</style>
