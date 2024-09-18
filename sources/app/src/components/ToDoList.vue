<template>
  <div class="wrapper-list">
  <sl-bar>
    <div slot="left">
      <h1 class="headline">Aktuelle Aufgaben</h1>
    </div>

    <div slot="right">
      <sl-button-group>
        <sl-select
          hoist
          @sl-change="updatefilter"
          :value="null"
        >
          <sl-option
            :key="null"
            :value="null"
            >Alle</sl-option
          >
          <sl-option
            v-for="(val, akey) in todoListHandler.structure?.['status']?.['values']"
            :key="akey"
            :value="akey"
          >
            {{ val }}
          </sl-option>
        </sl-select>
        <sl-button @click="reload" title="Tabelle neuladen">
          <sl-icon name="arrow-repeat"></sl-icon>
        </sl-button>
    </sl-button-group>
    </div>
  </sl-bar>
  <sl-card>
  <loader v-if="todoListHandler.state.skellist.length===0"></loader>
  <table v-else>
    <thead>
      <tr>
        <template  v-for="(bone, boneName) in todoListHandler.structure"
        :key="boneName">
        <th v-if="state.visibleBones.includes(boneName)"
        :style="{
          width: ['message'].includes(boneName)?'600px':'200px'
        }"
        >
          {{ bone['descr'] }}
        </th>
        </template>

      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(skel, idx) in todoListHandler.state.skellist"
        :key="idx"
        :class="{
          closed:skel['status']==='closed',
          pending:skel['status']==='pending',
        }"
      >
        <template v-for="(value, boneName) in skel">
          <td v-if="state.visibleBones.includes(boneName)">
            <to-do-list-cell :boneName="boneName" :skel="skel"></to-do-list-cell>
          </td>
      </template>
      </tr>
    </tbody>
  </table>
</sl-card>
</div>
</template>
<script setup>
import { ListRequest, Request } from '@viur/vue-utils'
import Loader from '@viur/vue-utils/generic/Loader.vue';
import { onMounted, reactive, provide } from 'vue'
import { getBoneWidget } from '@viur/vue-utils/bones/edit/index'
import ToDoListCell from './table/ToDoListCell.vue';
const todoListHandler = ListRequest('todolist', { module: 'todo' })
provide("listHandler",todoListHandler)

const state = reactive({
  loadingEntry: false,
  filter: {},
  visibleBones:["creationdate","firstname", "lastname","status","category","subject", "message"]
})
provide("listState", state)

function reload() {
  todoListHandler.fetchAll()
}
provide("listReload", reload)

function updatefilter(event) {
  console.log(event)
  if (!event.target.value) {
    state.filter = {}
  } else {
    state.filter = { status: event.target.value }
  }
  todoListHandler.state.params = state.filter
  reload()
}

onMounted(() => {
  reload()
})
</script>
<style scoped>
.wrapper-list{
  display:flex;
  flex-direction: column;
  gap:10px;
}

h1.headline{
  font-size:var(--sl-font-size-2x-large);
}

sl-card{
  position:relative;
  height:100%;
  min-height:200px;

  &::part(base){
    height:100%;
  }
}
sl-select::part(combobox){
  border-top-right-radius:0;
  border-bottom-right-radius:0;
}
table {
  width: 100%;

  & tbody {
    & tr {
      cursor: pointer;
      transition: all ease 0.3s;

      & td {
        padding: 0.4em 0.6em;
        overflow: hidden;
        word-wrap: break-word;
        border-right: 1px solid var(--sl-color-neutral-300);
        border-bottom: 1px solid var(--sl-color-neutral-300);

        &:last-child {
          border-right: 0;
        }
      }

      &:hover {
        background-color: var(--sl-color-neutral-200);
      }
    }
  }

  & thead {
    & th {
      position: relative;
      padding: 0.4em 2.4em 0.4em 0.6em;
      overflow: hidden;
      font-weight: 700;
      font-size: var(--sl-font-size-large);
      border-right: 1px solid var(--sl-color-neutral-300);
      text-overflow: ellipsis;
      border-bottom: 1px solid var(--sl-color-neutral-300);
      padding-bottom: 20px;
      text-align: center;

      &:last-child {
        border-right: 0;
      }
    }
  }

  & tr.closed{
    text-decoration: line-through;
    color: var(--sl-color-neutral-400);
  }
  & tr.pending > *{
    font-weight: 700;
  }
}
</style>
