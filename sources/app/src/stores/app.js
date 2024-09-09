import { reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import { Request } from '@viur/vue-utils'
import { useUserStore } from '@viur/vue-utils/login/stores/user'

export const useAppStore = defineStore('app', () => {
  const userStore = useUserStore()
  const router = useRouter()

  const state = reactive({
    init: false,
    name: 'TODO'
  })

  async function init() {
    Request.get('/vi/settings')
      .then(async (resp) => {
        let data = await resp.json()

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

  return {
    state,
    init
  }
})
