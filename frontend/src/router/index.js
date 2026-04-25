import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('../views/TestView.vue')
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/ReportView.vue')
  },
  {
    path: '/pk',
    name: 'PK',
    component: () => import('../views/PKView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue')
  },
  {
    path: '/wrong-words',
    name: 'WrongWords',
    component: () => import('../views/WrongWordsView.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/AdminView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否访问管理员页面
  if (to.path === '/admin') {
    // 检查用户是否登录且是管理员
    if (userStore.isLoggedIn && userStore.isAdmin) {
      next()
    } else {
      // 重定向到登录页面
      next('/login')
    }
  } else {
    next()
  }
})

export default router