<template>
  <div class="order-card">
    <div class="order-header">
      <div class="order-info">
        <h3>{{ t('order.orderLabel') }} #{{ order.id }}</h3>
        <p class="order-date">{{ formatDate(order.created_at) }}</p>
      </div>
      <span :class="['status-badge', `status-${order.status}`]">
        {{ getStatusLabel(order.status) }}
      </span>
    </div>

    <div class="order-body">
      <div v-if="order.prescription" class="section">
        <h4>{{ t('order.prescriptionInfo') }}</h4>
        <div class="prescription-summary">
          <p><strong>{{ t('order.diagnosis') }}:</strong> {{ order.prescription.diagnosis }}</p>
          <p v-if="order.prescription.doctor">
            <strong>{{ t('order.doctor') }}:</strong> {{ order.prescription.doctor.name }}
            <span v-if="order.prescription.doctor.specialization">
              ({{ order.prescription.doctor.specialization }})
            </span>
          </p>
          <p v-if="order.prescription.notes">
            <strong>{{ t('order.notes') }}:</strong> {{ order.prescription.notes }}
          </p>
        </div>

        <div v-if="order.prescription.medicines && order.prescription.medicines.length" class="medicines-list">
          <h5>{{ t('prescription.medicinesLabel') }}:</h5>
          <div v-for="med in order.prescription.medicines" :key="med.id" class="medicine-item">
            <div class="medicine-name">{{ med.name }}</div>
            <div class="medicine-details">
              <span v-if="med.dosage">{{ t('prescription.dosageLabel') }}: {{ med.dosage }}</span>
              <span v-if="med.frequency">{{ t('prescription.frequencyLabel') }}: {{ med.frequency }}</span>
              <span v-if="med.duration">{{ t('prescription.durationLabel') }}: {{ med.duration }}</span>
            </div>
            <p v-if="med.instructions" class="medicine-instructions">
              {{ med.instructions }}
            </p>
          </div>
        </div>
      </div>

      <div v-if="order.patient && showPatientInfo" class="section">
        <h4>{{ t('order.patientInfo') }}</h4>
        <p><strong>{{ t('order.name') }}:</strong> {{ order.patient.name }}</p>
        <p><strong>{{ t('order.phone') }}:</strong> {{ order.patient.number }}</p>
        <p><strong>{{ t('order.email') }}:</strong> {{ order.patient.email }}</p>
      </div>

      <div v-if="order.chemist && showChemistInfo" class="section">
        <h4>{{ t('order.chemistInfo') }}</h4>
        <p><strong>{{ t('order.name') }}:</strong> {{ order.chemist.name }}</p>
        <p v-if="order.chemist.pharmacy_name">
          <strong>{{ t('order.pharmacy') }}:</strong> {{ order.chemist.pharmacy_name }}
        </p>
        <p><strong>{{ t('order.phone') }}:</strong> {{ order.chemist.number }}</p>
        <p v-if="order.chemist.address">
          <strong>{{ t('order.address') }}:</strong> {{ order.chemist.address }}
        </p>
      </div>

      <div v-if="order.delivery_address" class="section">
        <h4>{{ t('order.deliveryAddress') }}</h4>
        <p>{{ order.delivery_address }}</p>
      </div>

      <div v-if="order.notes" class="section">
        <h4>{{ t('order.notes') }}</h4>
        <p>{{ order.notes }}</p>
      </div>
    </div>

    <div v-if="showActions" class="order-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from '../i18n'

const props = defineProps({
  order: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showPatientInfo: {
    type: Boolean,
    default: false
  },
  showChemistInfo: {
    type: Boolean,
    default: false
  }
})

const { t, dateLocale } = useI18n()

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
</script>

<style scoped>
.order-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f5f7fa;
}

.order-info h3 {
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 20px;
}

.order-date {
  color: #777;
  font-size: 14px;
}

.order-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
}

.section h4 {
  color: #2c3e50;
  margin-bottom: 12px;
  font-size: 16px;
}

.section h5 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 14px;
}

.section p {
  color: #555;
  line-height: 1.6;
  margin-bottom: 8px;
}

.prescription-summary {
  margin-bottom: 15px;
}

.medicines-list {
  margin-top: 15px;
}

.medicine-item {
  background: white;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 10px;
  border-left: 4px solid #3498db;
}

.medicine-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.medicine-details {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.medicine-details span {
  background: #e8f4f8;
  padding: 4px 10px;
  border-radius: 4px;
}

.medicine-instructions {
  font-size: 13px;
  color: #777;
  font-style: italic;
  margin-top: 8px;
}

.order-actions {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 2px solid #f5f7fa;
  display: flex;
  gap: 12px;
}
</style>
