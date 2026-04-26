<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="navbar-container">
      <div class="navbar-brand">
      <router-link to="/" class="brand-link">
        <span class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
        </span>
        <span class="brand-text">词汇评估工具</span>
      </router-link>
    </div>

    <button class="navbar-toggle" @click="isMenuOpen = !isMenuOpen">
      <span class="toggle-icon">
        <svg v-if="isMenuOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </span>
    </button>

    <div class="navbar-menu" :class="{ 'active': isMenuOpen }">
      <div class="nav-links">
        <router-link to="/" class="nav-link" @click="isMenuOpen = false">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </span>
          <span class="link-text">首页</span>
        </router-link>

        <router-link to="/test" class="nav-link" @click="isMenuOpen = false">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </span>
          <span class="link-text">词汇测试</span>
        </router-link>

        <router-link to="/pk" class="nav-link" @click="isMenuOpen = false">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M7 16a4 4 0 0 1-.88-7.903A5 5 0 1 1 15.9 6L16 6a5 5 0 0 1 1 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </span>
          <span class="link-text">PK对战</span>
        </router-link>

        <router-link to="/wrong-words" class="nav-link" @click="isMenuOpen = false" v-if="userStore.isLoggedIn">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </span>
          <span class="link-text">错题本</span>
        </router-link>

        <router-link to="/profile" class="nav-link" @click="isMenuOpen = false" v-if="userStore.isLoggedIn">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </span>
          <span class="link-text">个人中心</span>
        </router-link>

        <router-link to="/admin" class="nav-link admin-link" @click="isMenuOpen = false" v-if="userStore.isAdmin">
          <span class="link-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
          </span>
          <span class="link-text">后台管理</span>
        </router-link>
        </div>

        <div class="nav-auth">
          <template v-if="userStore.isLoggedIn">
            <div class="user-info">
              <span class="username">{{ userStore.user?.username }}</span>
            </div>
            <button @click="handleLogout" class="btn btn-logout">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-login" @click="isMenuOpen = false">登录</router-link>
            <router-link to="/register" class="btn btn-register" @click="isMenuOpen = false">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const isMenuOpen = ref(false)
const isScrolled = ref(false)

const handleLogout = () => {
  userStore.logout()
  isMenuOpen.value = false
  window.location.reload()
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.app.dark .navbar {
  background: rgba(10, 15, 26, 0.95);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.navbar.scrolled {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.app.dark .navbar.scrolled {
  background: rgba(10, 15, 26, 1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.navbar-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.brand-link:hover {
  transform: scale(1.02);
}

.brand-icon {
  color: #1e40af;
}

.app.dark .brand-icon {
  color: #60a5fa;
}

.brand-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app.dark .brand-text {
  background: linear-gradient(135deg, #60a5fa, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-toggle {
  display: none;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
}

.toggle-icon {
  color: #1e293b;
}

.app.dark .toggle-icon {
  color: #f1f5f9;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  text-decoration: none;
  color: #64748b;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.app.dark .nav-link {
  color: #94a3b8;
}

.nav-link:hover {
  color: #1e40af;
  background: rgba(30, 64, 175, 0.05);
}

.app.dark .nav-link:hover {
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
}

.nav-link.router-link-active {
  color: #1e40af;
  background: rgba(30, 64, 175, 0.1);
}

.app.dark .nav-link.router-link-active {
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.15);
}

.link-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.admin-link {
  color: #f59e0b;
}

.app.dark .admin-link {
  color: #fbbf24;
}

.admin-link:hover {
  color: #d97706;
  background: rgba(245, 158, 11, 0.1);
}

.app.dark .admin-link:hover {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.15);
}

.admin-link.router-link-active {
  color: #d97706;
  background: rgba(245, 158, 11, 0.15);
}

.app.dark .admin-link.router-link-active {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.2);
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f1f5f9;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.app.dark .user-info {
  background: #1e293b;
  border: 1px solid #334155;
}

.username {
  font-weight: 600;
  color: #1e293b;
}

.app.dark .username {
  color: #f1f5f9;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-login {
  background: #f1f5f9;
  color: #1e40af;
  border: 1px solid #e2e8f0;
}

.app.dark .btn-login {
  background: #1e293b;
  color: #60a5fa;
  border: 1px solid #334155;
}

.btn-login:hover {
  background: #e2e8f0;
}

.app.dark .btn-login:hover {
  background: #334155;
}

.btn-register {
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.btn-logout {
  background: #fef2f2;
  color: #ef4444;
  padding: 10px 16px;
  border: 1px solid #fee2e2;
}

.app.dark .btn-logout {
  background: #3f1f1f;
  color: #fca5a5;
  border: 1px solid #582c2c;
}

.btn-logout:hover {
  background: #fee2e2;
}

.app.dark .btn-logout:hover {
  background: #582c2c;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-container {
    height: 60px;
    padding: 0 16px;
  }

  .brand-text {
    font-size: 16px;
  }

  .navbar-toggle {
    display: block;
  }

  .navbar-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    flex-direction: column;
    background: white;
    padding: 20px;
    gap: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    display: none;
  }

  .app.dark .navbar-menu {
    background: #1e293b;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .navbar-menu.active {
    display: flex;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 4px;
  }

  .nav-link {
    width: 100%;
    padding: 14px 16px;
    justify-content: flex-start;
  }

  .nav-auth {
    flex-direction: column;
    width: 100%;
    gap: 12px;
    padding-top: 16px;
    border-top: 1px solid #e2e8f0;
  }

  .app.dark .nav-auth {
    border-top: 1px solid #334155;
  }

  .user-info {
    width: 100%;
    justify-content: center;
  }

  .btn {
    width: 100%;
    text-align: center;
  }
}
</style>
