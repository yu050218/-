<template>
  <div class="profile">
    <h1>个人中心</h1>

    <!-- 未登录状态 -->
    <div v-if="!userStore.isLoggedIn" class="not-logged-in card animate-fade-in">
      <div class="icon">🔒</div>
      <p>请先登录以查看个人信息</p>
      <router-link to="/login" class="btn btn-primary">登录</router-link>
    </div>

    <!-- 已登录状态 -->
    <div v-else>
      <!-- 用户信息 -->
      <div v-if="userStore.user" class="user-info card animate-fade-in" style="animation-delay: 0.1s">
        <h2>个人信息</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">用户名</span>
            <span class="value">{{ userStore.user.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">邮箱</span>
            <span class="value">{{ userStore.user.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">注册时间</span>
            <span class="value">{{ formatDate(userStore.user.created_at) }}</span>
          </div>
        </div>
      </div>
      <div v-else class="loading card animate-fade-in">
        <p>加载个人信息中...</p>
      </div>

      <!-- 修改信息表单 -->
      <div v-if="userStore.user" class="edit-profile card animate-fade-in" style="animation-delay: 0.2s">
        <h2>修改信息</h2>
        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <label for="email">邮箱</label>
            <input type="email" id="email" v-model="form.email" required />
          </div>
          <div class="form-group">
            <label for="password">新密码（留空不修改）</label>
            <input type="password" id="password" v-model="form.password" />
          </div>
          <div class="error" v-if="error">{{ error }}</div>
          <div class="success" v-if="success">{{ success }}</div>
          <button type="submit" class="btn btn-primary">更新信息</button>
        </form>
      </div>

      <!-- 操作按钮 -->
      <div class="profile-actions card animate-fade-in" style="animation-delay: 0.3s">
        <button @click="handleLogout" class="btn btn-danger">退出登录</button>
        <router-link to="/test" class="btn btn-primary">开始测试</router-link>
        <router-link to="/report" class="btn btn-secondary">测试报告</router-link>
        <router-link to="/wrong-words" class="btn btn-secondary">错题本</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  email: '',
  password: ''
})

const error = ref('')
const success = ref('')

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const loadProfile = async () => {
  if (userStore.isLoggedIn) {
    try {
      await userStore.getProfile()
      if (userStore.user) {
        form.value.email = userStore.user.email
      }
    } catch (error) {
      console.error('Error loading profile:', error)
    }
  }
}

const handleUpdate = async () => {
  try {
    await userStore.updateProfile(form.value.email, form.value.password)
    success.value = '信息更新成功'
    error.value = ''
    form.value.password = ''
  } catch (err) {
    error.value = err.message
    success.value = ''
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.not-logged-in {
  text-align: center;
  padding: 60px 20px;
}

.not-logged-in .icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.not-logged-in p {
  margin-bottom: 30px;
  font-size: 18px;
  color: #64748b;
}

.user-info h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.info-grid {
  display: grid;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8fafc;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.info-item:hover {
  background-color: #f1f5f9;
  transform: translateX(4px);
}

.info-item .label {
  font-weight: 600;
  color: #64748b;
}

.info-item .value {
  color: #1e293b;
  font-weight: 500;
}

.edit-profile h2 {
  margin-bottom: 24px;
  font-size: 20px;
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

.success {
  color: #10b981;
  margin-bottom: 20px;
  text-align: center;
  padding: 12px;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 8px;
  font-weight: 500;
}

.profile-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  padding: 30px;
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.4);
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
  .profile {
    padding: 16px;
  }

  .profile h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .not-logged-in {
    padding: 40px 16px;
  }

  .not-logged-in .icon {
    font-size: 48px;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .profile-actions {
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }

  .profile-actions .btn {
    width: 200px;
  }
}
</style>
