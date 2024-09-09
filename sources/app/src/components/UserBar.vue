<template>
  <sl-bar>
    <h1 slot="left">{{ userStore.state.user['name'] }}</h1>
    <div slot="right">
      <sl-button @click="userStore.logout">
        Logout
        <sl-icon
          slot="prefix"
          name="box-arrow-right"
        ></sl-icon>
      </sl-button>
    </div>
  </sl-bar>
</template>

<script setup>
import { reactive } from 'vue'
import { useUserStore } from '@viur/vue-utils/login/stores/user'
const userStore = useUserStore()
</script>

<style>
h1 {
  font-size: var(--ignt-font-size-large);
}
</style>
