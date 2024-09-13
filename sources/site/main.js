import '@viur/ignite/ignite.css' // load ignite defaults
import './shoelaceConfig.js' // import a selection of components
import './styles/style.css' // load app style

// ----------------------------------------------
// VUE JS
// ----------------------------------------------

import bone from '@viur/vue-utils/bones/edit/bone.vue'
import Wrapper_nested from '@viur/vue-utils/bones/edit/wrapper_nested.vue'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import CKEditor from '@ckeditor/ckeditor5-vue'

import { createI18n } from 'vue-i18n'
import en from '@/translations/en'
import de from '@/translations/de'
import { de_translations, en_translations } from '@viur/vue-components/translations/translations'

const app = createApp({})

app.component('Bone', bone)
app.component('WrapperNested', Wrapper_nested)

const i18n = createI18n({
  locale: 'de',
  fallbackLocale: 'en',
  messages: { en: { ...en_translations, ...en }, de: { ...de_translations, ...de } }
})

app.use(createPinia())
app.use(CKEditor)
app.use(i18n)

// exposed Components
import TodoAddForm from './vue/components/TodoAddForm.vue'
app.component("TodoAddForm",TodoAddForm)



// mount app
app.mount('#vite_context')



import './scripts/main.js' // load non vue scripts

