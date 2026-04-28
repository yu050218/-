<template>
  <div class="card-view">
    <h1>单词卡片</h1>

    <!-- 未登录状态 -->
    <div v-if="!userStore.isLoggedIn" class="not-logged-in card animate-fade-in">
      <div class="icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      <p>请先登录以使用单词卡片</p>
      <router-link to="/login" class="btn btn-primary">登录</router-link>
    </div>

    <!-- 已登录状态 -->
    <div v-else>
      <!-- 学习统计 -->
      <div class="stats card animate-fade-in">
        <div class="stat-item">
          <span class="stat-value">{{ currentIndex + 1 }}</span>
          <span class="stat-label">当前</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ words.length }}</span>
          <span class="stat-label">总数</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ correctCount }}</span>
          <span class="stat-label">正确</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">{{ wrongCount }}</span>
          <span class="stat-label">错误</span>
        </div>
      </div>

      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>

      <!-- 卡片区域 -->
      <div v-if="currentWord" class="card-container">
        <div 
          class="word-card" 
          :class="{ flipped: isFlipped, correct: lastResult === 'correct', wrong: lastResult === 'wrong' }"
          @click="flipCard"
        >
          <div class="card-face card-front">
            <div class="card-icon">📖</div>
            <h2>{{ currentWord.word }}</h2>
            <p class="phonetic">{{ currentWord.phonetic }}</p>
            <p class="hint">点击卡片查看释义</p>
          </div>
          <div class="card-face card-back">
            <div class="card-icon">💡</div>
            <h3>{{ currentWord.meaning }}</h3>
            <p class="difficulty">难度: {{ currentWord.difficulty }}</p>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <button 
          v-if="isFlipped" 
          @click="markWrong" 
          class="btn btn-wrong"
        >
          <span class="btn-icon">✗</span>
          <span>不认识</span>
        </button>
        <button 
          v-if="isFlipped" 
          @click="markCorrect" 
          class="btn btn-correct"
        >
          <span class="btn-icon">✓</span>
          <span>认识</span>
        </button>
        <button 
          v-if="!words.length" 
          @click="loadWords" 
          class="btn btn-primary"
        >
          开始学习
        </button>
      </div>

      <!-- 完成提示 -->
      <div v-if="showComplete" class="complete-card card animate-fade-in">
        <div class="complete-icon">🎉</div>
        <h2>学习完成！</h2>
        <p>本次学习 {{ correctCount + wrongCount }} 个单词</p>
        <p class="result-text">正确: {{ correctCount }} | 错误: {{ wrongCount }}</p>
        <p class="accuracy">正确率: {{ accuracyPercent }}%</p>
        <div class="complete-buttons">
          <button @click="restart" class="btn btn-primary">再学一遍</button>
          <router-link to="/wrong-words" class="btn btn-secondary">复习错题</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const userStore = useUserStore()

const words = ref([])
const currentIndex = ref(0)
const isFlipped = ref(false)
const lastResult = ref(null)
const correctCount = ref(0)
const wrongCount = ref(0)
const showComplete = ref(false)

const currentWord = computed(() => {
  return words.value[currentIndex.value] || null
})

const progressPercent = computed(() => {
  if (!words.value.length) return 0
  return ((currentIndex.value + 1) / words.value.length) * 100
})

const accuracyPercent = computed(() => {
  const total = correctCount.value + wrongCount.value
  if (total === 0) return 0
  return Math.round((correctCount.value / total) * 100)
})

const loadWords = async () => {
  try {
    const response = await axios.get('/api/test/wrong-words', {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    
    if (response.data.length > 0) {
      words.value = response.data
    } else {
      // 如果没有错题，加载所有单词
      const wordsResponse = await axios.get('/api/admin/word-bank', {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      })
      // 随机选择20个单词
      const allWords = wordsResponse.data
      const shuffled = allWords.sort(() => 0.5 - Math.random())
      words.value = shuffled.slice(0, 20)
    }
    
    currentIndex.value = 0
    correctCount.value = 0
    wrongCount.value = 0
    showComplete.value = false
    isFlipped.value = false
  } catch (error) {
    console.error('加载单词失败:', error)
  }
}

const flipCard = () => {
  if (!showComplete.value) {
    isFlipped.value = !isFlipped.value
  }
}

const markCorrect = () => {
  correctCount.value++
  lastResult.value = 'correct'
  nextWord()
}

const markWrong = () => {
  wrongCount.value++
  lastResult.value = 'wrong'
  
  // 将错题添加到错题本
  addToWrongWords()
  
  nextWord()
}

const addToWrongWords = async () => {
  if (!currentWord.value) return
  
  try {
    await axios.put('/api/test/review-submit', {
      word: currentWord.value.word,
      phonetic: currentWord.value.phonetic,
      meaning: currentWord.value.meaning,
      is_correct: false
    }, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
  } catch (error) {
    console.error('添加错题失败:', error)
  }
}

const nextWord = () => {
  setTimeout(() => {
    isFlipped.value = false
    lastResult.value = null
    
    if (currentIndex.value < words.value.length - 1) {
      currentIndex.value++
    } else {
      showComplete.value = true
    }
  }, 500)
}

const restart = () => {
  currentIndex.value = 0
  correctCount.value = 0
  wrongCount.value = 0
  showComplete.value = false
  isFlipped.value = false
  lastResult.value = null
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    loadWords()
  }
})
</script>

<style scoped>
.card-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.card-view h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 36px;
}

.not-logged-in {
  text-align: center;
  padding: 60px 20px;
}

.not-logged-in .icon {
  margin-bottom: 20px;
  color: #64748b;
}

.app.dark .not-logged-in .icon {
  color: #60a5fa;
}

.not-logged-in p {
  margin-bottom: 30px;
  font-size: 18px;
  color: #64748b;
}

.app.dark .not-logged-in p {
  color: #94a3b8;
}

.stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  padding: 20px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #165DFF;
}

.app.dark .stat-value {
  color: #60a5fa;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

.app.dark .stat-label {
  color: #94a3b8;
}

.stat-divider {
  width: 2px;
  height: 40px;
  background-color: #e2e8f0;
}

.app.dark .stat-divider {
  background-color: #334155;
}

.progress-bar {
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 30px;
  overflow: hidden;
}

.app.dark .progress-bar {
  background-color: #1e293b;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #165DFF, #0EA5E9);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.card-container {
  perspective: 1000px;
  margin-bottom: 30px;
}

.word-card {
  width: 100%;
  height: 350px;
  position: relative;
  transform-style: preserve-3d;
  cursor: pointer;
  transition: transform 0.6s ease;
}

.word-card.flipped {
  transform: rotateY(180deg);
}

.word-card.correct .card-face {
  border-color: #10b981;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.word-card.wrong .card-face {
  border-color: #ef4444;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px;
  background-color: white;
  border: 3px solid #e2e8f0;
  transition: all 0.3s ease;
}

.app.dark .card-face {
  background-color: #1e293b;
  border-color: #334155;
}

.card-front {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.app.dark .card-front {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
}

.card-back {
  transform: rotateY(180deg);
  background: linear-gradient(135deg, #165DFF 0%, #0EA5E9 100%);
  color: white;
}

.card-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.card-front h2 {
  font-size: 42px;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 12px;
}

.app.dark .card-front h2 {
  color: #f1f5f9;
}

.card-front .phonetic {
  color: #64748b;
  font-style: italic;
  font-size: 18px;
  margin-bottom: 20px;
}

.app.dark .card-front .phonetic {
  color: #94a3b8;
}

.card-front .hint {
  color: #94a3b8;
  font-size: 14px;
}

.app.dark .card-front .hint {
  color: #64748b;
}

.card-back h3 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 12px;
  text-align: center;
}

.card-back .difficulty {
  font-size: 16px;
  opacity: 0.8;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn-wrong,
.btn-correct {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-wrong {
  background-color: #fef2f2;
  color: #ef4444;
  border: 2px solid #fee2e2;
}

.btn-wrong:hover {
  background-color: #fee2e2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.app.dark .btn-wrong {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.app.dark .btn-wrong:hover {
  background-color: rgba(239, 68, 68, 0.2);
}

.btn-correct {
  background-color: #f0fdf4;
  color: #10b981;
  border: 2px solid #bbf7d0;
}

.btn-correct:hover {
  background-color: #bbf7d0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.app.dark .btn-correct {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border-color: rgba(16, 185, 129, 0.3);
}

.app.dark .btn-correct:hover {
  background-color: rgba(16, 185, 129, 0.2);
}

.btn-icon {
  font-size: 20px;
}

.complete-card {
  text-align: center;
  padding: 40px;
}

.complete-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.complete-card h2 {
  font-size: 32px;
  margin-bottom: 16px;
}

.complete-card p {
  font-size: 18px;
  color: #64748b;
  margin-bottom: 8px;
}

.app.dark .complete-card p {
  color: #94a3b8;
}

.result-text {
  font-weight: 600;
  color: #1e293b !important;
}

.app.dark .result-text {
  color: #f1f5f9 !important;
}

.accuracy {
  font-size: 24px !important;
  font-weight: 700;
  color: #165DFF !important;
  margin-bottom: 30px !important;
}

.complete-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
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
  .card-view {
    padding: 16px;
  }

  .card-view h1 {
    font-size: 28px;
    margin-bottom: 20px;
  }

  .stats {
    gap: 16px;
    padding: 16px;
  }

  .stat-value {
    font-size: 22px;
  }

  .stat-label {
    font-size: 12px;
  }

  .word-card {
    height: 300px;
  }

  .card-front h2 {
    font-size: 32px;
  }

  .card-back h3 {
    font-size: 22px;
  }

  .btn-wrong,
  .btn-correct {
    padding: 12px 24px;
    font-size: 14px;
  }

  .complete-card {
    padding: 30px 16px;
  }

  .complete-card h2 {
    font-size: 24px;
  }
}
</style>