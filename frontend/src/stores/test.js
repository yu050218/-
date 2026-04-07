import { defineStore } from 'pinia'
import axios from 'axios'

export const useTestStore = defineStore('test', {
  state: () => ({
    sessionId: null,
    currentQuestion: 1,
    totalQuestions: 30,
    currentWord: null,
    testResult: null,
    testRecords: []
  }),
  actions: {
    async startTest(testType) {
      try {
        const response = await axios.post('/api/test/start', {
          test_type: testType
        })
        this.sessionId = response.data.session_id
        this.currentQuestion = response.data.current_question
        this.totalQuestions = response.data.total_questions
        this.currentWord = response.data.question
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    async submitAnswer(wordId, answer) {
      try {
        const response = await axios.post('/api/test/submit', {
          session_id: this.sessionId,
          word_id: wordId,
          answer: answer
        })
        if (response.data.question) {
          this.currentQuestion = response.data.current_question
          this.currentWord = response.data.question
        } else {
          this.testResult = response.data.result
          this.sessionId = null
        }
        return response.data
      } catch (error) {
        throw error.response.data
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
    resetTest() {
      this.sessionId = null
      this.currentQuestion = 1
      this.totalQuestions = 30
      this.currentWord = null
      this.testResult = null
    }
  }
})