<template>
  <sl-bar>
    <div slot="left" class="userbar-left">
      <sl-avatar initials="?"
      :label="`${userStore.state.user['lastname']}, ${userStore.state.user['firstname']}`"
      :title="userStore.state.user['name']"
      ></sl-avatar>
      <h1>{{ userStore.state.user['lastname'] }}, {{ userStore.state.user['firstname'] }}</h1>

    </div>
    <div slot="right">
      <sl-button @click="logout" :loading="state.logoutLoading">
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
import { computed, reactive } from 'vue'
import { useUserStore } from '@viur/vue-utils/login/stores/user'
const userStore = useUserStore()

const state = reactive({
  logoutLoading:false
})

function logout(){
  state.logoutLoading=true
  userStore.logout().then(async (resp)=>{
    state.logoutLoading=false
  })
}


</script>

<style>
h1 {
  font-size: var(--sl-font-size-large);
}

.userbar-left{
  display:flex;
  gap:20px;
}
</style>
