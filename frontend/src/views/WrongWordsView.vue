<template>
  <div class="wrong-words">
    <h1>错题本</h1>

    <div v-if="wrongWords.length > 0" class="wrong-words-list">
      <div class="card animate-fade-in" style="animation-delay: 0.1s">
        <h2>我的错题</h2>
        <div class="words-grid">
          <div v-for="word in wrongWords" :key="word.id" class="word-card">
            <div class="word-info">
              <h3>{{ word.word }}</h3>
              <p class="phonetic">{{ word.phonetic }}</p>
              <p class="meaning">{{ word.meaning }}</p>
              <div class="stats-grid">
                <div class="stat-item wrong">
                  <span class="stat-label">错误</span>
                  <span class="stat-value">{{ word.wrong_count }}</span>
                </div>
                <div class="stat-item correct">
                  <span class="stat-label">正确</span>
                  <span class="stat-value">{{ word.correct_count || 0 }}</span>
                </div>
              </div>
              <p class="last-wrong">最后错误: {{ formatDate(word.last_wrong_date) }}</p>
              <p class="next-review">下次复习: {{ getNextReviewTime(word) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="review-section card animate-fade-in" style="animation-delay: 0.2s">
        <h2>复习计划</h2>
        <p class="review-info">根据艾宾浩斯遗忘曲线安排您的复习时间</p>
        <button @click="startReview" class="btn btn-primary">开始复习</button>
      </div>
    </div>

    <div v-else class="empty-message card animate-fade-in">
      <div class="icon">📚</div>
      <p>暂无错题记录</p>
      <p class="hint">完成测试后，答错的题目会自动添加到这里</p>
    </div>

    <!-- 复习测试 -->
    <div v-if="isReviewing" class="review-test card animate-fade-in">
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
        <div class="icon">🎉</div>
        <h3>复习完成！</h3>
        <p>本次复习了 {{ reviewedWords.length }} 个单词</p>
        <button @click="finishReview" class="btn btn-primary">结束复习</button>
      </div>
    </div>

    <div class="wrong-words-buttons card animate-fade-in" style="animation-delay: 0.3s">
      <router-link to="/" class="btn btn-secondary">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTestStore } from '../stores/test'
import { useUserStore } from '../stores/user'

const testStore = useTestStore()
const userStore = useUserStore()
const wrongWords = ref([])

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

const reviewIntervals = [1, 2, 4, 7, 15, 30]

const getNextReviewTime = (word) => {
  const correctCount = word.correct_count || 0
  const lastReview = new Date(word.last_correct_date || word.last_wrong_date)
  const intervalIndex = Math.min(correctCount, reviewIntervals.length - 1)
  const interval = reviewIntervals[intervalIndex]
  const nextReview = new Date(lastReview)
  nextReview.setDate(nextReview.getDate() + interval)
  return nextReview.toLocaleString()
}

const shouldReview = (word) => {
  const nextReviewTime = new Date(getNextReviewTime(word))
  return nextReviewTime <= new Date()
}

const loadWrongWords = async () => {
  if (userStore.token) {
    try {
      wrongWords.value = await testStore.getWrongWords(userStore.token)
    } catch (error) {
      console.error('Error loading wrong words:', error)
    }
  }
}

const startReview = () => {
  reviewWords.value = wrongWords.value.filter(shouldReview)
  reviewedWords.value = []
  isReviewing.value = true
  loadNextReviewWord()
}

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

const generateReviewOptions = () => {
  if (!currentReviewWord.value) return

  const correctAnswer = currentReviewWord.value.meaning

  const otherWords = wrongWords.value.filter(word => word.word !== currentReviewWord.value.word)
  const distractors = []

  for (let i = 0; i < 5 && i < otherWords.length; i++) {
    distractors.push(otherWords[i].meaning)
  }

  reviewOptions.value = [correctAnswer, ...distractors]

  for (let i = reviewOptions.value.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[reviewOptions.value[i], reviewOptions.value[j]] = [reviewOptions.value[j], reviewOptions.value[i]]
  }

  correctReviewIndex.value = reviewOptions.value.indexOf(correctAnswer)
}

const submitReviewAnswer = async (index) => {
  if (isReviewAnswered.value) return

  isReviewAnswered.value = true
  selectedReviewAnswer.value = index

  const isCorrect = index === correctReviewIndex.value

  if (userStore.token) {
    try {
      console.log('Review answer submitted:', { word: currentReviewWord.value.word, isCorrect })
    } catch (error) {
      console.error('Error submitting review answer:', error)
    }
  }

  reviewedWords.value.push({ ...currentReviewWord.value, isCorrect })

  setTimeout(() => {
    loadNextReviewWord()
  }, 1500)
}

const finishReview = () => {
  isReviewing.value = false
  currentReviewWord.value = null
  reviewOptions.value = []
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
  padding: 20px;
}

.wrong-words h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.wrong-words h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.words-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.word-card {
  background-color: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #ef4444;
  transition: all 0.3s ease;
}

.word-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.word-info h3 {
  margin-bottom: 8px;
  font-size: 20px;
  font-weight: 700;
}

.phonetic {
  color: #64748b;
  font-style: italic;
  margin-bottom: 12px;
  font-size: 14px;
}

.meaning {
  margin-bottom: 16px;
  color: #1e293b;
  font-size: 14px;
  line-height: 1.5;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
  background-color: white;
  border-radius: 8px;
}

.stat-item.wrong {
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.stat-item.correct {
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
}

.stat-item.wrong .stat-value {
  color: #ef4444;
}

.stat-item.correct .stat-value {
  color: #10b981;
}

.last-wrong, .next-review {
  color: #64748b;
  font-size: 12px;
  margin-bottom: 4px;
}

.next-review {
  color: #165DFF;
  font-weight: 600;
}

.empty-message {
  text-align: center;
  padding: 60px 20px;
}

.empty-message .icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-message p {
  font-size: 18px;
  color: #64748b;
  margin-bottom: 12px;
}

.empty-message .hint {
  font-size: 14px;
  color: #94a3b8;
}

.review-section {
  text-align: center;
  padding: 30px;
  margin-top: 24px;
}

.review-info {
  color: #64748b;
  margin-bottom: 20px;
  font-size: 14px;
}

.review-test {
  margin-top: 24px;
  padding: 30px;
}

.review-question {
  text-align: center;
}

.review-question h3 {
  font-size: 32px;
  margin-bottom: 12px;
  font-weight: 700;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.review-complete {
  text-align: center;
  padding: 40px 0;
}

.review-complete .icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.review-complete h3 {
  font-size: 24px;
  margin-bottom: 12px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 30px;
}

.option {
  width: 100%;
  text-align: left;
  padding: 16px 20px;
  background-color: #f8fafc;
  color: #1e293b;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 16px;
  font-weight: 500;
}

.option:hover {
  background-color: #f1f5f9;
  border-color: #165DFF;
  transform: translateY(-2px);
}

.option.correct {
  background: linear-gradient(135deg, #10b981, #34d399);
  color: white;
  border-color: #10b981;
}

.option.incorrect {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: white;
  border-color: #ef4444;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.wrong-words-buttons {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding: 20px;
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
  .wrong-words {
    padding: 16px;
  }

  .wrong-words h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .words-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .review-test {
    padding: 20px;
  }

  .review-question h3 {
    font-size: 24px;
  }

  .options {
    gap: 10px;
  }

  .option {
    padding: 14px 16px;
    font-size: 14px;
  }

  .wrong-words-buttons {
    flex-direction: column;
    align-items: center;
  }

  .wrong-words-buttons .btn {
    width: 200px;
  }
}
</style>
