import { fileURLToPath, URL } from 'node:url'
import path from 'path'
import copy from "rollup-plugin-copy"
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const APPNAME = "app"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    copy({
      targets: [
        {
          src: path.join(__dirname, "node_modules", "@viur", "shoelace", "dist", "assets"),
          dest: path.join(__dirname, "public", "shoelace")
        }
      ]
    }),
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith("sl-")
        }
      }
    }),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  base:`/${APPNAME}`,
  build:{
    outDir: path.resolve(__dirname, `../../deploy/${APPNAME}`),
    assetsInlineLimit: 0
  }
})
