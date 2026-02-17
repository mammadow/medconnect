import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const usePrescriptionStore = defineStore('prescription', () => {
  const prescriptions = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchPrescriptions = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/prescriptions')
      prescriptions.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch prescriptions'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const getPrescription = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/prescriptions/${id}`)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch prescription'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const createPrescription = async (prescriptionData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/api/prescriptions', prescriptionData)
      prescriptions.value.unshift(response.data.prescription)
      return { success: true, data: response.data.prescription }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to create prescription'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const updatePrescription = async (id, prescriptionData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/api/prescriptions/${id}`, prescriptionData)
      const index = prescriptions.value.findIndex(p => p.id === id)
      if (index !== -1) {
        prescriptions.value[index] = response.data.prescription
      }
      return { success: true, data: response.data.prescription }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update prescription'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return {
    prescriptions,
    loading,
    error,
    fetchPrescriptions,
    getPrescription,
    createPrescription,
    updatePrescription
  }
})