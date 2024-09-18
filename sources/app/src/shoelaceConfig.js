// @ts-nocheck
import '@viur/shoelace/dist/themes/viur.css'
import '@viur/shoelace/dist/components/button/button'
import '@viur/shoelace/dist/components/button-group/button-group'
import '@viur/shoelace/dist/components/icon/icon'
import '@viur/shoelace/dist/components/input/input'
import '@viur/shoelace/dist/components/dropdown/dropdown'
import '@viur/shoelace/dist/components/option/option'
import '@viur/shoelace/dist/components/menu/menu'
import '@viur/shoelace/dist/components/menu-item/menu-item'
import '@viur/shoelace/dist/components/badge/badge'
import '@viur/shoelace/dist/components/divider/divider'
import '@viur/shoelace/dist/components/avatar/avatar'
import '@viur/shoelace/dist/components/dialog/dialog'
import '@viur/shoelace/dist/components/tooltip/tooltip'
import '@viur/shoelace/dist/components/split-panel/split-panel'
import '@viur/shoelace/dist/components/radio-group/radio-group'
import '@viur/shoelace/dist/components/radio-button/radio-button'
import '@viur/shoelace/dist/components/select/select'
import '@viur/shoelace/dist/components/spinner/spinner'
import '@viur/shoelace/dist/components/card/card'
import '@viur/shoelace/dist/components/tag/tag'
import '@viur/shoelace/dist/components/tooltip/tooltip'
import '@viur/shoelace/dist/components/checkbox/checkbox'
import '@viur/shoelace/dist/components/drawer/drawer'
import '@viur/shoelace/dist/components/alert/alert'
import '@viur/shoelace/dist/components/tab/tab'
import '@viur/shoelace/dist/components/tab-group/tab-group'
import '@viur/shoelace/dist/components/tab-panel/tab-panel'
import '@viur/shoelace/dist/components/details/details'
import '@viur/shoelace/dist/components/switch/switch'
import '@viur/shoelace/dist/components/combobox/combobox'
import '@viur/shoelace/dist/components/icon-button/icon-button'
import '@viur/shoelace/dist/components/breadcrumb/breadcrumb'
import '@viur/shoelace/dist/components/breadcrumb-item/breadcrumb-item'
import '@viur/shoelace/dist/components/dialog/dialog'
import '@viur/shoelace/dist/components/format-bytes/format-bytes'
import '@viur/shoelace/dist/components/format-date/format-date'
import '@viur/shoelace/dist/components/color-picker/color-picker'
import '@viur/shoelace/dist/components/textarea/textarea'
import '@viur/shoelace/dist/components/animation/animation'
import '@viur/shoelace/dist/components/tree/tree'
import '@viur/shoelace/dist/components/tree-item/tree-item'
import '@viur/shoelace/dist/components/bar/bar'

import { setBasePath, getBasePath } from '@viur/shoelace/dist/utilities/base-path'
import { registerIconLibrary } from '@viur/shoelace/dist/utilities/icon-library.js'

if (import.meta.env.DEV){
  setBasePath(`/app/shoelace`)
}else{
  setBasePath(`shoelace`)
}


