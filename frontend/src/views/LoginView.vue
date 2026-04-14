<template>
  <div class="login">
    <h1>用户登录</h1>
    
    <!-- 已登录状态 -->
    <div v-if="userStore.isLoggedIn" class="logged-in">
      <p>您已登录为 {{ userStore.user?.username }}，是否要切换账号？</p>
      <button @click="handleLogout" class="btn">退出登录</button>
      <p>或者 <router-link to="/register">注册新账号</router-link></p>
    </div>
    
    <!-- 未登录状态 -->
    <div v-else>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="form.username" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="form.password" required />
        </div>
        <div class="error" v-if="error">{{ error }}</div>
        <button type="submit" class="btn">登录</button>
      </form>
      <p>还没有账号？<router-link to="/register">立即注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  password: ''
})

const error = ref('')

const handleLogin = async () => {
  try {
    await userStore.login(form.value.username, form.value.password)
    router.push('/')
  } catch (err) {
    error.value = err.message
  }
}

const handleLogout = () => {
  userStore.logout()
  // 刷新页面，显示登录表单
  window.location.reload()
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.login h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #666;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.error {
  color: red;
  margin-bottom: 20px;
  text-align: center;
}

.btn {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #45a049;
}

.login p {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login p a {
  color: #4CAF50;
  text-decoration: none;
}

.login p a:hover {
  text-decoration: underline;
}
</style>