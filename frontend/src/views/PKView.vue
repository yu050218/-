<template>
  <div class="pk">
    <h1>单词PK对战</h1>

    <!-- 未登录状态 -->
    <div v-if="!userStore.isLoggedIn" class="not-logged-in card animate-fade-in">
      <div class="icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14.5 17.5L3 6V3h3l11.5 11.5"></path>
          <path d="M13 19l6-6"></path>
          <path d="M16 16l4 4"></path>
          <path d="M19 21l2-2"></path>
        </svg>
      </div>
      <p>请先登录以参与PK对战</p>
      <router-link to="/login" class="btn btn-primary">登录</router-link>
    </div>

    <!-- 已登录状态 -->
    <div v-else>
      <!-- 匹配界面 -->
      <div v-if="!matchId" class="match-queue card animate-fade-in">
        <h2>寻找对手</h2>
        <div v-if="isMatching" class="matching-animation">
          <div class="spinner"></div>
          <p>正在匹配中，请稍候...</p>
          <button @click="cancelMatching" class="btn btn-secondary">取消匹配</button>
        </div>
        <button v-else @click="startMatching" class="btn btn-primary">开始匹配</button>
      </div>

      <!-- 对战界面 -->
      <div v-else-if="matchStatus === 'active'" class="pk-battle card animate-fade-in">
        <h2>PK对战</h2>
        <div class="battle-info">
          <div class="player you">
            <span class="player-name">你</span>
            <span class="score">{{ score1 }}</span>
          </div>
          <div class="vs">VS</div>
          <div class="player opponent">
            <span class="player-name">{{ isAiMatch ? 'AI' : '对手' }}</span>
            <span class="score">{{ score2 }}</span>
          </div>
        </div>
        <div class="round-info">
          <span class="round-badge">第 {{ currentRound }} / 10 回合</span>
        </div>
        <div class="word-info">
          <h3>{{ currentWord }}</h3>
          <p class="phonetic">{{ currentPhonetic }}</p>
          <p class="instruction">选择正确的释义：</p>
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
        <div class="leave-button">
          <button @click="leaveMatch" class="btn btn-leave">退出对战</button>
        </div>
      </div>

      <!-- 对战结果 -->
      <div v-else-if="matchStatus === 'finished'" class="pk-result card animate-fade-in">
        <h2>对战结果</h2>
        <div class="result-info">
          <div class="player-result you">
            <span class="player-name">你</span>
            <span class="score">{{ score1 }}</span>
          </div>
          <div class="vs">VS</div>
          <div class="player-result opponent">
            <span class="player-name">{{ isAiMatch ? 'AI' : '对手' }}</span>
            <span class="score">{{ score2 }}</span>
          </div>
        </div>
        <div class="winner" :class="{ 'win': winner === 'you', 'lose': winner === 'opponent', 'draw': winner === 'draw' }">
          <span v-if="winner === 'you'">🎉 你赢了！</span>
          <span v-else-if="winner === 'opponent'">😢 你输了！</span>
          <span v-else>🤝 平局！</span>
        </div>
        <div class="result-buttons">
          <button @click="resetPK" class="btn btn-primary">再来一局</button>
          <router-link to="/" class="btn btn-secondary">返回首页</router-link>
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
    // 先尝试离开之前的对战（如果有）
    try {
      await axios.put('/api/pk/match', {
        match_id: 'leave_previous',
        action: 'leave'
      }, {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      })
    } catch (leaveError) {
      // 忽略离开错误，继续尝试匹配
      console.log('No previous match to leave')
    }

    console.log('Token being sent:', userStore.token)
    const response = await axios.post('/api/pk/match', {}, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    console.log('Match response:', response)
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
    console.error('Error response:', error.response)
    console.error('Error data:', error.response?.data)
    console.error('Error status:', error.response?.status)
    isMatching.value = false
    
    // 如果是已经在匹配中的错误，提示用户
    if (error.response?.data?.message === 'You are already in a match' || 
        error.response?.data?.message === 'You are already in the match queue') {
      alert('您已经在匹配中或正在进行对战，请刷新页面后重试')
    }
  }
}

const cancelMatching = async () => {
  isMatching.value = false
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

const leaveMatch = async () => {
  if (!matchId.value) return
  
  try {
    await axios.put('/api/pk/match', {
      match_id: matchId.value,
      action: 'leave'
    }, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
  } catch (error) {
    console.error('离开对战失败:', error)
  }
  
  // 重置状态
  resetPK()
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
  isMatching.value = false
}
</script>

<style scoped>
.pk {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.pk h1 {
  text-align: center;
  margin-bottom: 40px;
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

.match-queue {
  text-align: center;
  padding: 60px 20px;
}

.match-queue h2 {
  margin-bottom: 30px;
  font-size: 24px;
}

.matching-animation {
  padding: 40px 0;
}

.matching-animation .btn {
  margin-top: 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  border: 4px solid #e2e8f0;
  border-top-color: #165DFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.app.dark .spinner {
  border-color: #334155;
  border-top-color: #60a5fa;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.pk-battle h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.battle-info {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px;
  background-color: #f8fafc;
  border-radius: 12px;
}

.app.dark .battle-info {
  background-color: #1e293b;
}

.player {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.player-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.app.dark .player-name {
  color: #f1f5f9;
}

.score {
  font-size: 36px;
  font-weight: 700;
}

.player.you .score {
  color: #10b981;
}

.player.opponent .score {
  color: #ef4444;
}

.vs {
  font-size: 28px;
  font-weight: 800;
  color: #64748b;
}

.app.dark .vs {
  color: #94a3b8;
}

.round-info {
  text-align: center;
  margin-bottom: 24px;
}

.round-badge {
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.word-info {
  text-align: center;
  margin-bottom: 32px;
}

.word-info h3 {
  font-size: 42px;
  margin-bottom: 12px;
  font-weight: 800;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.word-info .phonetic {
  color: #64748b;
  font-style: italic;
  margin-bottom: 16px;
  font-size: 16px;
}

.app.dark .word-info .phonetic {
  color: #94a3b8;
}

.word-info .instruction {
  color: #64748b;
  font-size: 16px;
  margin-bottom: 8px;
}

.app.dark .word-info .instruction {
  color: #94a3b8;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
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

.app.dark .option {
  background-color: #1e293b;
  color: #f1f5f9;
  border-color: #334155;
}

.option:hover {
  background-color: #f1f5f9;
  border-color: #165DFF;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.app.dark .option:hover {
  background-color: #334155;
  border-color: #60a5fa;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.leave-button {
  margin-top: 30px;
  text-align: center;
}

.btn-leave {
  background: transparent;
  color: #64748b;
  border: 2px solid #e2e8f0;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.app.dark .btn-leave {
  color: #94a3b8;
  border-color: #334155;
}

.btn-leave:hover {
  background-color: #fef2f2;
  border-color: #ef4444;
  color: #ef4444;
}

.app.dark .btn-leave:hover {
  background-color: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.pk-result {
  text-align: center;
  padding: 40px 20px;
}

.pk-result h2 {
  margin-bottom: 30px;
  font-size: 24px;
}

.result-info {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 30px;
  padding: 24px;
  background-color: #f8fafc;
  border-radius: 12px;
}

.app.dark .result-info {
  background-color: #1e293b;
}

.player-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.player-result .player-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.app.dark .player-result .player-name {
  color: #f1f5f9;
}

.player-result .score {
  font-size: 36px;
  font-weight: 700;
}

.player-result.you .score {
  color: #10b981;
}

.player-result.opponent .score {
  color: #ef4444;
}

.winner {
  margin-bottom: 40px;
  font-size: 28px;
  font-weight: 700;
  padding: 20px;
  border-radius: 12px;
}

.winner.win {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.2));
  color: #10b981;
}

.winner.lose {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.2));
  color: #ef4444;
}

.winner.draw {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.2));
  color: #f59e0b;
}

.result-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
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
  .pk {
    padding: 16px;
  }

  .pk h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .not-logged-in {
    padding: 40px 16px;
  }

  .not-logged-in .icon {
    width: 48px;
    height: 48px;
  }

  .match-queue {
    padding: 40px 16px;
  }

  .battle-info {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }

  .vs {
    font-size: 24px;
  }

  .score {
    font-size: 28px;
  }

  .word-info h3 {
    font-size: 32px;
  }

  .result-info {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }

  .winner {
    font-size: 24px;
    padding: 16px;
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
