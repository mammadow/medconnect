<template>
  <div class="orders-page">
    <div class="page-header">
      <div>
        <h1>{{ t('chemistOrders.title') }}</h1>
        <p class="page-description">{{ t('chemistOrders.subtitle') }}</p>
      </div>
    </div>

    <div class="orders-stats">
      <div class="stat-item">
        <div class="stat-value">{{ orders.length }}</div>
        <div class="stat-label">{{ t('chemistOrders.statsTotal') }}</div>
      </div>
      <div class="stat-item stat-pending">
        <div class="stat-value">{{ pendingOrders }}</div>
        <div class="stat-label">{{ t('chemistOrders.statsPending') }}</div>
      </div>
      <div class="stat-item stat-active">
        <div class="stat-value">{{ activeOrders }}</div>
        <div class="stat-label">{{ t('chemistOrders.statsActive') }}</div>
      </div>
      <div class="stat-item stat-completed">
        <div class="stat-value">{{ completedOrders }}</div>
        <div class="stat-label">{{ t('chemistOrders.statsCompleted') }}</div>
      </div>
    </div>

    <div class="card filters-card">
      <div class="filters-header">
        <h2 class="card-title">{{ t('chemistOrders.filtersTitle') }}</h2>
        <div class="filter-tabs">
          <button
            v-for="filter in statusFilters"
            :key="filter.value"
            @click="activeFilter = filter.value"
            :class="['filter-tab', { active: activeFilter === filter.value }]"
          >
            {{ filter.label }}
            <span v-if="filter.count > 0" class="filter-count">{{ filter.count }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>{{ t('chemistOrders.loading') }}</p>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="empty-state-large">
      <div class="empty-illustration">
        <AppIcon name="order" class="empty-icon" />
      </div>
      <h2>{{ getEmptyMessage() }}</h2>
      <p>{{ getEmptyDescription() }}</p>
    </div>

    <div v-else class="orders-timeline">
      <div
        v-for="order in filteredOrders"
        :key="order.id"
        class="order-timeline-item"
      >
        <div class="timeline-marker" :class="`marker-${order.status}`"></div>
        <div class="order-card-enhanced">
          <div class="order-header-enhanced">
            <div class="order-id-section">
              <div class="order-icon">
                <AppIcon name="order" class="order-icon-svg" />
              </div>
              <div>
                <h3>{{ t('order.orderLabel') }} #{{ order.id }}</h3>
                <p class="order-date">{{ formatDateTime(order.created_at) }}</p>
                <p v-if="order.patient" class="patient-name">
                  {{ t('chemistOrders.patientLabel') }}: {{ order.patient.name }}
                </p>
              </div>
            </div>
            <span :class="['status-badge-large', `status-${order.status}`]">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <div v-if="order.status !== 'pending' && order.status !== 'cancelled'" class="order-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: getProgressWidth(order.status) }"></div>
            </div>
            <div class="progress-labels">
              <span :class="{ active: isStepActive(order.status, 'accepted') }">{{ t('status.accepted') }}</span>
              <span :class="{ active: isStepActive(order.status, 'preparing') }">{{ t('status.preparing') }}</span>
              <span :class="{ active: isStepActive(order.status, 'ready') }">{{ t('status.ready') }}</span>
              <span :class="{ active: isStepActive(order.status, 'completed') }">{{ t('status.completed') }}</span>
            </div>
          </div>

          <div class="order-details-grid">
            <div v-if="order.prescription" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="prescription" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('chemistOrders.prescriptionLabel') }}</h4>
                <p>{{ order.prescription.diagnosis }}</p>
                <small v-if="order.prescription.medicines">
                  {{ order.prescription.medicines.length }} {{ t('chemistOrders.medicinesLabel') }}
                </small>
              </div>
            </div>

            <div v-if="order.patient" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="patient" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('chemistOrders.patientLabel') }}</h4>
                <p>{{ order.patient.name }}</p>
                <small v-if="order.patient.number">{{ order.patient.number }}</small>
              </div>
            </div>

            <div v-if="order.delivery_address" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="location" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('chemistOrders.deliveryLabel') }}</h4>
                <p>{{ order.delivery_address }}</p>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon">
                <AppIcon name="update" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('chemistOrders.lastUpdate') }}</h4>
                <p>{{ formatDateTime(order.updated_at) }}</p>
              </div>
            </div>
          </div>

          <div v-if="order.prescription && order.prescription.medicines && order.prescription.medicines.length" class="medicines-section">
            <h4 class="medicines-title">{{ t('chemistOrders.medicinesLabel') }}:</h4>
            <div class="medicines-grid">
              <div v-for="med in order.prescription.medicines" :key="med.id" class="medicine-card">
                <div class="medicine-header">
                  <strong>{{ med.name }}</strong>
                </div>
                <div class="medicine-details">
                  <span v-if="med.dosage" class="medicine-tag">{{ med.dosage }}</span>
                  <span v-if="med.frequency" class="medicine-tag">{{ med.frequency }}</span>
                  <span v-if="med.duration" class="medicine-tag">{{ med.duration }}</span>
                </div>
                <p v-if="med.instructions" class="medicine-instructions">
                  {{ med.instructions }}
                </p>
              </div>
            </div>
          </div>

          <div v-if="order.notes" class="order-notes">
            <strong>{{ t('chemistOrders.notesLabel') }}:</strong> {{ order.notes }}
          </div>

          <div class="order-actions">
            <template v-if="order.status === 'pending'">
              <button
                @click="handleAcceptOrder(order)"
                class="btn-action-success"
                :disabled="processingOrder === order.id"
              >
                <span v-if="processingOrder === order.id">...</span>
                <span v-else>{{ t('chemistOrders.acceptOrder') }}</span>
              </button>
              <button
                @click="viewOrderDetails(order)"
                class="btn-action-outline"
              >
                {{ t('chemistOrders.viewDetails') }}
              </button>
            </template>

            <template v-else-if="order.status === 'accepted'">
              <button
                @click="updateOrderStatus(order, 'preparing')"
                class="btn-action-primary"
                :disabled="processingOrder === order.id"
              >
                {{ t('chemistOrders.startPreparing') }}
              </button>
              <button
                @click="viewOrderDetails(order)"
                class="btn-action-outline"
              >
                {{ t('chemistOrders.viewDetails') }}
              </button>
            </template>

            <template v-else-if="order.status === 'preparing'">
              <button
                @click="updateOrderStatus(order, 'ready')"
                class="btn-action-success"
                :disabled="processingOrder === order.id"
              >
                {{ t('chemistOrders.markReady') }}
              </button>
              <button
                @click="viewOrderDetails(order)"
                class="btn-action-outline"
              >
                {{ t('chemistOrders.viewDetails') }}
              </button>
            </template>

            <template v-else-if="order.status === 'ready'">
              <button
                @click="updateOrderStatus(order, 'completed')"
                class="btn-action-success"
                :disabled="processingOrder === order.id"
              >
                {{ t('chemistOrders.completeOrder') }}
              </button>
              <button
                @click="viewOrderDetails(order)"
                class="btn-action-outline"
              >
                {{ t('chemistOrders.viewDetails') }}
              </button>
            </template>

            <template v-else>
              <button
                @click="viewOrderDetails(order)"
                class="btn-action-outline"
              >
                {{ t('chemistOrders.viewDetails') }}
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedOrder" class="modal-overlay" @click="selectedOrder = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header-gradient">
          <h2>{{ t('order.orderLabel') }} #{{ selectedOrder.id }}</h2>
          <button @click="selectedOrder = null" class="modal-close-btn">&times;</button>
        </div>

        <div class="modal-body-large">
          <OrderCard
            :order="selectedOrder"
            :show-patient-info="true"
            :show-chemist-info="false"
            :show-actions="false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/order'
import OrderCard from '../../components/OrderCard.vue'
import { useI18n } from '../../i18n'
import AppIcon from '../../components/AppIcon.vue'

const orderStore = useOrderStore()
const { t, dateLocale } = useI18n()
const orders = computed(() => orderStore.orders)
const loading = computed(() => orderStore.loading)

const activeFilter = ref('all')
const selectedOrder = ref(null)
const processingOrder = ref(null)

const pendingOrders = computed(() => {
  return orders.value.filter(o => o.status === 'pending').length
})

const activeOrders = computed(() => {
  return orders.value.filter(o => ['accepted', 'preparing', 'ready'].includes(o.status)).length
})

const completedOrders = computed(() => {
  return orders.value.filter(o => o.status === 'completed').length
})

const statusFilters = computed(() => [
  { value: 'all', label: t('chemistOrders.filterAll'), count: orders.value.length },
  { value: 'pending', label: t('chemistOrders.filterPending'), count: pendingOrders.value },
  { value: 'active', label: t('chemistOrders.filterActive'), count: activeOrders.value },
  { value: 'completed', label: t('chemistOrders.filterCompleted'), count: completedOrders.value }
])

const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') {
    return orders.value
  } else if (activeFilter.value === 'active') {
    return orders.value.filter(o => ['accepted', 'preparing', 'ready'].includes(o.status))
  } else {
    return orders.value.filter(o => o.status === activeFilter.value)
  }
})

const formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString(dateLocale.value, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => t(`status.${status}`)

const getProgressWidth = (status) => {
  const progress = {
    accepted: '25%',
    preparing: '50%',
    ready: '75%',
    completed: '100%'
  }
  return progress[status] || '0%'
}

const isStepActive = (currentStatus, step) => {
  const steps = ['accepted', 'preparing', 'ready', 'completed']
  const currentIndex = steps.indexOf(currentStatus)
  const stepIndex = steps.indexOf(step)
  return stepIndex <= currentIndex
}

const getEmptyMessage = () => {
  const messages = {
    all: t('chemistOrders.emptyAll'),
    pending: t('chemistOrders.emptyPending'),
    active: t('chemistOrders.emptyActive'),
    completed: t('chemistOrders.emptyCompleted')
  }
  return messages[activeFilter.value] || t('chemistOrders.emptyAll')
}

const getEmptyDescription = () => {
  const descriptions = {
    all: t('chemistOrders.emptyAllDesc'),
    pending: t('chemistOrders.emptyPendingDesc'),
    active: t('chemistOrders.emptyActiveDesc'),
    completed: t('chemistOrders.emptyCompletedDesc')
  }
  return descriptions[activeFilter.value] || ''
}

const handleAcceptOrder = async (order) => {
  const patientName = order.patient?.name || t('common.unknown')
  const diagnosis = order.prescription?.diagnosis || t('common.unknown')

  if (!confirm(t('chemistOrders.acceptConfirm', { id: order.id, patient: patientName, diagnosis }))) {
    return
  }

  processingOrder.value = order.id
  const result = await orderStore.acceptOrder(order.id)

  if (result.success) {
    showToast(t('chemistOrders.toastAccepted'), 'success')
  } else {
    showToast(result.error || t('chemistOrders.toastError'), 'error')
  }

  processingOrder.value = null
}

const updateOrderStatus = async (order, status) => {
  const statusLabel = t(`status.${status}`)

  if (!confirm(t('chemistOrders.updateConfirm', { id: order.id, status: statusLabel }))) {
    return
  }

  processingOrder.value = order.id
  const result = await orderStore.updateOrderStatus(order.id, status)

  if (result.success) {
    showToast(t('chemistOrders.toastStatusUpdated'), 'success')
  } else {
    showToast(result.error || t('chemistOrders.toastError'), 'error')
  }

  processingOrder.value = null
}

const viewOrderDetails = (order) => {
  selectedOrder.value = order
}

const showToast = (message, type) => {
  if (window.showToast) {
    window.showToast(message, type)
  } else {
    alert(message)
  }
}

onMounted(() => {
  orderStore.fetchOrders()
})
</script>

<style scoped>
.orders-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  animation: fadeIn 0.5s ease;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 20px;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 36px;
  margin-bottom: 8px;
}

.page-description {
  color: #7f8c8d;
  font-size: 16px;
}

.orders-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-item {
  background: white;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-align: center;
  border-top: 4px solid #3498db;
}

.stat-pending { border-top-color: #f39c12; }
.stat-active { border-top-color: #3498db; }
.stat-completed { border-top-color: #27ae60; }

.stat-value {
  font-size: 42px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filters-card {
  margin-bottom: 30px;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.card-title {
  font-size: 24px;
  color: #2c3e50;
  font-weight: 600;
}

.filter-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 10px 20px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #666;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-tab:hover {
  border-color: #3498db;
  color: #3498db;
}

.filter-tab.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.filter-count {
  background: rgba(255, 255, 255, 0.3);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
}

.filter-tab.active .filter-count {
  background: rgba(255, 255, 255, 0.3);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #777;
}

.spinner-large {
  width: 60px;
  height: 60px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state-large {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.empty-illustration {
  margin-bottom: 24px;
}

.empty-icon {
  width: 54px;
  height: 54px;
  margin: 0 auto;
  opacity: 0.5;
  color: #2c3e50;
}

.empty-state-large h2 {
  color: #2c3e50;
  font-size: 28px;
  margin-bottom: 12px;
}

.empty-state-large p {
  color: #7f8c8d;
  font-size: 16px;
}

.orders-timeline {
  position: relative;
  padding-left: 40px;
}

.orders-timeline::before {
  content: '';
  position: absolute;
  left: 14px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to bottom, #3498db, #9b59b6);
}

.order-timeline-item {
  position: relative;
  margin-bottom: 32px;
}

.timeline-marker {
  position: absolute;
  left: -33px;
  top: 20px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: white;
  border: 4px solid #3498db;
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.marker-pending { border-color: #f39c12; }
.marker-accepted { border-color: #3498db; }
.marker-preparing { border-color: #e74c3c; }
.marker-ready { border-color: #27ae60; }
.marker-completed { border-color: #27ae60; background: #27ae60; }
.marker-cancelled { border-color: #95a5a6; background: #95a5a6; }

.order-card-enhanced {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.order-card-enhanced:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.order-header-enhanced {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 24px;
}

.order-id-section {
  display: flex;
  gap: 16px;
  align-items: center;
}

.order-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

.order-icon-svg {
  width: 24px;
  height: 24px;
  color: white;
}

.order-id-section h3 {
  color: #2c3e50;
  font-size: 22px;
  margin-bottom: 4px;
}

.order-date {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 4px;
}

.patient-name {
  color: #3498db;
  font-size: 14px;
  font-weight: 500;
}

.status-badge-large {
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.status-pending { background: #fff3cd; color: #856404; }
.status-accepted { background: #d1ecf1; color: #0c5460; }
.status-preparing { background: #f8d7da; color: #721c24; }
.status-ready { background: #d4edda; color: #155724; }
.status-completed { background: #d4edda; color: #155724; }
.status-cancelled { background: #f5c6cb; color: #721c24; }

.order-progress {
  margin-bottom: 28px;
}

.progress-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.5s ease;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #95a5a6;
  font-weight: 600;
}

.progress-labels span.active {
  color: #3498db;
}

.order-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.detail-card {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  gap: 14px;
  align-items: start;
}

.detail-icon {
  width: 44px;
  height: 44px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.detail-icon-svg {
  width: 20px;
  height: 20px;
  color: #2c3e50;
}

.detail-content h4 {
  color: #2c3e50;
  font-size: 14px;
  margin-bottom: 6px;
  font-weight: 600;
}

.detail-content p {
  color: #555;
  font-size: 14px;
  margin-bottom: 4px;
}

.detail-content small {
  color: #7f8c8d;
  font-size: 12px;
}

.medicines-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.medicines-title {
  color: #2c3e50;
  font-size: 16px;
  margin-bottom: 16px;
  font-weight: 600;
}

.medicines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.medicine-card {
  background: white;
  padding: 16px;
  border-radius: 10px;
  border-left: 4px solid #3498db;
}

.medicine-header {
  margin-bottom: 10px;
}

.medicine-header strong {
  color: #2c3e50;
  font-size: 15px;
}

.medicine-details {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.medicine-tag {
  background: #e8f4f8;
  color: #2c3e50;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.medicine-instructions {
  font-size: 13px;
  color: #777;
  font-style: italic;
  margin-top: 8px;
}

.order-notes {
  background: #fff3cd;
  color: #856404;
  padding: 14px;
  border-radius: 10px;
  font-size: 14px;
  margin-bottom: 20px;
}

.order-actions {
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 2px solid #f5f7fa;
  flex-wrap: wrap;
}

.btn-action-outline,
.btn-action-primary,
.btn-action-success {
  flex: 1;
  min-width: 150px;
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-action-outline {
  background: white;
  border: 2px solid #3498db;
  color: #3498db;
}

.btn-action-outline:hover {
  background: #3498db;
  color: white;
}

.btn-action-primary {
  background: #3498db;
  color: white;
}

.btn-action-primary:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.btn-action-success {
  background: #27ae60;
  color: white;
}

.btn-action-success:hover {
  background: #229954;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
}

.btn-action-outline:disabled,
.btn-action-primary:disabled,
.btn-action-success:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  animation: slideUp 0.3s ease;
}

.modal-header-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 20px 20px 0 0;
}

.modal-header-gradient h2 {
  font-size: 26px;
}

.modal-close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  font-size: 32px;
  color: white;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-body-large {
  padding: 24px 28px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 28px;
  }

  .orders-stats {
    grid-template-columns: 1fr;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tabs {
    flex-direction: column;
  }

  .filter-tab {
    width: 100%;
    justify-content: center;
  }

  .orders-timeline {
    padding-left: 20px;
  }

  .order-actions {
    flex-direction: column;
  }

  .btn-action-outline,
  .btn-action-primary,
  .btn-action-success {
    width: 100%;
  }
}
</style>
