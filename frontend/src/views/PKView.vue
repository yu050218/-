<template>
  <div class="pk">
    <h1>单词PK对战</h1>
    
    <!-- 未登录状态 -->
    <div v-if="!userStore.isLoggedIn" class="not-logged-in">
      <p>请先登录以参与PK对战</p>
      <router-link to="/login" class="btn">登录</router-link>
    </div>
    
    <!-- 已登录状态 -->
    <div v-else>
      <!-- 匹配界面 -->
      <div v-if="!matchId" class="match-queue">
        <h2>寻找对手...</h2>
        <p v-if="isMatching">正在匹配中，请稍候...</p>
        <button v-else @click="startMatching" class="btn">开始匹配</button>
      </div>
      
      <!-- 对战界面 -->
      <div v-else-if="matchStatus === 'active'" class="pk-battle">
        <h2>PK对战</h2>
        <div class="battle-info">
          <div class="player">
            <span class="player-name">你</span>
            <span class="score">{{ score1 }}</span>
          </div>
          <div class="vs">VS</div>
          <div class="player">
            <span class="player-name">{{ isAiMatch ? 'AI' : '对手' }}</span>
            <span class="score">{{ score2 }}</span>
          </div>
        </div>
        <div class="round-info">
          <p>第 {{ currentRound }} / 10 回合</p>
        </div>
        <div class="word-info">
          <h3>{{ currentWord }}</h3>
          <p class="phonetic">{{ currentPhonetic }}</p>
          <p>选择正确的释义：</p>
        </div>
        <div class="options">
          <button 
            v-for="(option, index) in options" 
            :key="index"
            @click="submitAnswer(index)"
            :class="['btn', 'option']"
          >
            {{ option }}
          </button>
        </div>
      </div>
      
      <!-- 对战结果 -->
      <div v-else-if="matchStatus === 'finished'" class="pk-result">
        <h2>对战结果</h2>
        <div class="result-info">
          <div class="player-result">
            <span class="player-name">你</span>
            <span class="score">{{ score1 }}</span>
          </div>
          <div class="vs">VS</div>
          <div class="player-result">
            <span class="player-name">{{ isAiMatch ? 'AI' : '对手' }}</span>
            <span class="score">{{ score2 }}</span>
          </div>
        </div>
        <div class="winner">
          <p v-if="winner === 'you'">你赢了！</p>
          <p v-else-if="winner === 'opponent'">你输了！</p>
          <p v-else>平局！</p>
        </div>
        <div class="result-buttons">
          <button @click="resetPK" class="btn">再来一局</button>
          <router-link to="/" class="btn">返回首页</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const userStore = useUserStore()

const isMatching = ref(false)
const matchId = ref(null)
const matchStatus = ref('')
const score1 = ref(0)
const score2 = ref(0)
const currentRound = ref(0)
const currentWord = ref('')
const currentPhonetic = ref('')
const options = ref([])
const winner = ref('')
const isAiMatch = ref(false)

const startMatching = async () => {
  isMatching.value = true
  try {
    const response = await axios.post('/api/pk/match', {}, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    if (response.status === 200) {
      matchId.value = response.data.match_id
      matchStatus.value = 'active'
      currentRound.value = 1
      currentWord.value = response.data.question.word
      currentPhonetic.value = response.data.question.phonetic
      options.value = response.data.question.options
      isAiMatch.value = response.data.opponent_id === 'AI'
    } else if (response.status === 202) {
      // 等待对手
      setTimeout(() => {
        startMatching()
      }, 3000)
    }
  } catch (error) {
    console.error('匹配失败:', error)
    isMatching.value = false
  }
}

const submitAnswer = async (answer) => {
  try {
    const response = await axios.put('/api/pk/match', {
      match_id: matchId.value,
      action: 'submit',
      answer: answer
    }, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    if (response.data.status === 'active') {
      score1.value = response.data.score1
      score2.value = response.data.score2
      currentRound.value = response.data.current_round
      currentWord.value = response.data.question.word
      currentPhonetic.value = response.data.question.phonetic
      options.value = response.data.question.options
    } else if (response.data.status === 'finished') {
      score1.value = response.data.score1
      score2.value = response.data.score2
      matchStatus.value = 'finished'
      isAiMatch.value = response.data.is_ai_match
      winner.value = response.data.winner === userStore.user.id ? 'you' : (response.data.winner === 'AI' ? 'opponent' : 'opponent')
    }
  } catch (error) {
    console.error('提交答案失败:', error)
  }
}

const resetPK = () => {
  matchId.value = null
  matchStatus.value = ''
  score1.value = 0
  score2.value = 0
  currentRound.value = 0
  currentWord.value = ''
  winner.value = ''
  isAiMatch.value = false
}
</script>

<style scoped>
.pk {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.pk h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.not-logged-in {
  text-align: center;
  padding: 60px 0;
}

.not-logged-in p {
  margin-bottom: 30px;
  font-size: 18px;
  color: #666;
}

.match-queue {
  text-align: center;
  padding: 60px 0;
}

.match-queue h2 {
  margin-bottom: 30px;
  color: #666;
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
  text-decoration: none;
  display: inline-block;
}

.btn:hover {
  background-color: #45a049;
}

.pk-battle h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.battle-info {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
}

.player {
  text-align: center;
}

.player-name {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #333;
}

.score {
  font-size: 24px;
  font-weight: bold;
  color: #4CAF50;
}

.vs {
  font-size: 24px;
  font-weight: bold;
  color: #f44336;
  display: flex;
  align-items: center;
}

.round-info {
  text-align: center;
  margin-bottom: 30px;
  font-size: 18px;
  color: #666;
}

.word-info {
  text-align: center;
  margin-bottom: 40px;
}

.word-info h3 {
  font-size: 36px;
  margin-bottom: 20px;
  color: #333;
}

.word-info p {
  font-size: 18px;
  color: #666;
}

.phonetic {
  color: #999;
  font-style: italic;
  margin-bottom: 20px;
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

.pk-result {
  text-align: center;
  padding: 40px 0;
}

.pk-result h2 {
  margin-bottom: 30px;
  color: #333;
}

.result-info {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
}

.player-result {
  text-align: center;
}

.winner {
  margin-bottom: 40px;
  font-size: 24px;
  font-weight: bold;
  color: #f44336;
}

.result-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.result-buttons .btn {
  margin: 0 10px;
}
</style>