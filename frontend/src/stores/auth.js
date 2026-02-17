import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { setAuthHeader } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  const setAuth = (authToken, userData) => {
    token.value = authToken
    user.value = userData
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
    setAuthHeader(authToken)
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setAuthHeader(null)
  }

  const login = async (role, credentials) => {
    try {
      const response = await api.post(`/api/login/${role}`, credentials)
      setAuth(response.data.token, response.data.user)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  const register = async (role, userData) => {
    try {
      await api.post(`/api/register/${role}`, userData)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    clearAuth()
  }

  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser
  }
})
