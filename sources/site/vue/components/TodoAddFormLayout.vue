<template>

  <sl-card v-if="Object.keys(formState.structure).length>0">
    <h2 class="headline">Persönliche Angaben</h2>
    <div class="wrapper-name">
      <slot boneName="firstname"
            :widget="customStringBone"
            label="hide"
      >
      </slot>

      <slot boneName="lastname"
            :widget="customStringBone"
            label="hide"
      >
      </slot>
    </div>

    <slot boneName="category"
          :widget="getBoneWidget(formState.structure['category']['type'])"
          label="top"
    >
    </slot>
    <slot boneName="subject"
          :widget="getBoneWidget(formState.structure['subject']['type'])"
          label="hide"
    >
    </slot>

    <slot boneName="message"
          :widget="getBoneWidget(formState.structure['message']['type'])"
          label="hide"
    >
    </slot>


  </sl-card>


</template>
<script setup>
import {inject} from 'vue'
import {getBoneWidget} from "@viur/vue-utils/bones/edit";
import customStringBone from './customStringBone.vue';
const formState = inject("formState")
const formUpdate = inject("formUpdate")
</script>
<style scoped>
.wrapper-name{
  display:flex;
  gap:20px;
}

:deep(.bone-wrapper) {
  & sl-input::part(base) {
    border-radius: var(--sl-input-border-radius-medium);
  }

  & sl-select::part(combobox) {
    border-radius: var(--sl-input-border-radius-medium);
  }
}

:deep(.bone-wrapper:last-child) {
  margin-bottom: 0;
}

</style>
