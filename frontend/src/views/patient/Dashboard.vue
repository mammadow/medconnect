<template>
  <div class="patient-dashboard">
    <div class="dashboard-header">
      <div>
        <h1>{{ t('patient.dashboardTitle', { name: authStore.user.name }) }}</h1>
        <p class="subtitle">{{ t('patient.dashboardSubtitle') }}</p>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon-wrapper">
          <AppIcon name="prescription" class="stat-icon" />
        </div>
        <div class="stat-content">
          <h3>{{ prescriptions.length }}</h3>
          <p>{{ t('patient.stats.totalPrescriptions') }}</p>
        </div>
      </div>

      <div class="stat-card stat-success">
        <div class="stat-icon-wrapper">
          <AppIcon name="check" class="stat-icon" />
        </div>
        <div class="stat-content">
          <h3>{{ activePrescriptions }}</h3>
          <p>{{ t('patient.stats.activePrescriptions') }}</p>
        </div>
      </div>

      <div class="stat-card stat-warning">
        <div class="stat-icon-wrapper">
          <AppIcon name="order" class="stat-icon" />
        </div>
        <div class="stat-content">
          <h3>{{ orders.length }}</h3>
          <p>{{ t('patient.stats.totalOrders') }}</p>
        </div>
      </div>

      <div class="stat-card stat-info">
        <div class="stat-icon-wrapper">
          <AppIcon name="pending" class="stat-icon" />
        </div>
        <div class="stat-content">
          <h3>{{ pendingOrders }}</h3>
          <p>{{ t('patient.stats.pendingOrders') }}</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>{{ t('patient.quickActions') }}</h2>
      <div class="actions-grid">
        <router-link to="/patient/prescriptions" class="action-card">
          <div class="action-icon">
            <AppIcon name="prescription" class="action-icon-svg" />
          </div>
          <h3>{{ t('patient.myPrescriptions') }}</h3>
          <p>{{ t('patient.myPrescriptionsDesc') }}</p>
        </router-link>

        <router-link to="/patient/orders" class="action-card">
          <div class="action-icon">
            <AppIcon name="order" class="action-icon-svg" />
          </div>
          <h3>{{ t('patient.placeOrder') }}</h3>
          <p>{{ t('patient.placeOrderDesc') }}</p>
        </router-link>

        <div class="action-card" @click="showChemists = true">
          <div class="action-icon">
            <AppIcon name="pharmacy" class="action-icon-svg" />
          </div>
          <h3>{{ t('patient.chemists') }}</h3>
          <p>{{ t('patient.chemistsDesc') }}</p>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <h2>{{ t('patient.recentPrescriptions') }}</h2>
        <router-link to="/patient/prescriptions" class="link-view-all">
          {{ t('patient.viewAll') }}
        </router-link>
      </div>

      <div v-if="prescriptionLoading" class="loading">
        <div class="spinner"></div>
        <p>{{ t('patient.prescriptionsLoading') }}</p>
      </div>

      <div v-else-if="recentPrescriptions.length === 0" class="empty-state">
        <AppIcon name="prescription" class="empty-icon" />
        <h3>{{ t('patient.noPrescriptions') }}</h3>
        <p>{{ t('patient.noPrescriptionsDesc') }}</p>
      </div>

      <div v-else class="prescriptions-grid">
        <PrescriptionCard
          v-for="prescription in recentPrescriptions"
          :key="prescription.id"
          :prescription="prescription"
          class="prescription-item"
        >
          <template #actions>
            <button @click="createOrderFromPrescription(prescription)" class="btn btn-primary btn-sm">
              {{ t('patient.placeOrder') }}
            </button>
          </template>
        </PrescriptionCard>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <h2>{{ t('patient.recentOrders') }}</h2>
        <router-link to="/patient/orders" class="link-view-all">
          {{ t('patient.viewAll') }}
        </router-link>
      </div>

      <div v-if="orderLoading" class="loading">
        <div class="spinner"></div>
        <p>{{ t('patient.ordersLoading') }}</p>
      </div>

      <div v-else-if="recentOrders.length === 0" class="empty-state">
        <AppIcon name="order" class="empty-icon" />
        <h3>{{ t('patient.noOrders') }}</h3>
        <p>{{ t('patient.noOrdersDesc') }}</p>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in recentOrders" :key="order.id" class="order-item">
          <div class="order-header">
            <div class="order-info">
              <h4>{{ t('order.orderLabel') }} #{{ order.id }}</h4>
              <p class="order-date">{{ formatDate(order.created_at) }}</p>
            </div>
            <span :class="['status-badge', `status-${order.status}`]">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <div class="order-content">
            <div v-if="order.prescription" class="order-prescription">
              <strong>{{ t('patient.orderDiagnosis') }}:</strong> {{ order.prescription.diagnosis }}
            </div>
            <div v-if="order.chemist" class="order-chemist">
              <strong>{{ t('patient.orderPharmacy') }}:</strong> {{ order.chemist.pharmacy_name || order.chemist.name }}
            </div>
            <div v-if="order.delivery_address" class="order-address">
              <strong>{{ t('patient.orderAddress') }}:</strong> {{ order.delivery_address }}
            </div>
          </div>

          <div class="order-actions">
            <router-link :to="`/patient/orders?id=${order.id}`" class="btn btn-secondary btn-sm">
              {{ t('patient.orderDetails') }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showChemists" class="modal-overlay" @click="showChemists = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>{{ t('patient.modalTitle') }}</h2>
          <button @click="showChemists = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="chemists.length === 0" class="loading">{{ t('patient.modalLoading') }}</div>
          <div v-else class="chemists-list">
            <div v-for="chemist in chemists" :key="chemist.id" class="chemist-item">
              <div class="chemist-icon">
                <AppIcon name="pharmacy" class="chemist-icon-svg" />
              </div>
              <div class="chemist-info">
                <h4>{{ chemist.pharmacy_name || chemist.name }}</h4>
                <p v-if="chemist.address">{{ t('order.address') }}: {{ chemist.address }}</p>
                <p>{{ t('order.phone') }}: {{ chemist.number }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { usePrescriptionStore } from '../../stores/prescription'
import { useOrderStore } from '../../stores/order'
import { chemistApi } from '../../services/api'
import PrescriptionCard from '../../components/PrescriptionCard.vue'
import AppIcon from '../../components/AppIcon.vue'
import { useI18n } from '../../i18n'

const router = useRouter()
const authStore = useAuthStore()
const prescriptionStore = usePrescriptionStore()
const orderStore = useOrderStore()
const { t, dateLocale } = useI18n()

const prescriptions = computed(() => prescriptionStore.prescriptions)
const orders = computed(() => orderStore.orders)
const prescriptionLoading = computed(() => prescriptionStore.loading)
const orderLoading = computed(() => orderStore.loading)

const showChemists = ref(false)
const chemists = ref([])

const activePrescriptions = computed(() => {
  return prescriptions.value.filter(p => p.status === 'active').length
})

const pendingOrders = computed(() => {
  return orders.value.filter(o => o.status === 'pending' || o.status === 'accepted').length
})

const recentPrescriptions = computed(() => {
  return prescriptions.value.slice(0, 3)
})

const recentOrders = computed(() => {
  return orders.value.slice(0, 3)
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString(dateLocale.value, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => t(`status.${status}`)

const createOrderFromPrescription = (prescription) => {
  router.push({
    path: '/patient/orders',
    query: { prescription_id: prescription.id }
  })
}

const loadChemists = async () => {
  try {
    const response = await chemistApi.getAll()
    chemists.value = response.data
  } catch (error) {
    console.error('Failed to load chemists:', error)
  }
}

onMounted(async () => {
  await prescriptionStore.fetchPrescriptions()
  await orderStore.fetchOrders()
  await loadChemists()
})
</script>

<style scoped>
.patient-dashboard {
  animation: fadeIn 0.5s ease;
}

.dashboard-header {
  margin-bottom: 40px;
}

.dashboard-header h1 {
  color: #2c3e50;
  font-size: 36px;
  margin-bottom: 8px;
}

.subtitle {
  color: #7f8c8d;
  font-size: 18px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  border-left: 4px solid;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.stat-primary {
  border-color: #3498db;
}

.stat-success {
  border-color: #27ae60;
}

.stat-warning {
  border-color: #f39c12;
}

.stat-info {
  border-color: #9b59b6;
}

.stat-icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(52, 152, 219, 0.05) 100%);
}

.stat-icon {
  width: 28px;
  height: 28px;
  color: #2c3e50;
}

.stat-success .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(39, 174, 96, 0.1) 0%, rgba(39, 174, 96, 0.05) 100%);
}

.stat-warning .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(243, 156, 18, 0.1) 0%, rgba(243, 156, 18, 0.05) 100%);
}

.stat-info .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(155, 89, 182, 0.1) 0%, rgba(155, 89, 182, 0.05) 100%);
}

.stat-content h3 {
  font-size: 42px;
  color: #2c3e50;
  margin-bottom: 4px;
  font-weight: 700;
}

.stat-content p {
  color: #7f8c8d;
  font-size: 15px;
  font-weight: 500;
}

.quick-actions {
  margin-bottom: 50px;
}

.quick-actions h2 {
  color: #2c3e50;
  margin-bottom: 24px;
  font-size: 28px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.action-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: center;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
  border-color: #3498db;
}

.action-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
}

.action-icon-svg {
  width: 28px;
  height: 28px;
  color: #2c3e50;
}

.action-card h3 {
  color: #2c3e50;
  margin-bottom: 12px;
  font-size: 22px;
}

.action-card p {
  color: #7f8c8d;
  font-size: 15px;
  line-height: 1.5;
}

.section {
  margin-bottom: 50px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  color: #2c3e50;
  font-size: 28px;
}

.link-view-all {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: color 0.3s;
}

.link-view-all:hover {
  color: #2980b9;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.empty-icon {
  width: 52px;
  height: 52px;
  margin: 0 auto 20px;
  opacity: 0.5;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 12px;
  font-size: 22px;
}

.empty-state p {
  color: #7f8c8d;
  font-size: 16px;
}

.prescriptions-grid {
  display: grid;
  gap: 20px;
}

.prescription-item {
  animation: slideUp 0.4s ease;
}

.orders-list {
  display: grid;
  gap: 20px;
}

.order-item {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.order-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f5f7fa;
}

.order-info h4 {
  color: #2c3e50;
  margin-bottom: 6px;
  font-size: 20px;
}

.order-date {
  color: #7f8c8d;
  font-size: 14px;
}

.order-content {
  margin-bottom: 16px;
}

.order-prescription,
.order-chemist,
.order-address {
  margin-bottom: 10px;
  color: #555;
  font-size: 15px;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

.modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  animation: slideUp 0.3s;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #f5f7fa;
}

.modal-header h2 {
  color: #2c3e50;
  font-size: 24px;
}

.modal-close {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: #7f8c8d;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.modal-close:hover {
  background: #f5f7fa;
  color: #2c3e50;
}

.modal-body {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.chemists-list {
  display: grid;
  gap: 16px;
}

.chemist-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.chemist-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.chemist-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
}

.chemist-icon-svg {
  width: 26px;
  height: 26px;
  color: #2c3e50;
}

.chemist-info h4 {
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 18px;
}

.chemist-info p {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 4px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
