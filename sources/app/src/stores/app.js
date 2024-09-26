import { reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import { Request } from '@viur/vue-utils'
import { useUserStore } from '@viur/vue-utils/login/stores/user'
import { useColorStore } from '@/stores/color.js'



export const useAppStore = defineStore('app', () => {
  const userStore = useUserStore()
  const colorStore = useColorStore()
  const router = useRouter()

  const state = reactive({
    init: false,
    "admin.login.background": publicAsset("login-background.jpg"),
    "admin.login.logo": publicAsset("logo.svg"),
    "admin.color.primary": "",
    "admin.color.secondary": ""
  })

  async function init() {
    Request.get('/vi/settings')
      .then(async (resp) => {
        let data = await resp.json()

        for (const key in data) {
          if (data[key] !== undefined || data[key] !== null) {
            if (data[key].length > 0) {
              if ((key.endsWith(".logo") || key.endsWith(".background")) && !key.startsWith("/")) {
                state[key] = publicAsset(data[key])
                continue
              }
              state[key] = data[key]
            }
            if (key === "admin.color.primary") {
              colorStore.state.primaryColor = state[key]
            }
            if (key === "admin.color.secondary") {
              colorStore.state.secondaryColor = state[key]
            }
          }
        }


        if (data['admin.user.google.clientID']) {
          userStore.googleInit(data['admin.user.google.clientID']).catch(() => {
            throw new Error('clientId is required since the plugin is not initialized with a Client Id')
          })
        }
        await userStore.updateUser()
        state['init'] = true
      })
      .catch((error) => {
        console.log(error)
      })
  }

  watch(
    () => userStore.state['user.loggedin'],
    (newVal, oldVal) => {
      //wenn login success nach home redirecten
      if (newVal === 'yes' && oldVal !== 'yes') {
        router.replace({ name: 'home' })
        // wenn logout zurück zur loginseite
      } else if (newVal === 'no' && oldVal === 'yes') {
        router.replace({ name: 'login' })
      }
    }
  )

    function publicAsset(path, prefix = "app") {
    if (import.meta.env.DEV) {
      if(path.startsWith("/")){
        return `${import.meta.env.VITE_API_URL}${path}`
      }else{
        return `${prefix}/${path}`
      }

    }
    return path
}

  return {
    state,
    init,
    publicAsset
  }
})
