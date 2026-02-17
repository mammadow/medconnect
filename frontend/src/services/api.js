import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

const setAuthHeader = (token) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common.Authorization
  }
}

// Initialize default header from existing localStorage token
setAuthHeader(localStorage.getItem('token'))

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - let caller decide
      console.warn('API 401', error.response?.data || error.message)
    }
    return Promise.reject(error)
  }
)

export default api
export { setAuthHeader }

// Specific API methods
export const patientApi = {
  search: (query) => api.get(`/api/patients/search?q=${query}`)
}

export const chemistApi = {
  getAll: () => api.get('/api/chemists')
}

export const doctorApi = {
  getAll: () => api.get('/api/doctors')
}

export const adminApi = {
  getOverview: (params = {}) => api.get('/api/admin/overview', { params }),
  getPending: (params = {}) => api.get('/api/admin/pending', { params }),
  approveUser: (payload) => api.post('/api/admin/approve', payload),
  refuseUser: (payload) => api.post('/api/admin/refuse', payload)
}

export const profileApi = {
  get: () => api.get('/api/me'),
  update: (payload) => api.put('/api/profile', payload)
}
