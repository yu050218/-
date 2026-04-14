<template>
  <div class="report">
    <h1>测试报告</h1>
    
    <!-- 最新测试结果 -->
    <div v-if="testStore.testResult" class="latest-result">
      <h2>最新测试结果</h2>
      <div class="result-card">
        <div class="result-item">
          <span class="label">词汇量</span>
          <span class="value">{{ testStore.testResult.vocabulary_size }}</span>
        </div>
        <div class="result-item">
          <span class="label">等级</span>
          <span class="value">{{ testStore.testResult.level }}</span>
        </div>
        <div class="result-item">
          <span class="label">正确率</span>
          <span class="value">{{ (testStore.testResult.correct_rate * 100).toFixed(1) }}%</span>
        </div>
      </div>
    </div>
    
    <!-- 历史趋势图 -->
    <div class="history-chart">
      <h2>历史测试趋势</h2>
      <canvas ref="chartCanvas"></canvas>
    </div>
    
    <!-- 历史测试记录 -->
    <div class="history-records">
      <h2>历史测试记录</h2>
      <div class="records-table">
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
            <tr v-for="record in recentTestRecords" :key="record.id">
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
    </div>
    
    <div class="report-buttons">
      <router-link to="/test" class="btn">再测一次</router-link>
      <router-link to="/" class="btn">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTestStore } from '../stores/test'
import { useUserStore } from '../stores/user'
import Chart from 'chart.js/auto'

const testStore = useTestStore()
const userStore = useUserStore()
const chartCanvas = ref(null)
let chart = null

// 只显示最近3次的测试记录
const recentTestRecords = computed(() => {
  return testStore.testRecords.slice(0, 3)
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const loadTestRecords = async () => {
  if (userStore.token) {
    await testStore.getTestRecords(userStore.token)
  }
}

const createChart = () => {
  if (!chartCanvas.value) return
  
  const ctx = chartCanvas.value.getContext('2d')
  
  // 只取最近的测试记录（最多5次）
  const recentRecords = testStore.testRecords.slice(0, 5).reverse()
  
  // 准备图表数据
  const labels = recentRecords.map(record => formatDate(record.test_date))
  const vocabularyData = recentRecords.map(record => record.vocabulary_size)
  const correctRateData = recentRecords.map(record => (record.correct_count / record.total_count) * 100)
  
  // 销毁旧图表
  if (chart) {
    chart.destroy()
  }
  
  // 创建新图表
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '正确率 (%)',
          data: correctRateData,
          borderColor: '#2196F3',
          backgroundColor: 'rgba(33, 150, 243, 0.1)',
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: '正确率 (%)'
          }
        }
      }
    }
  })
}

onMounted(async () => {
  await loadTestRecords()
  createChart()
})
</script>

<style scoped>
.report {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.report h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.latest-result {
  margin-bottom: 40px;
}

.latest-result h2 {
  margin-bottom: 20px;
  color: #666;
}

.result-card {
  display: flex;
  justify-content: space-around;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
}

.result-item {
  text-align: center;
}

.result-item .label {
  display: block;
  color: #666;
  margin-bottom: 5px;
}

.result-item .value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.history-chart {
  margin-bottom: 40px;
}

.history-chart h2 {
  margin-bottom: 20px;
  color: #666;
}

.history-records {
  margin-bottom: 40px;
}

.history-records h2 {
  margin-bottom: 20px;
  color: #666;
}

.records-table {
  overflow-x: auto;
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

.report-buttons {
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
  margin: 0 10px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #45a049;
}
</style>