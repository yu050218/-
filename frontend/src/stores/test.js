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
        const response = await axios.post('/api/test/start', {
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
        const response = await axios.post('/api/test/submit', {
          session_id: this.sessionId,
          word: word,
          answer: answer
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
        }
        return response.data
      } catch (error) {
        console.error('Error submitting answer:', error)
        throw error.response ? error.response.data : error
      }
    },
    async getTestRecords(token) {
      try {
        const response = await axios.get('/api/test/record', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.testRecords = response.data
        return response.data
      } catch (error) {
        throw error.response.data
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