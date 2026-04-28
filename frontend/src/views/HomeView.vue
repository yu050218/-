<template>
  <div class="home">
    <h1>词小记</h1>
    <div class="features">
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.1s">
        <div class="feature-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <h2>词汇测试</h2>
        <p>测试你的词汇量，获得详细的评估报告</p>
        <router-link to="/test" class="btn btn-primary">开始测试</router-link>
      </div>
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.2s">
        <div class="feature-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 16a4 4 0 0 1-.88-7.903A5 5 0 1 1 15.9 6L16 6a5 5 0 0 1 1 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
        </div>
        <h2>单词PK对战</h2>
        <p>与其他用户实时对战，检验你的词汇水平</p>
        <router-link to="/pk" class="btn btn-primary">开始对战</router-link>
      </div>
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.3s">
        <div class="feature-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <h2>错题本</h2>
        <p>记录错题，复习巩固，基于艾宾浩斯遗忘曲线</p>
        <router-link to="/wrong-words" class="btn btn-primary" v-if="userStore.isLoggedIn">查看错题</router-link>
        <router-link to="/login" class="btn btn-secondary" v-else>登录后查看</router-link>
      </div>
      <div class="feature-card card animate-fade-in" style="animation-delay: 0.4s">
        <div class="feature-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="6" width="15" height="14" rx="2"/>
            <path d="M17 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-2"/>
            <path d="M7 10l5 2 5-2"/>
          </svg>
        </div>
        <h2>单词卡片</h2>
        <p>抽认卡模式学习单词，轻松记忆</p>
        <router-link to="/cards" class="btn btn-primary" v-if="userStore.isLoggedIn">开始学习</router-link>
        <router-link to="/login" class="btn btn-secondary" v-else>登录后学习</router-link>
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
  max-width: 1200px;
  margin: 0 auto;
}

.home h1 {
  font-size: 48px;
  margin-bottom: 60px;
  font-weight: 800;
}

.features {
  display: flex;
  justify-content: center;
  margin-bottom: 60px;
  flex-wrap: wrap;
  gap: 30px;
}

.feature-card {
  width: 340px;
  margin: 10px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.1), rgba(59, 130, 246, 0.1));
  color: #1e40af;
  transition: all 0.3s ease;
}

.app.dark .feature-icon {
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.1), rgba(147, 197, 253, 0.1));
  color: #60a5fa;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-card h2 {
  font-size: 24px;
  margin-bottom: 16px;
}

.feature-card p {
  margin-bottom: 30px;
  font-size: 16px;
  line-height: 1.6;
  color: #64748b;
}

.app.dark .feature-card p {
  color: #94a3b8;
}

.user-stats {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 32px;
}

.user-stats h2 {
  font-size: 24px;
  margin-bottom: 12px;
}

.stats-hint {
  color: #64748b;
  font-size: 14px;
}

.app.dark .stats-hint {
  color: #94a3b8;
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

  .user-stats {
    padding: 24px;
  }
}
</style>
