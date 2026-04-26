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
  console.log('File uploaded:', event.target.files[0])
}

const uploadWordBank = async () => {
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
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
}

.app.dark .admin {
  background-color: rgba(30, 41, 59, 0.95);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.admin h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #1e293b;
  font-weight: 700;
  font-size: 32px;
}

.app.dark .admin h1 {
  color: #f1f5f9;
}

.admin-tabs {
  display: flex;
  margin-bottom: 40px;
  border-bottom: 1px solid #e2e8f0;
  gap: 8px;
}

.app.dark .admin-tabs {
  border-bottom-color: #334155;
}

.tab-button {
  padding: 12px 24px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  color: #64748b;
  transition: all 0.3s ease;
  border-radius: 8px 8px 0 0;
}

.tab-button:hover {
  color: #1e40af;
  background: rgba(30, 64, 175, 0.05);
}

.app.dark .tab-button:hover {
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
}

.tab-button.active {
  color: #1e40af;
  border-bottom-color: #1e40af;
  background: rgba(30, 64, 175, 0.08);
}

.app.dark .tab-button.active {
  color: #60a5fa;
  border-bottom-color: #60a5fa;
  background: rgba(96, 165, 250, 0.12);
}

.admin-section h2 {
  margin-bottom: 24px;
  color: #1e293b;
  font-weight: 600;
  font-size: 20px;
}

.app.dark .admin-section h2 {
  color: #f1f5f9;
}

.users-list, .records-list {
  margin-bottom: 40px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
}

th, td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.app.dark th, .app.dark td {
  border-bottom-color: #334155;
}

th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #475569;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.app.dark th {
  background-color: #1e293b;
  color: #94a3b8;
}

tr {
  transition: background-color 0.2s ease;
}

tr:hover {
  background-color: #f8fafc;
}

.app.dark tr:hover {
  background-color: #1e293b;
}

td {
  color: #1e293b;
  font-size: 14px;
}

.app.dark td {
  color: #e2e8f0;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 8px;
  font-size: 13px;
  font-weight: 600;
}

.btn.view {
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
}

.btn.view:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.app.dark .btn.view {
  background: linear-gradient(135deg, #1e40af, #60a5fa);
}

.app.dark .btn.view:hover {
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
}

.btn.delete {
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
}

.btn.delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.app.dark .btn.delete:hover {
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
}

.btn.back {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.btn.back:hover {
  background: #e2e8f0;
}

.app.dark .btn.back {
  background: #1e293b;
  color: #94a3b8;
  border-color: #334155;
}

.app.dark .btn.back:hover {
  background: #334155;
}

.btn.upload {
  background: linear-gradient(135deg, #059669, #10b981);
  color: white;
  margin-top: 12px;
}

.btn.upload:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

.app.dark .btn.upload:hover {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.empty-message {
  text-align: center;
  padding: 80px 0;
  color: #64748b;
  font-size: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px dashed #e2e8f0;
}

.app.dark .empty-message {
  color: #94a3b8;
  background: #1e293b;
  border-color: #334155;
}

.words-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.word-card {
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #1e40af;
  transition: all 0.3s ease;
}

.word-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.app.dark .word-card {
  background: #1e293b;
}

.app.dark .word-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.word-info h3 {
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 600;
  font-size: 18px;
}

.app.dark .word-info h3 {
  color: #f1f5f9;
}

.phonetic {
  color: #64748b;
  font-style: italic;
  margin-bottom: 12px;
  font-size: 14px;
}

.app.dark .phonetic {
  color: #94a3b8;
}

.meaning {
  margin-bottom: 12px;
  color: #475569;
  font-size: 14px;
  line-height: 1.6;
}

.app.dark .meaning {
  color: #cbd5e1;
}

.difficulty {
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
  display: inline-block;
  padding: 4px 10px;
  background: rgba(30, 64, 175, 0.1);
  border-radius: 20px;
  color: #1e40af;
}

.app.dark .difficulty {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
}

.upload-section {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e2e8f0;
}

.app.dark .upload-section {
  border-top-color: #334155;
}

.upload-section h3 {
  margin-bottom: 16px;
  color: #1e293b;
  font-weight: 600;
}

.app.dark .upload-section h3 {
  color: #f1f5f9;
}

.upload-section input[type="file"] {
  padding: 12px;
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  background: #f8fafc;
  color: #475569;
  font-size: 14px;
}

.app.dark .upload-section input[type="file"] {
  border-color: #334155;
  background: #1e293b;
  color: #94a3b8;
}

.back-button {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .admin {
    padding: 24px 16px;
  }

  .admin h1 {
    font-size: 24px;
    margin-bottom: 24px;
  }

  .tab-button {
    padding: 10px 16px;
    font-size: 14px;
  }

  .words-grid {
    grid-template-columns: 1fr;
  }

  table {
    font-size: 13px;
  }

  th, td {
    padding: 10px 8px;
  }
}
</style>
