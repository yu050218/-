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
            <p class="last-wrong">最后错误: {{ formatDate(word.last_wrong_date) }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-message">
      <p>暂无错题记录</p>
    </div>
    
    <div class="wrong-words-buttons">
      <router-link to="/" class="btn">返回首页</router-link>
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

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
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
}

.btn:hover {
  background-color: #45a049;
}
</style>