<template>
  <the-login-screen
    :background-image="appStore.state['admin.login.background']"
    :logo="appStore.state['admin.login.logo']"
  ></the-login-screen>
</template>

<script setup>
import TheLoginScreen from '@viur/vue-utils/login/TheLoginScreen.vue'
import {useAppStore} from "@/stores/app.js"
const appStore = useAppStore()

</script>
