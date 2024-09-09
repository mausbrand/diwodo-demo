import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@viur/vue-utils/login/stores/user'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      meta: {
        layout: 'TheDefaultLayout'
      },
      component: () => import('../views/LoginView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // wenn nicht eingeloggt, und Seite nicht login > redirect to login
  if (to.name !== 'login' && !userStore.state['user']) {
    next({
      path: 'login',
      replace: true
    })
  } else {
    next()
  }
})

export default router
