<template>
  <div class="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()

onMounted(async () => {
  // 检查是否有token，如果有则获取用户信息
  if (userStore.token) {
    try {
      await userStore.getProfile()
    } catch (error) {
      // 如果获取失败，清除token
      userStore.logout()
    }
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>