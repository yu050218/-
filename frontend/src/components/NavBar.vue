<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="navbar-container">
      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">📚</span>
          <span class="brand-text">词汇评估工具</span>
        </router-link>
      </div>

      <button class="navbar-toggle" @click="isMenuOpen = !isMenuOpen">
        <span class="toggle-icon">{{ isMenuOpen ? '✕' : '☰' }}</span>
      </button>

      <div class="navbar-menu" :class="{ 'active': isMenuOpen }">
        <div class="nav-links">
          <router-link to="/" class="nav-link" @click="isMenuOpen = false">
            <span class="link-icon">🏠</span>
            <span class="link-text">首页</span>
          </router-link>

          <router-link to="/test" class="nav-link" @click="isMenuOpen = false">
            <span class="link-icon">📝</span>
            <span class="link-text">词汇测试</span>
          </router-link>

          <router-link to="/pk" class="nav-link" @click="isMenuOpen = false">
            <span class="link-icon">⚔️</span>
            <span class="link-text">PK对战</span>
          </router-link>

          <router-link to="/wrong-words" class="nav-link" @click="isMenuOpen = false" v-if="userStore.isLoggedIn">
            <span class="link-icon">📋</span>
            <span class="link-text">错题本</span>
          </router-link>

          <router-link to="/profile" class="nav-link" @click="isMenuOpen = false" v-if="userStore.isLoggedIn">
            <span class="link-icon">👤</span>
            <span class="link-text">个人中心</span>
          </router-link>

          <router-link to="/admin" class="nav-link admin-link" @click="isMenuOpen = false" v-if="userStore.isAdmin">
            <span class="link-icon">⚙️</span>
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.navbar.scrolled {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
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
  font-size: 28px;
}

.brand-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
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
  font-size: 24px;
  color: #1e293b;
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

.nav-link:hover {
  color: #165DFF;
  background: rgba(22, 93, 255, 0.05);
}

.nav-link.router-link-active {
  color: #165DFF;
  background: rgba(22, 93, 255, 0.1);
}

.link-icon {
  font-size: 18px;
}

.admin-link {
  color: #f59e0b;
}

.admin-link:hover {
  color: #d97706;
  background: rgba(245, 158, 11, 0.1);
}

.admin-link.router-link-active {
  color: #d97706;
  background: rgba(245, 158, 11, 0.15);
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
  background: #f8fafc;
  border-radius: 8px;
}

.username {
  font-weight: 600;
  color: #1e293b;
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
  background: #f8fafc;
  color: #165DFF;
}

.btn-login:hover {
  background: #e2e8f0;
}

.btn-register {
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  color: white;
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 93, 255, 0.3);
}

.btn-logout {
  background: #fef2f2;
  color: #ef4444;
  padding: 10px 16px;
}

.btn-logout:hover {
  background: #fee2e2;
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
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    display: none;
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
