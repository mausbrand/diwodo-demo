<template>
   <template v-if="boneName === 'status'">
      <sl-spinner v-if="listState.loadingEntry"></sl-spinner>
      <sl-select
        v-else
        hoist
        :value="skel[boneName]"
        @sl-change="updateStatus($event, skel)"
      >
        <sl-option
          v-for="(val, akey) in listHandler.structure[boneName]['values']"
          :key="akey"
          :value="akey"
        >
          {{ val }}
        </sl-option>
      </sl-select>
    </template>

    <template v-else-if="boneName === 'category'">
      {{ listHandler.structure[boneName]['values'][skel[boneName]] }}
    </template>

    <template v-else-if="listHandler.structure[boneName]['type']==='date'">
        <sl-format-date hour-format="24" lang="de" :date="skel[boneName]"
                        hour="numeric"
                        minute="numeric"
                        second="numeric"
                        day="numeric"
                        month="numeric"
                        year="numeric"
                        weekday="long">
      </sl-format-date>
    </template>

    <template v-else>
      {{ skel[boneName] || "-" }}
    </template>
</template>
<script setup>
import { Request } from '@viur/vue-utils'
import { inject } from 'vue';
const props = defineProps({
  boneName:String,
  skel:Object
})
const listState = inject('listState')
const listHandler = inject('listHandler')
const listReload = inject('listReload')

function updateStatus(event, skel) {
  listState.loadingEntry = true
  Request.edit('todo', skel['key'], {
    dataObj: {
      status: event.target.value
    }
  })
    .then((resp) => {
      listState.loadingEntry = false
      listReload()
    })
    .catch((error) => {
      listState.loadingEntry = false
      listReload()
    })
}

</script>
