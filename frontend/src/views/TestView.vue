<template>
  <div class="test">
    <h1>词汇测试</h1>
    
    <!-- 开始测试按钮 -->
    <div v-if="!testStore.sessionId && !testStore.testResult" class="test-start">
      <h2>开始词汇测试</h2>
      <p>本次测试共50道题，包含小学、初中、高中各难度级别</p>
      <button @click="startTest('50')" class="btn">开始测试</button>
    </div>
    
    <!-- 测试进行中 -->
    <div v-else-if="testStore.currentWord" class="test-progress">
      <div class="progress-bar">
        <div class="progress" :style="{ width: (testStore.currentQuestion / testStore.totalQuestions) * 100 + '%' }"></div>
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
    <div v-else-if="testStore.testResult" class="test-result">
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
        <button @click="resetTest" class="btn">再测一次</button>
        <router-link to="/report" class="btn">查看报告</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useTestStore } from '../stores/test'

const testStore = useTestStore()
const isAnswered = ref(false)
const isCorrect = ref(false)
const selectedAnswer = ref(null)
const correctIndex = ref(null)

// 组件挂载时重置测试结果，确保不显示上一次的报告
onMounted(() => {
  testStore.testResult = null
})

// 监听currentWord变化，重置状态
watch(() => testStore.currentWord, () => {
  isAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = null
  correctIndex.value = null
})

const startTest = async (testType) => {
  // 重置测试结果，确保不显示上一次的报告
  testStore.testResult = null
  isAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = null
  correctIndex.value = null
  await testStore.startTest(testType)
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
    
    isCorrect.value = response.is_correct
    
    // 延迟500毫秒后进入下一题
    setTimeout(() => {
      isAnswered.value = false
      selectedAnswer.value = null
      correctIndex.value = null
    }, 500)
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
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.test h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.test-type h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #666;
}

.test-options {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.btn {
  padding: 15px 30px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #45a049;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin-bottom: 30px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.5s;
}

.question h3 {
  text-align: center;
  margin-bottom: 30px;
  color: #666;
}

.word-info {
  text-align: center;
  margin-bottom: 40px;
}

.word-info h2 {
  font-size: 36px;
  margin-bottom: 10px;
  color: #333;
}

.phonetic-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.phonetic {
  color: #999;
  font-style: italic;
  margin: 0;
}

.phonetic-btn {
  background-color: #f0f0f0;
  color: #333;
  padding: 5px 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.phonetic-btn:hover {
  background-color: #e0e0e0;
  border-color: #4CAF50;
}

.meaning {
  font-size: 18px;
  color: #666;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 30px;
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

.unknown-button {
  margin-top: 30px;
  text-align: center;
}

.unknown {
  background-color: #ff9800;
}

.unknown:hover {
  background-color: #f57c00;
}

.test-result {
  text-align: center;
}

.test-result h2 {
  margin-bottom: 30px;
  color: #333;
}

.result-info {
  margin-bottom: 40px;
}

.result-info p {
  font-size: 18px;
  margin-bottom: 10px;
  color: #666;
}

.suggestions {
  margin-top: 20px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 5px;
  border-left: 4px solid #4CAF50;
}

.suggestions h4 {
  margin-top: 0;
  color: #333;
  margin-bottom: 10px;
}

.suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.suggestions li {
  margin-bottom: 5px;
  color: #666;
  font-size: 16px;
}

.result-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.result-buttons .btn {
  margin: 0 10px;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.test-start {
  text-align: center;
  padding: 60px 0;
}

.test-start h2 {
  margin-bottom: 20px;
  color: #333;
}

.test-start p {
  margin-bottom: 40px;
  color: #666;
  font-size: 16px;
}

.test-start .btn {
  padding: 15px 40px;
  font-size: 18px;
}
</style>