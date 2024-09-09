<template>
  <div class="wrapper">
  <sl-bar>
    <div slot="left">
      <h1 class="headline">Meine Todo's</h1>
    </div>

    <div slot="right">
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
      <sl-button @click="reload">
        <sl-icon name="arrow-repeat"></sl-icon>
      </sl-button>
    </div>
  </sl-bar>

  <table>
    <thead>
      <tr>
        <th
          v-for="(bone, boneName) in todoListHandler.structure"
          :key="boneName"
        >
          {{ bone['descr'] }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(skel, idx) in todoListHandler.state.skellist"
        :key="idx"
      >
        <td v-for="(value, boneName) in skel">
          <template v-if="boneName === 'status'">
            <sl-spinner v-if="state.loadingEntry"></sl-spinner>
            <sl-select
              v-else
              hoist
              :value="value"
              @sl-change="updateStatus($event, skel)"
            >
              <sl-option
                v-for="(val, akey) in todoListHandler.structure[boneName]['values']"
                :key="akey"
                :value="akey"
              >
                {{ val }}
              </sl-option>
            </sl-select>
          </template>
          <template v-else>
            {{ value }}
          </template>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</template>
<script setup>
import { ListRequest, Request } from '@viur/vue-utils'
import { onMounted, reactive } from 'vue'
import { getBoneWidget } from '@viur/vue-utils/bones/edit/index'
const todoListHandler = ListRequest('todolist', { module: 'todo' })

const state = reactive({
  loadingEntry: false,
  filter: {}
})

function reload() {
  todoListHandler.fetchAll()
}

function updateStatus(event, skel) {
  state.loadingEntry = true
  Request.edit('todo', skel['key'], {
    dataObj: {
      status: event.target.value
    }
  })
    .then((resp) => {
      state.loadingEntry = false
      reload()
    })
    .catch((error) => {
      state.loadingEntry = false
      reload()
    })
}

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
.wrapper{
  display:flex;
  flex-direction: column;
  gap:10px;
}
table {
  width: 100%;
  table-layout: fixed;

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
      border-right: 1px solid var(--sl-color-neutral-300);
      text-overflow: ellipsis;

      &:last-child {
        border-right: 0;
      }
    }
  }
}
</style>
