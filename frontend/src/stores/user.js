import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user && state.user.is_admin === 1
  },
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('/api/login', {
          username,
          password
        })
        this.token = response.data.token
        this.user = {
          id: response.data.user_id,
          username: response.data.username,
          is_admin: response.data.is_admin
        }
        localStorage.setItem('token', this.token)
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    async register(username, email, password) {
      try {
        const response = await axios.post('/api/register', {
          username,
          email,
          password
        })
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    async getProfile() {
      try {
        const response = await axios.get('/api/profile', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        this.user = response.data
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    async updateProfile(email, password) {
      try {
        const response = await axios.put('/api/profile', {
          email,
          password
        }, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        return response.data
      } catch (error) {
        throw error.response.data
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})