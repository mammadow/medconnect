<template>
  <div class="orders-page">
    <div class="page-header">
      <div>
        <h1>{{ t('patientOrders.title') }}</h1>
        <p class="page-description">{{ t('patientOrders.subtitle') }}</p>
      </div>

      <button @click="showCreateOrder = true" class="btn-create-order">
        <span class="btn-icon">
          <AppIcon name="add" class="btn-icon-svg" />
        </span>
        <span>{{ t('patientOrders.newOrder') }}</span>
      </button>
    </div>

    <div class="orders-stats">
      <div class="stat-item">
        <div class="stat-value">{{ orders.length }}</div>
        <div class="stat-label">{{ t('patientOrders.statsTotal') }}</div>
      </div>
      <div class="stat-item stat-pending">
        <div class="stat-value">{{ pendingOrders }}</div>
        <div class="stat-label">{{ t('patientOrders.statsPending') }}</div>
      </div>
      <div class="stat-item stat-active">
        <div class="stat-value">{{ activeOrders }}</div>
        <div class="stat-label">{{ t('patientOrders.statsActive') }}</div>
      </div>
      <div class="stat-item stat-completed">
        <div class="stat-value">{{ completedOrders }}</div>
        <div class="stat-label">{{ t('patientOrders.statsCompleted') }}</div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>{{ t('patientOrders.loading') }}</p>
    </div>

    <div v-else-if="orders.length === 0" class="empty-state-large">
      <div class="empty-illustration">
        <AppIcon name="order" class="empty-icon" />
      </div>
      <h2>{{ t('patientOrders.emptyTitle') }}</h2>
      <p>{{ t('patientOrders.emptyText') }}</p>
      <button @click="showCreateOrder = true" class="btn btn-primary btn-large">
        {{ t('patientOrders.createFirst') }}
      </button>
    </div>

    <div v-else class="orders-timeline">
      <div
        v-for="order in orders"
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
              </div>
            </div>
            <span :class="['status-badge-large', `status-${order.status}`]">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <div class="order-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: getProgressWidth(order.status) }"></div>
            </div>
            <div class="progress-labels">
              <span :class="{ active: isStepActive(order.status, 'pending') }">{{ t('patientOrders.sentStep') }}</span>
              <span :class="{ active: isStepActive(order.status, 'accepted') }">{{ t('patientOrders.acceptedStep') }}</span>
              <span :class="{ active: isStepActive(order.status, 'preparing') }">{{ t('patientOrders.preparingStep') }}</span>
              <span :class="{ active: isStepActive(order.status, 'ready') }">{{ t('patientOrders.readyStep') }}</span>
              <span :class="{ active: isStepActive(order.status, 'completed') }">{{ t('patientOrders.completedStep') }}</span>
            </div>
          </div>

          <div class="order-details-grid">
            <div v-if="order.prescription" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="prescription" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('patientOrders.prescriptionCard') }}</h4>
                <p>{{ order.prescription.diagnosis }}</p>
                <small v-if="order.prescription.medicines">
                  {{ order.prescription.medicines.length }} {{ t('prescription.medicinesLabel') }}
                </small>
              </div>
            </div>

            <div v-if="order.chemist" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="pharmacy" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('patientOrders.pharmacyCard') }}</h4>
                <p>{{ order.chemist.pharmacy_name || order.chemist.name }}</p>
                <small v-if="order.chemist.address">{{ order.chemist.address }}</small>
              </div>
            </div>

            <div v-if="order.delivery_address" class="detail-card">
              <div class="detail-icon">
                <AppIcon name="location" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('patientOrders.deliveryCard') }}</h4>
                <p>{{ order.delivery_address }}</p>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon">
                <AppIcon name="update" class="detail-icon-svg" />
              </div>
              <div class="detail-content">
                <h4>{{ t('patientOrders.lastUpdate') }}</h4>
                <p>{{ formatDateTime(order.updated_at) }}</p>
              </div>
            </div>
          </div>

          <div v-if="order.notes" class="order-notes">
            <strong>{{ t('patientOrders.notes') }}:</strong> {{ order.notes }}
          </div>

          <div class="order-actions">
            <button @click="viewOrderDetails(order)" class="btn-action-outline">
              {{ t('patientOrders.viewDetails') }}
            </button>
            <button
              v-if="order.status === 'pending'"
              @click="cancelOrder(order)"
              class="btn-action-danger"
            >
              {{ t('patientOrders.cancelOrder') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedOrder" class="modal-overlay" @click="selectedOrder = null">
      <div class="modal-details" @click.stop>
        <div class="modal-header-gradient">
          <h2>{{ t('patientOrders.detailsTitle') }} #{{ selectedOrder.id }}</h2>
          <button @click="selectedOrder = null" class="modal-close-btn">&times;</button>
        </div>

        <div class="modal-body-large">
          <OrderCard
            :order="selectedOrder"
            :show-chemist-info="true"
            :show-actions="false"
          />
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="startReorder(selectedOrder)">
            {{ t('patientOrders.reorder') }}
          </button>
          <button type="button" class="btn btn-secondary" @click="selectedOrder = null">
            {{ t('patientOrders.close') }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showCreateOrder" class="modal-overlay" @click="showCreateOrder = false">
      <div class="modal-create-order" @click.stop>
        <div class="modal-header-gradient">
          <h2>{{ t('patientOrders.modalTitle') }}</h2>
          <button @click="showCreateOrder = false" class="modal-close-btn">&times;</button>
        </div>

        <div class="modal-body-large">
          <form @submit.prevent="handleCreateOrder" class="order-form">
            <div class="form-section">
              <label class="form-label-enhanced">
                <span class="label-icon">
                  <AppIcon name="prescription" class="label-icon-svg" />
                </span>
                {{ t('patientOrders.selectPrescription') }} *
              </label>
              <select v-model="orderForm.prescription_id" class="form-select-enhanced" required>
                <option value="">{{ t('patientOrders.selectPrescriptionPlaceholder') }}</option>
                <option
                  v-for="prescription in availablePrescriptions"
                  :key="prescription.id"
                  :value="prescription.id"
                >
                  {{ t('patientPrescriptions.prescriptionLabel') }} #{{ prescription.id }} - {{ prescription.diagnosis }}
                </option>
              </select>
            </div>

            <div class="form-section">
              <label class="form-label-enhanced">
                <span class="label-icon">
                  <AppIcon name="pharmacy" class="label-icon-svg" />
                </span>
                {{ t('patientOrders.selectChemist') }}
              </label>
              <select v-model="orderForm.chemist_id" class="form-select-enhanced">
                <option value="">{{ t('patientOrders.selectChemistPlaceholder') }}</option>
                <option
                  v-for="chemist in chemists"
                  :key="chemist.id"
                  :value="chemist.id"
                >
                  {{ chemist.pharmacy_name || chemist.name }}
                  <span v-if="chemist.address"> - {{ chemist.address }}</span>
                </option>
              </select>
              <small class="form-hint">{{ t('patientOrders.chemistHint') }}</small>
            </div>

            <div class="form-section">
              <label class="form-label-enhanced">
                <span class="label-icon">
                  <AppIcon name="location" class="label-icon-svg" />
                </span>
                {{ t('patientOrders.deliveryAddress') }} *
              </label>
              <textarea
                v-model="orderForm.delivery_address"
                class="form-textarea-enhanced"
                rows="3"
                :placeholder="t('patientOrders.deliveryPlaceholder')"
                required
              ></textarea>
            </div>

            <div class="form-section">
              <label class="form-label-enhanced">
                <span class="label-icon">
                  <AppIcon name="note" class="label-icon-svg" />
                </span>
                {{ t('patientOrders.orderNotes') }}
              </label>
              <textarea
                v-model="orderForm.notes"
                class="form-textarea-enhanced"
                rows="3"
                :placeholder="t('patientOrders.notesPlaceholder')"
              ></textarea>
            </div>

            <div v-if="orderError" class="error-message-enhanced">
              {{ orderError }}
            </div>

            <div class="form-actions-enhanced">
              <button type="submit" class="btn btn-primary btn-large" :disabled="orderLoading">
                <span v-if="orderLoading">{{ t('patientOrders.creating') }}</span>
                <span v-else>{{ t('patientOrders.createOrder') }}</span>
              </button>
              <button type="button" @click="showCreateOrder = false" class="btn btn-secondary btn-large">
                {{ t('patientOrders.cancel') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useOrderStore } from '../../stores/order'
import { usePrescriptionStore } from '../../stores/prescription'
import { chemistApi } from '../../services/api'
import { useI18n } from '../../i18n'
import AppIcon from '../../components/AppIcon.vue'
import OrderCard from '../../components/OrderCard.vue'

const route = useRoute()
const orderStore = useOrderStore()
const prescriptionStore = usePrescriptionStore()
const { t, dateLocale } = useI18n()

const showCreateOrder = ref(false)
const selectedOrder = ref(null)
const chemists = ref([])
const orderForm = ref({
  prescription_id: '',
  chemist_id: '',
  delivery_address: '',
  notes: ''
})
const orderError = ref('')
const orderLoading = ref(false)

const orders = computed(() => orderStore.orders)
const loading = computed(() => orderStore.loading)
const prescriptions = computed(() => prescriptionStore.prescriptions)

const availablePrescriptions = computed(() => {
  return prescriptions.value.filter(p => p.status === 'active')
})

const pendingOrders = computed(() => {
  return orders.value.filter(o => o.status === 'pending').length
})

const activeOrders = computed(() => {
  return orders.value.filter(o => ['accepted', 'preparing', 'ready'].includes(o.status)).length
})

const completedOrders = computed(() => {
  return orders.value.filter(o => o.status === 'completed').length
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
    pending: '20%',
    accepted: '40%',
    preparing: '60%',
    ready: '80%',
    completed: '100%',
    cancelled: '0%'
  }
  return progress[status] || '0%'
}

const isStepActive = (currentStatus, step) => {
  const steps = ['pending', 'accepted', 'preparing', 'ready', 'completed']
  const currentIndex = steps.indexOf(currentStatus)
  const stepIndex = steps.indexOf(step)
  return stepIndex <= currentIndex
}

const handleCreateOrder = async () => {
  orderError.value = ''
  orderLoading.value = true

  const result = await orderStore.createOrder(orderForm.value)

  if (result.success) {
    window.showToast(t('patientOrders.toastCreated'), 'success')
    showCreateOrder.value = false
    orderForm.value = {
      prescription_id: '',
      chemist_id: '',
      delivery_address: '',
      notes: ''
    }
  } else {
    orderError.value = result.error
  }

  orderLoading.value = false
}

const viewOrderDetails = (order) => {
  selectedOrder.value = order
}

const startReorder = (order) => {
  showCreateOrder.value = true
  selectedOrder.value = null
  orderForm.value = {
    prescription_id: order.prescription?.id || '',
    chemist_id: order.chemist?.id || '',
    delivery_address: order.delivery_address || '',
    notes: ''
  }
}

const cancelOrder = async (order) => {
  if (!confirm(t('patientOrders.cancelConfirm'))) return

  const result = await orderStore.updateOrderStatus(order.id, 'cancelled')
  if (result.success) {
    window.showToast(t('patientOrders.toastCancelled'), 'success')
  } else {
    window.showToast(t('patientOrders.toastError'), 'error')
  }
}

const loadChemists = async () => {
  try {
    const response = await chemistApi.getAll()
    chemists.value = response.data
  } catch (error) {
    console.error('Failed to load chemists:', error)
  }
}

watch(() => route.query.prescription_id, (newId) => {
  if (newId) {
    orderForm.value.prescription_id = parseInt(newId)
    showCreateOrder.value = true
  }
}, { immediate: true })

onMounted(async () => {
  await orderStore.fetchOrders()
  await prescriptionStore.fetchPrescriptions()
  await loadChemists()
})
</script>

<style scoped>
.orders-page {
  max-width: 1200px;
  margin: 0 auto;
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

.btn-create-order {
  padding: 14px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-icon-svg {
  width: 18px;
  height: 18px;
}

.btn-create-order:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.orders-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
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

.empty-icon {
  width: 54px;
  height: 54px;
  margin: 0 auto;
  color: #2c3e50;
  opacity: 0.5;
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
}

.status-badge-large {
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

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

.btn-action-outline,
.btn-action-danger {
  flex: 1;
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
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

.btn-action-danger {
  background: white;
  border: 2px solid #e74c3c;
  color: #e74c3c;
}

.btn-action-danger:hover {
  background: #e74c3c;
  color: white;
}

.modal-create-order {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 0.3s;
}

.modal-details {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 0.3s;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  max-height: 65vh;
  overflow-y: auto;
}

.modal-footer {
  padding: 20px 32px;
  border-top: 2px solid #f5f7fa;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  background: #f8f9fa;
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label-enhanced {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: #2c3e50;
  font-size: 16px;
}

.label-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.label-icon-svg {
  width: 18px;
  height: 18px;
  color: #2c3e50;
}

.form-select-enhanced,
.form-textarea-enhanced {
  padding: 14px 18px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s;
  font-family: inherit;
}

.form-select-enhanced:focus,
.form-textarea-enhanced:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.1);
}

.form-hint {
  color: #7f8c8d;
  font-size: 13px;
  font-style: italic;
}

.error-message-enhanced {
  background: #fee;
  color: #c33;
  padding: 14px;
  border-radius: 10px;
  border-left: 4px solid #e74c3c;
}

.form-actions-enhanced {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.btn-large {
  padding: 14px 32px;
  font-size: 16px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
