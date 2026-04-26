<template>
  <div class="login">
    <h1>用户登录</h1>

    <!-- 已登录状态 -->
    <div v-if="userStore.isLoggedIn" class="logged-in card animate-fade-in">
      <div class="icon">👤</div>
      <p>您已登录为 <strong>{{ userStore.user?.username }}</strong>，是否要切换账号？</p>
      <button @click="handleLogout" class="btn btn-secondary">退出登录</button>
      <p>或者 <router-link to="/register">注册新账号</router-link></p>
    </div>

    <!-- 未登录状态 -->
    <div v-else class="card animate-fade-in">
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
        <button type="submit" class="btn btn-primary">登录</button>
      </form>
      <p class="link-text">还没有账号？<router-link to="/register">立即注册</router-link></p>
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
  window.location.reload()
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.login h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.logged-in {
  text-align: center;
  padding: 40px 20px;
}

.logged-in .icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.logged-in p {
  font-size: 18px;
  margin-bottom: 24px;
  line-height: 1.6;
}

.logged-in .btn {
  margin-bottom: 16px;
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

.login a {
  color: #165DFF;
  text-decoration: none;
  font-weight: 600;
}

.login a:hover {
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
  .login {
    padding: 16px;
  }

  .login h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .logged-in {
    padding: 30px 16px;
  }

  .logged-in .icon {
    font-size: 48px;
  }

  .logged-in p {
    font-size: 16px;
  }
}
</style>
