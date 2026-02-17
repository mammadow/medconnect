<template>
  <div class="prescriptions-page">
    <div class="page-header">
      <div>
        <h1>{{ t('patientPrescriptions.title') }}</h1>
        <p class="page-description">{{ t('patientPrescriptions.subtitle') }}</p>
      </div>

      <div class="header-actions">
        <div class="filter-group">
          <label>{{ t('patientPrescriptions.statusLabel') }}:</label>
          <select v-model="filterStatus" class="filter-select">
            <option value="all">{{ t('patientPrescriptions.all') }}</option>
            <option value="active">{{ t('status.active') }}</option>
            <option value="fulfilled">{{ t('status.fulfilled') }}</option>
            <option value="cancelled">{{ t('status.cancelled') }}</option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>{{ t('patientPrescriptions.loading') }}</p>
    </div>

    <div v-else-if="filteredPrescriptions.length === 0 && !loading" class="empty-state-large">
      <div class="empty-illustration">
        <AppIcon name="prescription" class="empty-icon" />
        <div class="empty-circle"></div>
      </div>
      <h2>{{ t('patientPrescriptions.emptyTitle') }}</h2>
      <p v-if="filterStatus !== 'all'">{{ t('patientPrescriptions.emptyFiltered') }}</p>
      <p v-else>{{ t('patientPrescriptions.emptyAll') }}</p>
    </div>

    <div v-else class="prescriptions-container">
      <div class="prescriptions-count">
        <span>{{ t('patientPrescriptions.foundCount', { count: filteredPrescriptions.length }) }}</span>
      </div>

      <div class="prescriptions-list">
        <div
          v-for="prescription in filteredPrescriptions"
          :key="prescription.id"
          class="prescription-card-wrapper"
        >
          <div class="prescription-card-enhanced">
            <div class="card-header-enhanced">
              <div class="header-left">
                <div class="prescription-id">
                  <span class="id-label">{{ t('patientPrescriptions.prescriptionLabel') }}</span>
                  <span class="id-number">#{{ prescription.id }}</span>
                </div>
                <div class="prescription-date">
                  <span class="date-icon">
                    <AppIcon name="calendar" class="date-icon-svg" />
                  </span>
                  <span>{{ formatDate(prescription.date) }}</span>
                </div>
              </div>
              <span :class="['status-badge-enhanced', `status-${prescription.status}`]">
                {{ getStatusLabel(prescription.status) }}
              </span>
            </div>

            <div v-if="prescription.doctor" class="doctor-section">
              <div class="doctor-avatar">
                <AppIcon name="doctor" class="doctor-avatar-svg" />
              </div>
              <div class="doctor-info">
                <h4>{{ prescription.doctor.name }}</h4>
                <p v-if="prescription.doctor.specialization">{{ prescription.doctor.specialization }}</p>
                <p v-if="prescription.doctor.number" class="doctor-contact">{{ prescription.doctor.number }}</p>
              </div>
            </div>

            <div class="diagnosis-section">
              <div class="section-label">
                <span class="label-icon">
                  <AppIcon name="prescription" class="label-icon-svg" />
                </span>
                <span>{{ t('patientPrescriptions.diagnosisLabel') }}</span>
              </div>
              <p class="diagnosis-text">{{ prescription.diagnosis }}</p>
            </div>

            <div v-if="prescription.notes" class="notes-section">
              <div class="section-label">
                <span class="label-icon">
                  <AppIcon name="note" class="label-icon-svg" />
                </span>
                <span>{{ t('patientPrescriptions.notesLabel') }}</span>
              </div>
              <p class="notes-text">{{ prescription.notes }}</p>
            </div>

            <div v-if="prescription.medicines && prescription.medicines.length" class="medicines-section">
              <div class="section-label">
                <span class="label-icon">
                  <AppIcon name="medicine" class="label-icon-svg" />
                </span>
                <span>{{ t('patientPrescriptions.medicinesLabel') }} ({{ prescription.medicines.length }})</span>
              </div>

              <div class="medicines-grid">
                <div
                  v-for="medicine in prescription.medicines"
                  :key="medicine.id"
                  class="medicine-card"
                >
                  <div class="medicine-header">
                    <h5>{{ medicine.name }}</h5>
                  </div>
                  <div class="medicine-details">
                    <div v-if="medicine.dosage" class="detail-item">
                      <span class="detail-label">{{ t('prescription.dosageLabel') }}:</span>
                      <span class="detail-value">{{ medicine.dosage }}</span>
                    </div>
                    <div v-if="medicine.frequency" class="detail-item">
                      <span class="detail-label">{{ t('prescription.frequencyLabel') }}:</span>
                      <span class="detail-value">{{ medicine.frequency }}</span>
                    </div>
                    <div v-if="medicine.duration" class="detail-item">
                      <span class="detail-label">{{ t('prescription.durationLabel') }}:</span>
                      <span class="detail-value">{{ medicine.duration }}</span>
                    </div>
                  </div>
                  <p v-if="medicine.instructions" class="medicine-instructions">
                    {{ medicine.instructions }}
                  </p>
                </div>
              </div>
            </div>

            <div class="card-actions-enhanced">
              <button
                @click="createOrder(prescription)"
                class="btn-action btn-primary-action"
                :disabled="prescription.status !== 'active'"
              >
                <span class="btn-icon">
                  <AppIcon name="order" class="btn-icon-svg" />
                </span>
                <span>{{ t('patientPrescriptions.orderButton') }}</span>
              </button>

              <button
                @click="viewDetails(prescription)"
                class="btn-action btn-secondary-action"
              >
                <span class="btn-icon">
                  <AppIcon name="info" class="btn-icon-svg" />
                </span>
                <span>{{ t('patientPrescriptions.detailsButton') }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedPrescription" class="modal-overlay" @click="selectedPrescription = null">
      <div class="modal-large" @click.stop>
        <div class="modal-header-large">
          <h2>{{ t('patientPrescriptions.modalTitle') }}</h2>
          <button @click="selectedPrescription = null" class="modal-close-btn">&times;</button>
        </div>
        <div class="modal-body-large">
          <PrescriptionCard :prescription="selectedPrescription" :show-actions="false" />
        </div>
        <div class="modal-footer">
          <button
            @click="createOrder(selectedPrescription)"
            class="btn btn-primary"
            :disabled="selectedPrescription.status !== 'active'"
          >
            {{ t('patientPrescriptions.orderButton') }}
          </button>
          <button @click="selectedPrescription = null" class="btn btn-secondary">
            {{ t('patientPrescriptions.close') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePrescriptionStore } from '../../stores/prescription'
import PrescriptionCard from '../../components/PrescriptionCard.vue'
import { useI18n } from '../../i18n'
import AppIcon from '../../components/AppIcon.vue'

const router = useRouter()
const prescriptionStore = usePrescriptionStore()
const { t, dateLocale } = useI18n()

const filterStatus = ref('all')
const selectedPrescription = ref(null)

const prescriptions = computed(() => prescriptionStore.prescriptions)
const loading = computed(() => prescriptionStore.loading)

const filteredPrescriptions = computed(() => {
  if (filterStatus.value === 'all') {
    return prescriptions.value
  }
  return prescriptions.value.filter(p => p.status === filterStatus.value)
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString(dateLocale.value, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusLabel = (status) => t(`status.${status}`)

const createOrder = (prescription) => {
  router.push({
    path: '/patient/orders',
    query: { prescription_id: prescription.id }
  })
}

const viewDetails = (prescription) => {
  selectedPrescription.value = prescription
}

onMounted(() => {
  prescriptionStore.fetchPrescriptions()
})
</script>

<style scoped>
.prescriptions-page {
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 40px;
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

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 12px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
}

.filter-select {
  padding: 8px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
  gap: 24px;
}

.spinner-large {
  width: 60px;
  height: 60px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-state-large {
  text-align: center;
  padding: 100px 20px;
}

.empty-illustration {
  position: relative;
  margin-bottom: 32px;
}

.empty-icon {
  width: 54px;
  height: 54px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  color: #2c3e50;
}

.empty-circle {
  position: absolute;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
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

.prescriptions-count {
  margin-bottom: 24px;
  color: #7f8c8d;
  font-size: 15px;
}

.prescriptions-list {
  display: grid;
  gap: 24px;
}

.prescription-card-enhanced {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  transition: all 0.4s ease;
  border: 2px solid transparent;
}

.prescription-card-enhanced:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.15);
  border-color: #3498db;
}

.card-header-enhanced {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f5f7fa;
}

.header-left {
  display: flex;
  gap: 24px;
  align-items: center;
  flex-wrap: wrap;
}

.prescription-id {
  display: flex;
  align-items: center;
  gap: 8px;
}

.id-label {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.id-number {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
}

.prescription-date {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7f8c8d;
  font-size: 15px;
}

.date-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.date-icon-svg {
  width: 16px;
  height: 16px;
}

.status-badge-enhanced {
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.doctor-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
}

.doctor-avatar {
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.doctor-avatar-svg {
  width: 28px;
  height: 28px;
  color: #2c3e50;
}

.doctor-info h4 {
  color: #2c3e50;
  font-size: 20px;
  margin-bottom: 6px;
}

.doctor-info p {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 4px;
}

.doctor-contact {
  color: #3498db;
  font-weight: 500;
}

.diagnosis-section,
.notes-section,
.medicines-section {
  margin-bottom: 24px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-weight: 700;
  color: #2c3e50;
  font-size: 18px;
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

.diagnosis-text,
.notes-text {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #3498db;
  color: #2c3e50;
  line-height: 1.7;
  font-size: 15px;
}

.notes-text {
  border-left-color: #f39c12;
}

.medicines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.medicine-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  border-radius: 14px;
  border: 2px solid #e9ecef;
  transition: all 0.3s;
}

.medicine-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.2);
}

.medicine-header h5 {
  color: #2c3e50;
  font-size: 18px;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e9ecef;
}

.medicine-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.detail-label {
  color: #7f8c8d;
  font-weight: 500;
}

.detail-value {
  color: #2c3e50;
  font-weight: 600;
}

.medicine-instructions {
  background: #fff3cd;
  color: #856404;
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  margin-top: 12px;
}

.card-actions-enhanced {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 2px solid #f5f7fa;
}

.btn-action {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.btn-primary-action {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary-action:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary-action:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary-action {
  background: white;
  color: #2c3e50;
  border: 2px solid #e0e0e0;
}

.btn-secondary-action:hover {
  background: #f8f9fa;
  border-color: #3498db;
  color: #3498db;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-icon-svg {
  width: 16px;
  height: 16px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

.modal-large {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 800px;
  max-height: 85vh;
  overflow: hidden;
  animation: slideUp 0.3s;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header-large {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px;
  border-bottom: 2px solid #f5f7fa;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-header-large h2 {
  font-size: 26px;
}

.modal-close-btn {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  font-size: 28px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.modal-close-btn:hover {
  background: rgba(255,255,255,0.3);
  transform: rotate(90deg);
}

.modal-body-large {
  padding: 32px;
  max-height: 60vh;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
