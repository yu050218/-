import { defineStore } from 'pinia'
import axios from 'axios'

export const useTestStore = defineStore('test', {
  state: () => ({
    sessionId: localStorage.getItem('testSessionId') || null,
    currentQuestion: 1,
    totalQuestions: 30,
    currentWord: null,
    testResult: null,
    testRecords: []
  }),
  actions: {
    async startTest(testType) {
      try {
        console.log('Starting test with type:', testType)
        const response = await axios.post('http://localhost:8000/api/test/start', {
          test_type: testType
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        console.log('Test started successfully:', response.data)
        this.sessionId = response.data.session_id
        localStorage.setItem('testSessionId', this.sessionId)
        this.currentQuestion = response.data.current_question
        this.totalQuestions = response.data.total_questions
        this.currentWord = response.data.question
        return response.data
      } catch (error) {
        console.error('Error starting test:', error)
        throw error.response ? error.response.data : error
      }
    },
    async submitAnswer(word, answer) {
      try {
        console.log('Submitting answer:', { word, answer, sessionId: this.sessionId })
        
        // 构建请求头
        const headers = {
          'Content-Type': 'application/json'
        }
        // 从 localStorage 读取 token
        const token = localStorage.getItem('token')
        console.log('Retrieved token from localStorage:', token)
        if (token) {
          headers.Authorization = `Bearer ${token}`
          console.log('Including authorization header:', headers.Authorization)
        } else {
          console.log('No token found, not including authorization header')
        }
        
        const response = await axios.post('/api/test/submit', {
          session_id: this.sessionId,
          word: word,
          answer: answer
        }, {
          headers: headers
        })
        console.log('Submit answer response:', response.data)
        if (response.data.question) {
          this.currentQuestion = response.data.current_question
          this.currentWord = response.data.question
          console.log('Next question received:', this.currentWord)
        } else {
          this.testResult = response.data.result
          this.sessionId = null
          this.currentWord = null
          localStorage.removeItem('testSessionId')
          console.log('Test completed, result:', this.testResult)
          
          // 测试完成后，重新加载测试记录
          const token = localStorage.getItem('token')
          console.log('Retrieved token for record reload:', token)
          if (token) {
            console.log('Reloading test records with token:', token)
            this.getTestRecords(token).catch(error => {
              console.error('Error loading test records after test completion:', error)
            })
          } else {
            console.log('No token, skipping test records reload')
          }
        }
        return response.data
      } catch (error) {
        console.error('Error submitting answer:', error)
        throw error.response ? error.response.data : error
      }
    },
    async getTestRecords(token) {
      try {
        console.log('Getting test records with token:', token)
        const response = await axios.get('/api/test/record', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        console.log('Test records response:', response.data)
        this.testRecords = response.data
        return response.data
      } catch (error) {
        console.error('Error getting test records:', error)
        throw error.response ? error.response.data : error
      }
    },
    async getWrongWords(token) {
      try {
        const response = await axios.get('/api/test/wrong-words', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    resetTest() {
      this.sessionId = null
      localStorage.removeItem('testSessionId')
      this.currentQuestion = 1
      this.totalQuestions = 30
      this.currentWord = null
      this.testResult = null
    }
  }
})