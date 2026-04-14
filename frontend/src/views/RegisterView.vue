<template>
  <div class="register">
    <h1>用户注册</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <div class="error" v-if="error">{{ error }}</div>
      <button type="submit" class="btn">注册</button>
    </form>
    <p>已有账号？<router-link to="/login">立即登录</router-link></p>
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
  email: '',
  password: ''
})

const error = ref('')

const handleRegister = async () => {
  try {
    await userStore.register(form.value.username, form.value.email, form.value.password)
    router.push('/login')
  } catch (err) {
    error.value = err.message
  }
}
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.register h1 {
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

.register p {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register p a {
  color: #4CAF50;
  text-decoration: none;
}

.register p a:hover {
  text-decoration: underline;
}
</style>