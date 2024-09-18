<template>
  <div class="wrapper">
    <user-bar></user-bar>
    <ToDoList></ToDoList>
  </div>
</template>
<script setup>
import ToDoList from '@/components/ToDoList.vue'
import UserBar from '@/components/UserBar.vue'
</script>
<style scoped>
.wrapper {
  padding: 20px;
  display:flex;
  flex-direction: column;
  gap:20px;
  height:100%;
  background-image: url("/login-background.jpg");
  background-blend-mode:color-dodge;
  background-color: var(--sl-color-neutral-300);
}
</style>
