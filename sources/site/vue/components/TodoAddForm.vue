<template>
  <div class="wrapper">
    <sl-alert v-if="state.wasSuccess" open variant="success" duration="3000" @sl-hide="state.wasSuccess=false">
      <sl-icon slot="icon" name="check2-circle"></sl-icon>
      <span>Vielen Dank für Ihre Rückmeldung.</span>
    </sl-alert>

    <div >
      <loader v-if="state.formLoading"></loader>
      <vi-form
          ref="addform"
          module="todo"
          action="add"
      >
      </vi-form>
    </div>

    <sl-bar>
      <div slot="right">
        <sl-button variant="success" @click="sendForm" :loading="state.sending">
          <sl-icon name="send" slot="prefix"></sl-icon>
          Senden
        </sl-button>
      </div>
    </sl-bar>
  </div>
</template>
<script setup>
/*
:useCategories="false"
:layout="TodoAddFormLayout"
*/
import {ref, reactive, computed} from 'vue'
import loader from '@viur/vue-utils/generic/Loader.vue'
import TodoAddFormLayout from './TodoAddFormLayout.vue';
import ViForm from '@viur/vue-utils/forms/ViForm.vue'
const addform = ref(null)
const state = reactive({
  sending:undefined,
  wasSuccess:false,
  formLoading:computed(()=>{
    if (!addform.value){
      return true
    }
    return addform.value.state.loading
  })
})


function sendForm(){
  state.sending = true
  addform.value.sendData().then(async (resp)=>{
    let data = await resp.json()
    state.sending = undefined
    if (data['action']==="addSuccess"){
      state.wasSuccess = true
      addform.value.state.skel = {} // clears form
      //window.location.href = "/todo/add?style=success"
    }
  })
}


</script>
<style scoped>
.wrapper{
  display:flex;
  flex-direction: column;
  gap:20px;
  & > div{
    position:relative;
  }
}
sl-alert{

  & span{
    font-weight: bold;
  }

}
</style>
