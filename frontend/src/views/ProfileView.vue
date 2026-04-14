<template>
  <div class="profile">
    <h1>个人中心</h1>
    
    <!-- 未登录状态 -->
    <div v-if="!userStore.isLoggedIn" class="not-logged-in">
      <p>请先登录以查看个人信息</p>
      <router-link to="/login" class="btn">登录</router-link>
    </div>
    
    <!-- 已登录状态 -->
    <div v-else>
      <!-- 用户信息 -->
      <div v-if="userStore.user" class="user-info">
        <h2>个人信息</h2>
        <div class="info-item">
          <span class="label">用户名:</span>
          <span class="value">{{ userStore.user.username }}</span>
        </div>
        <div class="info-item">
          <span class="label">邮箱:</span>
          <span class="value">{{ userStore.user.email }}</span>
        </div>
        <div class="info-item">
          <span class="label">注册时间:</span>
          <span class="value">{{ formatDate(userStore.user.created_at) }}</span>
        </div>
      </div>
      <div v-else class="loading">
        <p>加载个人信息中...</p>
      </div>
      
      <!-- 修改信息表单 -->
      <div v-if="userStore.user" class="edit-profile">
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
          <button type="submit" class="btn">更新信息</button>
        </form>
      </div>
      
      <!-- 操作按钮 -->
      <div class="profile-actions">
        <button @click="handleLogout" class="btn logout">退出登录</button>
        <router-link to="/test" class="btn">开始测试</router-link>
        <router-link to="/report" class="btn">测试报告</router-link>
        <router-link to="/wrong-words" class="btn">错题本</router-link>
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
    // 清空密码字段
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
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.not-logged-in {
  text-align: center;
  padding: 60px 0;
}

.not-logged-in p {
  margin-bottom: 30px;
  font-size: 18px;
  color: #666;
}

.user-info {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
}

.user-info h2 {
  margin-bottom: 20px;
  color: #666;
}

.info-item {
  margin-bottom: 15px;
  display: flex;
}

.info-item .label {
  width: 100px;
  font-weight: bold;
  color: #333;
}

.info-item .value {
  color: #666;
}

.edit-profile {
  margin-bottom: 40px;
}

.edit-profile h2 {
  margin-bottom: 20px;
  color: #666;
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

.success {
  color: green;
  margin-bottom: 20px;
  text-align: center;
}

.btn {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn:hover {
  background-color: #45a049;
}

.logout {
  background-color: #f44336;
}

.logout:hover {
  background-color: #da190b;
}

.profile-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.profile-actions .btn {
  margin: 0 10px;
}
</style>