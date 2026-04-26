<template>
  <div class="register">
    <h1>用户注册</h1>
    <div class="card animate-fade-in">
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
        <button type="submit" class="btn btn-primary">注册</button>
      </form>
      <p class="link-text">已有账号？<router-link to="/login">立即登录</router-link></p>
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
  padding: 20px;
}

.register h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.error {
  color: #ef4444;
  margin-bottom: 20px;
  text-align: center;
  padding: 12px;
  background-color: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
  font-weight: 500;
}

.link-text {
  text-align: center;
  margin-top: 24px;
  color: #64748b;
}

.register a {
  color: #165DFF;
  text-decoration: none;
  font-weight: 600;
}

.register a:hover {
  text-decoration: underline;
}

/* 动画效果 */
.animate-fade-in {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register {
    padding: 16px;
  }

  .register h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }
}
</style>
