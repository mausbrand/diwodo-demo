<template>
  <sl-input
    ref="stringBone"
    :placeholder="boneState.bonestructure.descr"
    :disabled="boneState.readonly"
    :value="Utils.unescape(value)"
    :required="boneState.bonestructure.required"
    @sl-change="changeEvent"
    @keyup="changeEvent"
  ></sl-input>
</template>

<script lang="ts">
//@ts-nocheck
import { reactive, defineComponent, onMounted, inject, computed, watchEffect, ref } from "vue"
import { useTimeoutFn } from "@vueuse/core"
import Utils from "@viur/vue-utils//bones/utils"

export default defineComponent({
  inheritAttrs: false,
  props: {
    name: String,
    value: [Object, String, Number, Boolean, Array],
    index: Number,
    lang: String,
    autofocus: Boolean
  },
  components: {},
  emits: ["change"],
  setup(props, context) {
    const boneState = inject("boneState")
    const state = reactive({
      value: computed(() => props.value)
    })

    const stringBone = ref(null)

    function changeEvent(event) {
      context.emit("change", props.name, event.target.value, props.lang, props.index)
    }

    watchEffect(() => {
      if (props.autofocus) {
        if (stringBone.value && stringBone.value !== null && stringBone !== null) {
          const { start } = useTimeoutFn(() => {
            stringBone.value.focus()
          }, 600)

          start()
        }
      }
    })

    onMounted(() => {
      context.emit("change", props.name, props.value, props.lang, props.index) //init
    })

    return {
      state,
      Utils,
      boneState,
      changeEvent,
      stringBone
    }
  }
})
</script>

<style scoped>
sl-input {
  width: 100%;

  &::part(base) {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }

  @media (max-width: 900px) {
    &::part(base) {
      border-top-right-radius: 0;
      border-bottom-left-radius: var(--sl-border-radius-medium);
    }
  }
}
</style>
