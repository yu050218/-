<template>
  <div class="home">
    <h1>词汇评估工具</h1>
    <div class="features">
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.1s">
        <div class="feature-icon">📚</div>
        <h2>词汇测试</h2>
        <p>测试你的词汇量，获得详细的评估报告</p>
        <router-link to="/test" class="btn btn-primary">开始测试</router-link>
      </div>
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.2s">
        <div class="feature-icon">⚔️</div>
        <h2>单词PK对战</h2>
        <p>与其他用户实时对战，检验你的词汇水平</p>
        <router-link to="/pk" class="btn btn-primary">开始对战</router-link>
      </div>
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.3s">
        <div class="feature-icon">📋</div>
        <h2>错题本</h2>
        <p>记录错题，复习巩固，基于艾宾浩斯遗忘曲线</p>
        <router-link to="/wrong-words" class="btn btn-primary" v-if="userStore.isLoggedIn">查看错题</router-link>
        <router-link to="/login" class="btn btn-secondary" v-else>登录后查看</router-link>
      </div>
    </div>

    <div v-if="userStore.isLoggedIn" class="user-stats card animate-fade-in" style="animation-delay: 0.4s">
      <h2>欢迎回来，{{ userStore.user?.username }}</h2>
      <p class="stats-hint">通过顶部导航栏快速访问各项功能</p>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
</script>

<style scoped>
.home {
  text-align: center;
  padding: 40px 0;
}

.home h1 {
  font-size: 48px;
  margin-bottom: 60px;
  font-weight: 800;
}

.features {
  display: flex;
  justify-content: space-around;
  margin-bottom: 60px;
  flex-wrap: wrap;
  gap: 30px;
}

.feature-card {
  width: 320px;
  margin: 10px;
  position: relative;
  overflow: hidden;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

.feature-card h2 {
  font-size: 24px;
  margin-bottom: 16px;
}

.feature-card p {
  margin-bottom: 30px;
  font-size: 16px;
  line-height: 1.6;
}

.user-stats {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.user-stats h2 {
  font-size: 24px;
  margin-bottom: 12px;
}

.stats-hint {
  color: #64748b;
  font-size: 14px;
}

/* 动画效果 */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

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
  .home {
    padding: 30px 0;
  }

  .home h1 {
    font-size: 36px;
    margin-bottom: 40px;
  }

  .features {
    gap: 20px;
  }

  .feature-card {
    width: 100%;
    max-width: 320px;
  }
}
</style>
