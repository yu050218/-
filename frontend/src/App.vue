<template>
  <div class="app" :class="{ dark: themeStore.isDark }">
    <NavBar />
    <div class="theme-toggle" @click="themeStore.toggleTheme">
      <span v-if="themeStore.isDark">🌞</span>
      <span v-else>🌙</span>
    </div>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'
import { useThemeStore } from './stores/theme'
import NavBar from './components/NavBar.vue'

const userStore = useUserStore()
const themeStore = useThemeStore()

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
  transition: all 0.3s ease;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
}

.app {
  min-height: 100vh;
  position: relative;
}

/* 深色模式 */
.app.dark {
  background-color: #0f172a;
  color: #f1f5f9;
}

.main-content {
  padding-top: 90px;
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 40px;
}

/* 主题切换按钮 */
.theme-toggle {
  position: fixed;
  top: 85px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 999;
  font-size: 24px;
  animation: pulse 2s infinite;
}

.theme-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 动画效果 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* 卡片样式 */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  padding: 24px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.app.dark .card {
  background: #1e293b;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 按钮样式 */
.btn {
  display: inline-block;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  text-align: center;
}

.btn-primary {
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(22, 93, 255, 0.4);
}

.btn-secondary {
  background: #e2e8f0;
  color: #1e293b;
}

.app.dark .btn-secondary {
  background: #334155;
  color: #f1f5f9;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* 表单样式 */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.app.dark .form-group input {
  background: #334155;
  border-color: #475569;
  color: #f1f5f9;
}

.form-group input:focus {
  outline: none;
  border-color: #165DFF;
  box-shadow: 0 0 0 3px rgba(22, 93, 255, 0.1);
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app.dark h1, .app.dark h2, .app.dark h3, .app.dark h4, .app.dark h5, .app.dark h6 {
  background: linear-gradient(135deg, #60a5fa, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding-top: 80px;
    padding-left: 16px;
    padding-right: 16px;
    padding-bottom: 30px;
  }

  .card {
    padding: 16px;
  }

  .theme-toggle {
    top: 75px;
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}
</style>
