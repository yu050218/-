<template>
  <div class="wrong-words">
    <h1>错题本</h1>
    
    <div v-if="wrongWords.length > 0" class="wrong-words-list">
      <h2>我的错题</h2>
      <div class="words-grid">
        <div v-for="word in wrongWords" :key="word.id" class="word-card">
          <div class="word-info">
            <h3>{{ word.word }}</h3>
            <p class="phonetic">{{ word.phonetic }}</p>
            <p class="meaning">{{ word.meaning }}</p>
            <p class="wrong-count">错误次数: {{ word.wrong_count }}</p>
            <p class="correct-count">正确次数: {{ word.correct_count || 0 }}</p>
            <p class="last-wrong">最后错误: {{ formatDate(word.last_wrong_date) }}</p>
            <p class="next-review">下次复习: {{ getNextReviewTime(word) }}</p>
          </div>
        </div>
      </div>
      <div class="review-section">
        <h2>复习计划</h2>
        <button @click="startReview" class="btn">开始复习</button>
      </div>
    </div>
    
    <div v-else class="empty-message">
      <p>暂无错题记录</p>
    </div>
    
    <!-- 复习测试 -->
    <div v-if="isReviewing" class="review-test">
      <h2>复习测试</h2>
      <div v-if="currentReviewWord" class="review-question">
        <h3>{{ currentReviewWord.word }}</h3>
        <p class="phonetic">{{ currentReviewWord.phonetic }}</p>
        <div class="options">
          <button 
            v-for="(option, index) in reviewOptions" 
            :key="index"
            @click="submitReviewAnswer(index)"
            :class="['btn', 'option', { 'correct': isReviewAnswered && index === correctReviewIndex, 'incorrect': isReviewAnswered && index === selectedReviewAnswer && index !== correctReviewIndex }]"
            :disabled="isReviewAnswered"
          >
            {{ option }}
          </button>
        </div>
      </div>
      <div v-else class="review-complete">
        <h3>复习完成！</h3>
        <p>本次复习了 {{ reviewedWords.length }} 个单词</p>
        <button @click="finishReview" class="btn">结束复习</button>
      </div>
    </div>
    
    <div class="wrong-words-buttons">
      <router-link to="/" class="btn">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTestStore } from '../stores/test'
import { useUserStore } from '../stores/user'

const testStore = useTestStore()
const userStore = useUserStore()
const wrongWords = ref([])

// 复习相关状态
const isReviewing = ref(false)
const currentReviewWord = ref(null)
const reviewOptions = ref([])
const correctReviewIndex = ref(0)
const isReviewAnswered = ref(false)
const selectedReviewAnswer = ref(null)
const reviewWords = ref([])
const reviewedWords = ref([])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 艾宾浩斯遗忘曲线的复习间隔（天）
const reviewIntervals = [1, 2, 4, 7, 15, 30]

// 计算下次复习时间
const getNextReviewTime = (word) => {
  const correctCount = word.correct_count || 0
  const lastReview = new Date(word.last_correct_date || word.last_wrong_date)
  const intervalIndex = Math.min(correctCount, reviewIntervals.length - 1)
  const interval = reviewIntervals[intervalIndex]
  const nextReview = new Date(lastReview)
  nextReview.setDate(nextReview.getDate() + interval)
  return nextReview.toLocaleString()
}

// 检查是否需要复习
const shouldReview = (word) => {
  const nextReviewTime = new Date(getNextReviewTime(word))
  return nextReviewTime <= new Date()
}

// 加载错题
const loadWrongWords = async () => {
  if (userStore.token) {
    try {
      wrongWords.value = await testStore.getWrongWords(userStore.token)
    } catch (error) {
      console.error('Error loading wrong words:', error)
    }
  }
}

// 开始复习
const startReview = () => {
  // 筛选需要复习的单词
  reviewWords.value = wrongWords.value.filter(shouldReview)
  reviewedWords.value = []
  isReviewing.value = true
  loadNextReviewWord()
}

// 加载下一个复习单词
const loadNextReviewWord = () => {
  if (reviewWords.value.length > 0) {
    currentReviewWord.value = reviewWords.value.shift()
    generateReviewOptions()
    isReviewAnswered.value = false
    selectedReviewAnswer.value = null
  } else {
    currentReviewWord.value = null
  }
}

// 生成复习选项
const generateReviewOptions = () => {
  if (!currentReviewWord.value) return
  
  // 正确答案
  const correctAnswer = currentReviewWord.value.meaning
  
  // 生成干扰选项（从其他错题中随机选择）
  const otherWords = wrongWords.value.filter(word => word.word !== currentReviewWord.value.word)
  const distractors = []
  
  for (let i = 0; i < 5 && i < otherWords.length; i++) {
    distractors.push(otherWords[i].meaning)
  }
  
  // 组合选项并打乱顺序
  reviewOptions.value = [correctAnswer, ...distractors]
  
  // 随机打乱选项
  for (let i = reviewOptions.value.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[reviewOptions.value[i], reviewOptions.value[j]] = [reviewOptions.value[j], reviewOptions.value[i]]
  }
  
  // 记录正确选项的索引
  correctReviewIndex.value = reviewOptions.value.indexOf(correctAnswer)
}

// 提交复习答案
const submitReviewAnswer = async (index) => {
  if (isReviewAnswered.value) return
  
  isReviewAnswered.value = true
  selectedReviewAnswer.value = index
  
  // 检查答案是否正确
  const isCorrect = index === correctReviewIndex.value
  
  // 模拟提交答案到后端
  // 实际项目中应该调用后端API来更新错题本
  if (userStore.token) {
    try {
      // 这里应该调用后端API来更新错题本
      // 暂时模拟成功
      console.log('Review answer submitted:', { word: currentReviewWord.value.word, isCorrect })
    } catch (error) {
      console.error('Error submitting review answer:', error)
    }
  }
  
  // 记录已复习的单词
  reviewedWords.value.push({ ...currentReviewWord.value, isCorrect })
  
  // 延迟加载下一个单词
  setTimeout(() => {
    loadNextReviewWord()
  }, 1500)
}

// 结束复习
const finishReview = () => {
  isReviewing.value = false
  currentReviewWord.value = null
  reviewOptions.value = []
  // 重新加载错题本
  loadWrongWords()
}

onMounted(async () => {
  await loadWrongWords()
})
</script>

<style scoped>
.wrong-words {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.wrong-words h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.wrong-words h2 {
  margin-bottom: 20px;
  color: #666;
}

.words-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.word-card {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #f44336;
}

.word-info h3 {
  margin-bottom: 5px;
  color: #333;
}

.phonetic {
  color: #999;
  font-style: italic;
  margin-bottom: 10px;
}

.meaning {
  margin-bottom: 10px;
  color: #666;
}

.wrong-count {
  margin-bottom: 5px;
  color: #f44336;
  font-weight: bold;
}

.last-wrong {
  color: #999;
  font-size: 14px;
}

.empty-message {
  text-align: center;
  padding: 60px 0;
  color: #666;
  font-size: 18px;
}

.review-section {
  margin-top: 40px;
  text-align: center;
}

.review-test {
  margin-top: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  border-left: 4px solid #4CAF50;
}

.review-question {
  text-align: center;
}

.review-question h3 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.review-complete {
  text-align: center;
  padding: 40px 0;
}

.correct-count {
  margin-bottom: 5px;
  color: #4CAF50;
  font-weight: bold;
}

.next-review {
  color: #2196F3;
  font-size: 14px;
  margin-top: 10px;
}

.wrong-words-buttons {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.btn {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.btn:hover {
  background-color: #45a049;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.option {
  width: 100%;
  text-align: left;
  padding: 15px 20px;
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  transition: all 0.3s;
}

.option:hover {
  background-color: #e0e0e0;
  border-color: #4CAF50;
}

.option.correct {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.option.incorrect {
  background-color: #f44336;
  color: white;
  border-color: #f44336;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>