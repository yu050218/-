<template>
  <div class="report">
    <h1>测试报告</h1>

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
      <p>请先登录以查看测试报告</p>
      <router-link to="/login" class="btn btn-primary">登录</router-link>
    </div>

    <!-- 已登录状态 -->
    <template v-else>
      <!-- 最新测试结果 -->
      <div v-if="testStore.testResult" class="latest-result card animate-fade-in" style="animation-delay: 0.1s">
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
      <div class="history-chart card animate-fade-in" style="animation-delay: 0.2s">
        <h2>历史测试趋势</h2>
        <div class="chart-container">
          <canvas ref="chartCanvas" id="chartCanvas"></canvas>
        </div>
      </div>

      <!-- 历史测试记录 -->
      <div class="history-records card animate-fade-in" style="animation-delay: 0.3s">
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

      <div class="report-buttons card animate-fade-in" style="animation-delay: 0.4s">
        <router-link to="/test" class="btn btn-primary">再测一次</router-link>
        <router-link to="/" class="btn btn-secondary">返回首页</router-link>
      </div>
    </template>
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

const recentTestRecords = computed(() => {
  return testStore.testRecords.slice(0, 10)
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const loadTestRecords = async () => {
  if (userStore.token) {
    try {
      await testStore.getTestRecords(userStore.token)
      console.log('Test records loaded:', testStore.testRecords)
    } catch (error) {
      console.error('Error loading test records:', error)
    }
  } else {
    console.log('No token, skipping test records load')
  }
}

const createChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')

  const recentRecords = testStore.testRecords.slice(0, 10).reverse()
  console.log('Recent test records for chart:', recentRecords)

  const labels = recentRecords.map(record => formatDate(record.test_date))
  const correctRateData = recentRecords.map(record => (record.correct_count / record.total_count) * 100)
  console.log('Chart labels:', labels)
  console.log('Chart data:', correctRateData)

  if (chart) {
    chart.destroy()
  }

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '正确率 (%)',
          data: correctRateData,
          borderColor: '#165DFF',
          backgroundColor: 'rgba(22, 93, 255, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: '正确率 (%)'
          },
          min: 0,
          max: 100
        }
      },
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: 'index',
          intersect: false
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
  padding: 20px;
}

.report h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 36px;
}

.latest-result h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.result-card {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.result-item {
  text-align: center;
  padding: 20px;
  background-color: #f8fafc;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.app.dark .result-item {
  background-color: #1e293b;
}

.result-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.app.dark .result-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.result-item .label {
  display: block;
  color: #64748b;
  margin-bottom: 8px;
  font-weight: 600;
}

.app.dark .result-item .label {
  color: #94a3b8;
}

.result-item .value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #165DFF, #0EA5E9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.history-chart h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.chart-container {
  height: 300px;
  position: relative;
}

#chartCanvas {
  width: 100% !important;
  height: 100% !important;
}

.history-records h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.records-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.app.dark th, .app.dark td {
  border-bottom-color: #334155;
}

th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #64748b;
}

.app.dark th {
  background-color: #1e293b;
  color: #94a3b8;
}

tr {
  transition: all 0.3s ease;
}

tr:hover {
  background-color: #f1f5f9;
}

.app.dark tr {
  background-color: transparent;
}

.app.dark tr:hover {
  background-color: #334155;
}

td {
  color: #1e293b;
  font-size: 14px;
}

.app.dark td {
  color: #e2e8f0;
}

.report-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  padding: 30px;
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
  font-size: 18px;
  color: #64748b;
  margin-bottom: 30px;
}

.app.dark .not-logged-in p {
  color: #94a3b8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .report {
    padding: 16px;
  }

  .report h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .result-card {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .result-item {
    padding: 16px;
  }

  .result-item .value {
    font-size: 24px;
  }

  .chart-container {
    height: 250px;
  }

  .report-buttons {
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }

  .report-buttons .btn {
    width: 200px;
  }

  table {
    font-size: 14px;
  }

  th, td {
    padding: 10px 12px;
  }
}
</style>
