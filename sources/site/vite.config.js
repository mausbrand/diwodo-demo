import { fileURLToPath, URL } from 'node:url'
import path from "path"
import { defineConfig } from 'vite'
import copy from "rollup-plugin-copy"
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer'

const APPNAME = "site"

function ViurWatcher(options = { filePaths: [] }) {
  /* Observe non vite folder for auto full-reload, can be disabled in config
  */
  return {
    name: 'viurwatcher',
    configureServer(server) {
      options.filePaths.forEach((f) => {
        server.watcher.add(f);
      });
      function onWatchChange(_) {
        let staticFileUpdate = options.filePaths.filter(x=>_.startsWith(x))
        if (staticFileUpdate.length>0){
          server.hot.send({ type: 'full-reload' });
        }

      }
      server.watcher.on('add', onWatchChange);
      server.watcher.on('unlink', onWatchChange);
      server.watcher.on('change', onWatchChange);
    },
  };
}

// https://vitejs.dev/config/
export default defineConfig({
  runtimeCompiler:true,

  plugins: [
    ViteImageOptimizer({
      logStats:false
    }),
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

    ViurWatcher({filePaths:["../../deploy/html"]})
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./vue', import.meta.url)),
      "vue":'vue/dist/vue.esm-bundler'
    }
  },
  server:{
    origin:"http://localhost:8081"
  },
  base: process.env.NODE_ENV === "production" ? `/static/${APPNAME}/` : "/",
  build: {
    emptyOutDir: true,
    manifest:true,
    assetsInlineLimit:0,
    outDir: `../../deploy/static/${APPNAME}`,
    rollupOptions: {
      output: {
        chunkFileNames: (chunkinfo) => {
          if (
            chunkinfo["moduleIds"].filter((x) => x.includes("node_modules/@viur/shoelace/dist/components")).length > 0
          ) {
            return `[name].js`
          } else {
            return `[name]-[hash].js`
          }
        },
        manualChunks(id) {
          if (id.includes("node_modules/@viur/shoelace/dist/components")) {
            return "shoelace/component_" + id.split("/").slice(-2)[0]
          }
          if (id.includes("node_modules/vue")){
            return `vue/${id.split('node_modules/')[1]}`
          }
          if (id.includes("node_modules/@viur/ckeditor5-build-classic/build/ckeditor.js")) {
            return "viur-ckeditor.js"
          }
        }
      }
    }
  }
})
