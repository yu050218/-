<template>
  <div class="admin">
    <h1>后台管理</h1>
    
    <div class="admin-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
        class="tab-button"
      >
        {{ tab.name }}
      </button>
    </div>
    
    <!-- 用户管理 -->
    <div v-if="activeTab === 'users'" class="admin-section">
      <h2>用户管理</h2>
      
      <div v-if="users.length > 0" class="users-list">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>
                <button @click="viewUserRecords(user.id)" class="btn view">查看记录</button>
                <button @click="deleteUser(user.id)" class="btn delete">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-else class="empty-message">
        <p>暂无用户记录</p>
      </div>
    </div>
    
    <!-- 用户测评记录 -->
    <div v-if="activeTab === 'user-records'" class="admin-section">
      <h2>用户测评记录</h2>
      
      <div class="back-button">
        <button @click="activeTab = 'users'" class="btn back">返回用户列表</button>
      </div>
      
      <div v-if="userRecords.length > 0" class="records-list">
        <table>
          <thead>
            <tr>
              <th>测试日期</th>
              <th>答对题数</th>
              <th>总题数</th>
              <th>正确率</th>
              <th>词汇量</th>
              <th>等级</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in userRecords" :key="record.id">
              <td>{{ formatDate(record.test_date) }}</td>
              <td>{{ record.correct_count }}</td>
              <td>{{ record.total_count }}</td>
              <td>{{ ((record.correct_count / record.total_count) * 100).toFixed(1) }}%</td>
              <td>{{ record.vocabulary_size }}</td>
              <td>{{ record.level }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-else class="empty-message">
        <p>暂无测评记录</p>
      </div>
    </div>
    
    <!-- 词库管理 -->
    <div v-if="activeTab === 'word-bank'" class="admin-section">
      <h2>测评词库管理</h2>
      
      <div v-if="words.length > 0" class="words-list">
        <div class="words-grid">
          <div v-for="(word, index) in words" :key="index" class="word-card">
            <div class="word-info">
              <h3>{{ word.word }}</h3>
              <p class="phonetic">{{ word.phonetic }}</p>
              <p class="meaning">{{ word.meaning }}</p>
              <p class="difficulty">难度: {{ word.difficulty }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-message">
        <p>暂无单词记录</p>
      </div>
      
      <div class="upload-section">
        <h3>上传新词库</h3>
        <input type="file" @change="handleFileUpload" accept=".xlsx,.xls" />
        <button @click="uploadWordBank" class="btn upload">上传</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const userStore = useUserStore()
const activeTab = ref('users')
const users = ref([])
const userRecords = ref([])
const words = ref([])
const selectedUserId = ref(null)

const tabs = [
  { id: 'users', name: '用户管理' },
  { id: 'word-bank', name: '词库管理' }
]

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const loadUsers = async () => {
  if (userStore.token) {
    try {
      const response = await axios.get('/api/admin/users', {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      })
      users.value = response.data
    } catch (error) {
      console.error('Error loading users:', error)
    }
  }
}

const viewUserRecords = async (userId) => {
  selectedUserId.value = userId
  if (userStore.token) {
    try {
      const response = await axios.get(`/api/admin/users/${userId}/records`, {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      })
      userRecords.value = response.data
      activeTab.value = 'user-records'
    } catch (error) {
      console.error('Error loading user records:', error)
    }
  }
}

const deleteUser = async (userId) => {
  if (confirm('确定要删除这个用户吗？')) {
    if (userStore.token) {
      try {
        await axios.delete(`/api/admin/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${userStore.token}`
          }
        })
        loadUsers()
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    }
  }
}

const loadWordBank = async () => {
  if (userStore.token) {
    try {
      const response = await axios.get('/api/admin/word-bank', {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      })
      words.value = response.data
    } catch (error) {
      console.error('Error loading word bank:', error)
    }
  }
}

const handleFileUpload = (event) => {
  // 处理文件上传
  console.log('File uploaded:', event.target.files[0])
}

const uploadWordBank = async () => {
  // 上传词库文件
  // 实际项目中应该实现文件上传功能
  console.log('Uploading word bank...')
}

onMounted(async () => {
  await loadUsers()
  await loadWordBank()
})
</script>

<style scoped>
.admin {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.admin h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.admin-tabs {
  display: flex;
  margin-bottom: 40px;
  border-bottom: 1px solid #ddd;
}

.tab-button {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: all 0.3s;
}

.tab-button:hover {
  color: #4CAF50;
}

.tab-button.active {
  color: #4CAF50;
  border-bottom-color: #4CAF50;
}

.admin-section h2 {
  margin-bottom: 20px;
  color: #666;
}

.users-list, .records-list {
  margin-bottom: 40px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
  color: #333;
}

tr:hover {
  background-color: #f5f5f5;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-right: 5px;
}

.btn.view {
  background-color: #2196F3;
  color: white;
}

.btn.view:hover {
  background-color: #1976D2;
}

.btn.delete {
  background-color: #f44336;
  color: white;
}

.btn.delete:hover {
  background-color: #d32f2f;
}

.btn.back {
  background-color: #607D8B;
  color: white;
  margin-bottom: 20px;
}

.btn.back:hover {
  background-color: #455A64;
}

.btn.upload {
  background-color: #4CAF50;
  color: white;
  margin-top: 10px;
}

.btn.upload:hover {
  background-color: #45a049;
}

.empty-message {
  text-align: center;
  padding: 60px 0;
  color: #666;
  font-size: 18px;
}

.words-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.word-card {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #4CAF50;
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

.difficulty {
  color: #666;
  font-size: 14px;
}

.upload-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
}

.upload-section h3 {
  margin-bottom: 10px;
  color: #666;
}
</style>
