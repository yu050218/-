<template>
  <div class="test">
    <h1>词汇测试</h1>
    
    <!-- 开始测试按钮 -->
    <div v-if="!testStore.sessionId && !testStore.testResult" class="test-start card animate-fade-in">
      <h2>开始词汇测试</h2>
      <p>本次测试共50道题，包含小学、初中、高中各难度级别</p>
      <button @click="startTest('50')" class="btn btn-primary">开始测试</button>
    </div>
    
    <!-- 测试进行中 -->
    <div v-else-if="testStore.currentWord" class="test-progress card animate-fade-in">
      <div class="progress-bar">
        <div class="progress" :style="{ width: (testStore.currentQuestion / testStore.totalQuestions) * 100 + '%' }"></div>
      </div>
      <div class="test-stats">
        <div class="stat-item">
          <span class="stat-label">错题数:</span>
          <span class="stat-value wrong">{{ testStore.totalWrong || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">连续错题:</span>
          <span class="stat-value consecutive-wrong">{{ testStore.consecutiveWrong || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">用时:</span>
          <span class="stat-value timer">{{ formatTime(elapsedTime) }}</span>
        </div>
      </div>
      <div class="question">
        <h3>第 {{ testStore.currentQuestion }} / {{ testStore.totalQuestions }} 题</h3>
        <div class="word-info">
          <h2>{{ testStore.currentWord.word }}</h2>
            <div class="phonetic-container">
              <p class="phonetic">{{ testStore.currentWord.phonetic }}</p>
              <button @click="playPronunciation" class="btn phonetic-btn">🔊</button>
            </div>
        </div>
        <div class="options">
          <button 
            v-for="(option, index) in testStore.currentWord.options" 
            :key="index"
            @click="submitAnswer(index)"
            :class="['btn', 'option', { 'correct': isAnswered && index === correctIndex, 'incorrect': isAnswered && index === selectedAnswer && index !== correctIndex }]"
            :disabled="isAnswered"
          >
            {{ option }}
          </button>
        </div>
        <div class="unknown-button">
          <button @click="submitAnswer('unknown')" class="btn unknown" :disabled="isAnswered">不认识</button>
        </div>
      </div>
    </div>
    
    <!-- 测试结果 -->
    <div v-else-if="testStore.testResult" class="test-result card animate-fade-in">
      <h2>测试结果</h2>
      <div class="result-info">
        <p>答对: {{ testStore.testResult.correct_count }} / {{ testStore.testResult.total_count }}</p>
        <p>正确率: {{ (testStore.testResult.correct_rate * 100).toFixed(1) }}%</p>
        <p>词汇量: {{ testStore.testResult.vocabulary_size }}</p>
        <p>等级: {{ testStore.testResult.level }}</p>
        <p>教育水平: {{ testStore.testResult.education_level }}</p>
        <div class="suggestions">
          <h4>学习建议:</h4>
          <ul>
            <li v-for="(suggestion, index) in testStore.testResult.study_suggestions" :key="index">
              {{ suggestion }}
            </li>
          </ul>
        </div>
      </div>
      <div class="result-buttons">
        <button @click="resetTest" class="btn btn-secondary">再测一次</button>
        <router-link to="/report" class="btn btn-primary">查看报告</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useTestStore } from '../stores/test'
import { useRouter } from 'vue-router'

const testStore = useTestStore()
const router = useRouter()
const isAnswered = ref(false)
const isCorrect = ref(false)
const selectedAnswer = ref(null)
const correctIndex = ref(null)
const elapsedTime = ref(0)
let timer = null

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const startTimer = () => {
  stopTimer()
  elapsedTime.value = 0
  timer = setInterval(() => {
    elapsedTime.value++
  }, 1000)
}

const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

onUnmounted(() => {
  stopTimer()
})

// 组件挂载时重置测试结果，确保不显示上一次的报告
onMounted(() => {
  console.log('Component mounted, testStore:', testStore)
  testStore.testResult = null
  testStore.sessionId = null
  testStore.currentWord = null
  testStore.totalWrong = 0
  testStore.consecutiveWrong = 0
  localStorage.removeItem('testSessionId')
  console.log('After reset, testStore.sessionId:', testStore.sessionId)
  console.log('After reset, testStore.currentWord:', testStore.currentWord)
})

// 监听 testStore 的变化
watch(() => testStore.currentWord, (newValue) => {
  console.log('testStore.currentWord changed:', newValue)
})

watch(() => testStore.sessionId, (newValue) => {
  console.log('testStore.sessionId changed:', newValue)
})

// 监听currentWord变化，重置状态
watch(() => testStore.currentWord, () => {
  isAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = null
  correctIndex.value = null
})

const startTest = async (testType) => {
  try {
    console.log('Starting test...')
    // 重置测试结果，确保不显示上一次的报告
    testStore.testResult = null
    isAnswered.value = false
    isCorrect.value = false
    selectedAnswer.value = null
    correctIndex.value = null
    testStore.totalWrong = 0
    testStore.consecutiveWrong = 0
    // 启动计时器
    startTimer()
    console.log('Calling testStore.startTest...')
    await testStore.startTest(testType)
    console.log('Test started successfully, currentWord:', testStore.currentWord)
  } catch (error) {
    console.error('Error starting test:', error)
    stopTimer()
  }
}

const submitAnswer = async (answer) => {
  try {
    // 检查是否有当前单词
    if (!testStore.currentWord) {
      console.error('No current word to answer')
      return
    }
    
    selectedAnswer.value = answer
    correctIndex.value = testStore.currentWord.correct_index
    isAnswered.value = true
    
    // 设置30秒的请求超时
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Request timeout')), 30000)
    })
    
    const response = await Promise.race([
      testStore.submitAnswer(testStore.currentWord.word, answer),
      timeoutPromise
    ])
    
    if (response.question) {
      // 有下一个问题
      isCorrect.value = response.is_correct
      
      // 更新错题数和连续错题数
      if (response.total_wrong !== undefined) {
        testStore.totalWrong = response.total_wrong
      }
      if (response.consecutive_wrong !== undefined) {
        testStore.consecutiveWrong = response.consecutive_wrong
      }
      
      // 延迟500毫秒后进入下一题
      setTimeout(() => {
        isAnswered.value = false
        selectedAnswer.value = null
        correctIndex.value = null
      }, 500)
    } else {
      // 测试完成，跳转到报告页面
      isAnswered.value = true
      isCorrect.value = true // 显示正确答案的样式
      
      setTimeout(() => {
        router.push('/report')
      }, 1500)
    }
  } catch (error) {
    console.error('Error submitting answer:', error)
    // 重置状态，避免卡死
    isAnswered.value = false
    selectedAnswer.value = null
    correctIndex.value = null
    
    // 如果是会话无效错误，重置测试
    if (error.message === 'Invalid session ID') {
      console.log('Session expired, resetting test')
      testStore.resetTest()
    }
  }
}

const resetTest = () => {
  isAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = null
  correctIndex.value = null
  stopTimer()
  testStore.resetTest()
}

const playPronunciation = () => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(testStore.currentWord.word)
    utterance.lang = 'en-US'
    speechSynthesis.speak(utterance)
  }
}
</script>

<style scoped>
.test {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.test h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.test-start {
  text-align: center;
  padding: 60px 0;
}

.test-start h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.test-start p {
  margin-bottom: 40px;
  font-size: 16px;
  line-height: 1.6;
}

.test-start .btn {
  padding: 15px 40px;
  font-size: 18px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #e2e8f0;
  border-radius: 5px;
  margin-bottom: 30px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #165DFF, #0EA5E9);
  transition: width 0.5s ease;
  border-radius: 5px;
}

.question h3 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 18px;
  font-weight: 600;
}

.word-info {
  text-align: center;
  margin-bottom: 40px;
}

.word-info h2 {
  font-size: 48px;
  margin-bottom: 16px;
  font-weight: 800;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.phonetic-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

.phonetic {
  color: #64748b;
  font-style: italic;
  margin: 0;
  font-size: 16px;
}

.phonetic-btn {
  background-color: #e2e8f0;
  color: #1e293b;
  padding: 8px 12px;
  font-size: 16px;
  border: 1px solid #cbd5e1;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.phonetic-btn:hover {
  background-color: #cbd5e1;
  border-color: #165DFF;
  transform: scale(1.1);
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.option.correct {
  background: linear-gradient(135deg, #10b981, #34d399);
  color: white;
  border-color: #10b981;
  box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
}

.option.incorrect {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: white;
  border-color: #ef4444;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.4);
}

.unknown-button {
  margin-top: 30px;
  text-align: center;
}

.unknown {
  background: linear-gradient(135deg, #ff9800, #f59e0b);
  color: white;
  padding: 16px 40px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.unknown:hover {
  background: linear-gradient(135deg, #f57c00, #ea580c);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(245, 124, 0, 0.4);
}

.test-result {
  text-align: center;
}

.test-result h2 {
  margin-bottom: 30px;
  font-size: 28px;
}

.result-info {
  margin-bottom: 40px;
}

.result-info p {
  font-size: 18px;
  margin-bottom: 12px;
  font-weight: 500;
}

.suggestions {
  margin-top: 30px;
  background-color: #f8fafc;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #165DFF;
  text-align: left;
}

.suggestions h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
}

.suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.suggestions li {
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.5;
}

.result-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  flex-wrap: wrap;
}

.result-buttons .btn {
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
  transform: none !important;
  box-shadow: none !important;
}

.test-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
}

.stat-value.wrong {
  color: #ef4444;
}

.stat-value.consecutive-wrong {
  color: #f59e0b;
}

.stat-value.timer {
  color: #165DFF;
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
  .test {
    padding: 16px;
  }
  
  .test h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }
  
  .word-info h2 {
    font-size: 36px;
  }
  
  .options {
    gap: 10px;
  }
  
  .option {
    padding: 14px 16px;
    font-size: 14px;
  }
  
  .test-stats {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }
  
  .stat-item {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
  
  .result-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .result-buttons .btn {
    width: 200px;
  }
}
</style>