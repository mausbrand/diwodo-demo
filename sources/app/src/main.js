import './shoelaceConfig'

import bone from '@viur/vue-utils/bones/edit/bone.vue'
import Wrapper_nested from '@viur/vue-utils/bones/edit/wrapper_nested.vue'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import CKEditor from '@ckeditor/ckeditor5-vue'

import { createI18n } from 'vue-i18n'
import en from './translations/en'
import de from './translations/de'
import { de_translations, en_translations } from '@viur/vue-components/translations/translations'

const app = createApp(App)

app.component('Bone', bone)
app.component('WrapperNested', Wrapper_nested)

const i18n = createI18n({
  locale: 'de',
  fallbackLocale: 'en',
  messages: { en: { ...en_translations, ...en }, de: { ...de_translations, ...de } }
})

app.use(createPinia())
app.use(router)
app.use(CKEditor)
app.use(i18n)

app.mount('#app')
