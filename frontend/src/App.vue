<template>
  <div class="app" :class="{ dark: themeStore.isDark }">
    <div class="night-sky" v-if="themeStore.isDark">
      <div class="nebula"></div>
      <div class="stars"></div>
      <div class="stars second"></div>
    </div>
    <div class="day-sky" v-else>
      <div class="sun-container">
        <div class="sun-core"></div>
        <div class="sun-ring ring-1"></div>
        <div class="sun-ring ring-2"></div>
        <div class="sun-ring ring-3"></div>
      </div>
    </div>
    <NavBar />
    <div class="theme-toggle" @click="themeStore.toggleTheme">
      <svg v-if="themeStore.isDark" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>
      <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
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
  background-color: #f1f5f9;
  color: #1e293b;
  line-height: 1.6;
}

.app {
  min-height: 100vh;
  position: relative;
}

/* 日间模式太阳效果 */
.day-sky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
}

.day-sky::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at 30% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 60%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
              radial-gradient(ellipse at 50% 80%, rgba(30, 64, 175, 0.03) 0%, transparent 30%);
  animation: lightShift 15s ease-in-out infinite;
}

@keyframes lightShift {
  0%, 100% {
    transform: translate(0, 0);
  }
  33% {
    transform: translate(2%, 1%);
  }
  66% {
    transform: translate(-1%, 2%);
  }
}

.sun-container {
  position: absolute;
  top: 8%;
  left: 12%;
  width: 120px;
  height: 120px;
}

.sun-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255, 255, 255, 0.95) 0%, rgba(200, 220, 255, 0.8) 50%, rgba(100, 150, 255, 0.3) 100%);
  border-radius: 50%;
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.6), 0 0 60px rgba(100, 150, 255, 0.4);
}

.sun-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 50%;
  border: 1px solid;
  transform: translate(-50%, -50%);
}

.ring-1 {
  width: 60px;
  height: 60px;
  border-color: rgba(100, 150, 255, 0.3);
  animation: rotateRing 20s linear infinite;
}

.ring-2 {
  width: 90px;
  height: 90px;
  border-color: rgba(100, 150, 255, 0.2);
  animation: rotateRing 30s linear infinite reverse;
}

.ring-3 {
  width: 120px;
  height: 120px;
  border-color: rgba(100, 150, 255, 0.1);
  animation: rotateRing 40s linear infinite;
}

@keyframes rotateRing {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

/* 日间模式 */
.app:not(.dark) {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.app:not(.dark)::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at top left, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
              radial-gradient(ellipse at bottom right, rgba(30, 64, 175, 0.03) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* 夜间模式星空背景 */
.night-sky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background: linear-gradient(135deg, #0a0f1a 0%, #1a1a2e 50%, #16213e 100%);
}

.nebula {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 150vmax;
  height: 150vmax;
  transform: translate(-50%, -50%);
  background: conic-gradient(from 0deg, transparent 0deg, rgba(30, 64, 175, 0.03) 30deg, transparent 60deg, rgba(59, 130, 246, 0.02) 90deg, transparent 120deg, rgba(99, 102, 241, 0.03) 150deg, transparent 180deg, rgba(30, 64, 175, 0.02) 210deg, transparent 240deg, rgba(59, 130, 246, 0.03) 270deg, transparent 300deg, rgba(99, 102, 241, 0.02) 330deg, transparent 360deg);
  animation: rotateNebula 120s linear infinite;
  opacity: 0.8;
}

.nebula::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100vmax;
  height: 100vmax;
  transform: translate(-50%, -50%);
  background: conic-gradient(from 180deg, transparent 0deg, rgba(59, 130, 246, 0.04) 45deg, transparent 90deg, rgba(30, 64, 175, 0.03) 135deg, transparent 180deg, rgba(99, 102, 241, 0.04) 225deg, transparent 270deg, rgba(59, 130, 246, 0.03) 315deg, transparent 360deg);
  animation: rotateNebula 90s linear infinite reverse;
  opacity: 0.6;
}

@keyframes rotateNebula {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(2px 2px at 20px 30px, rgba(200, 220, 255, 0.8), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(200, 220, 255, 0.6), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(200, 220, 255, 0.7), transparent),
    radial-gradient(2px 2px at 160px 120px, rgba(200, 220, 255, 0.8), transparent),
    radial-gradient(1px 1px at 230px 80px, rgba(200, 220, 255, 0.6), transparent),
    radial-gradient(2px 2px at 300px 150px, rgba(200, 220, 255, 0.5), transparent),
    radial-gradient(1px 1px at 350px 200px, rgba(200, 220, 255, 0.7), transparent),
    radial-gradient(2px 2px at 420px 60px, rgba(200, 220, 255, 0.6), transparent),
    radial-gradient(1px 1px at 480px 180px, rgba(200, 220, 255, 0.8), transparent),
    radial-gradient(2px 2px at 550px 100px, rgba(200, 220, 255, 0.7), transparent),
    radial-gradient(1px 1px at 620px 220px, rgba(200, 220, 255, 0.6), transparent),
    radial-gradient(2px 2px at 700px 50px, rgba(200, 220, 255, 0.5), transparent),
    radial-gradient(1px 1px at 780px 160px, rgba(200, 220, 255, 0.7), transparent),
    radial-gradient(2px 2px at 850px 90px, rgba(200, 220, 255, 0.6), transparent),
    radial-gradient(1px 1px at 920px 240px, rgba(200, 220, 255, 0.8), transparent);
  background-repeat: repeat;
  background-size: 1000px 300px;
  animation: twinkle 4s ease-in-out infinite;
}

.stars.second {
  background-image:
    radial-gradient(1px 1px at 50px 100px, rgba(200, 220, 255, 0.4), transparent),
    radial-gradient(2px 2px at 120px 50px, rgba(200, 220, 255, 0.3), transparent),
    radial-gradient(1px 1px at 200px 150px, rgba(200, 220, 255, 0.5), transparent),
    radial-gradient(2px 2px at 280px 80px, rgba(200, 220, 255, 0.3), transparent),
    radial-gradient(1px 1px at 360px 200px, rgba(200, 220, 255, 0.4), transparent),
    radial-gradient(2px 2px at 440px 120px, rgba(200, 220, 255, 0.3), transparent),
    radial-gradient(1px 1px at 520px 60px, rgba(200, 220, 255, 0.5), transparent),
    radial-gradient(2px 2px at 600px 180px, rgba(200, 220, 255, 0.3), transparent),
    radial-gradient(1px 1px at 680px 140px, rgba(200, 220, 255, 0.4), transparent),
    radial-gradient(2px 2px at 760px 40px, rgba(200, 220, 255, 0.3), transparent),
    radial-gradient(1px 1px at 840px 100px, rgba(200, 220, 255, 0.5), transparent);
  background-repeat: repeat;
  background-size: 900px 250px;
  animation: twinkle 5s ease-in-out infinite;
  animation-delay: 1s;
  opacity: 0.6;
}

@keyframes twinkle {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 深色模式 */
.app.dark {
  background: linear-gradient(135deg, #0a0f1a 0%, #1a1a2e 50%, #16213e 100%);
  color: #f1f5f9;
}

.app.dark::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at top left, rgba(30, 64, 175, 0.1) 0%, transparent 50%),
              radial-gradient(ellipse at bottom right, rgba(59, 130, 246, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.main-content {
  position: relative;
  z-index: 1;
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
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 999;
  font-size: 24px;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 卡片样式 */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  padding: 24px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.app.dark .card {
  background: #1e293b;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #334155;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
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
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(30, 64, 175, 0.4);
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
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app.dark h1, .app.dark h2, .app.dark h3, .app.dark h4, .app.dark h5, .app.dark h6 {
  background: linear-gradient(135deg, #60a5fa, #93c5fd);
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
