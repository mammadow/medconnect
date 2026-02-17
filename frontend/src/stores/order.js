import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchOrders = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/orders')
      orders.value = response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch orders'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const getOrder = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/orders/${id}`)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch order'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const createOrder = async (orderData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/api/orders', orderData)
      orders.value.unshift(response.data.order)
      return { success: true, data: response.data.order }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to create order'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const acceptOrder = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/api/orders/${id}/accept`)
      const index = orders.value.findIndex(o => o.id === id)
      if (index !== -1) {
        orders.value[index] = response.data.order
      }
      return { success: true, data: response.data.order }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to accept order'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateOrderStatus = async (id, status) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/api/orders/${id}/status`, { status })
      const index = orders.value.findIndex(o => o.id === id)
      if (index !== -1) {
        orders.value[index] = response.data.order
      }
      return { success: true, data: response.data.order }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update order status'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return {
    orders,
    loading,
    error,
    fetchOrders,
    getOrder,
    createOrder,
    acceptOrder,
    updateOrderStatus
  }
})