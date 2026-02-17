<template>
  <div class="prescription-card">
    <div class="card-header">
      <div>
        <h3>{{ prescription.diagnosis }}</h3>
        <p class="date">{{ formatDate(prescription.date) }}</p>
      </div>
      <span :class="['status-badge', `status-${prescription.status}`]">
        {{ getStatusLabel(prescription.status) }}
      </span>
    </div>

    <div class="card-body">
      <div v-if="prescription.doctor" class="info-row">
        <strong>{{ t('prescription.doctorLabel') }}:</strong> {{ prescription.doctor.name }}
        <span v-if="prescription.doctor.specialization">({{ prescription.doctor.specialization }})</span>
      </div>

      <div v-if="prescription.patient" class="info-row">
        <strong>{{ t('prescription.patientLabel') }}:</strong> {{ prescription.patient.name }}
      </div>

      <div v-if="prescription.notes" class="notes">
        <strong>{{ t('prescription.notesLabel') }}:</strong> {{ prescription.notes }}
      </div>

      <div v-if="prescription.medicines && prescription.medicines.length" class="medicines">
        <h4>{{ t('prescription.medicinesLabel') }}:</h4>
        <ul>
          <li v-for="med in prescription.medicines" :key="med.id">
            <strong>{{ med.name }}</strong>
            <div class="medicine-details">
              <span v-if="med.dosage">{{ t('prescription.dosageLabel') }}: {{ med.dosage }}</span>
              <span v-if="med.frequency">{{ t('prescription.frequencyLabel') }}: {{ med.frequency }}</span>
              <span v-if="med.duration">{{ t('prescription.durationLabel') }}: {{ med.duration }}</span>
            </div>
            <p v-if="med.instructions" class="instructions">{{ med.instructions }}</p>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="showActions" class="card-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from '../i18n'

defineProps({
  prescription: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
})

const { t, dateLocale } = useI18n()

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString(dateLocale.value, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusLabel = (status) => t(`status.${status}`)
</script>

<style scoped>
.prescription-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f5f7fa;
}

.card-header h3 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.date {
  color: #777;
  font-size: 14px;
}

.card-body {
  margin-bottom: 15px;
}

.info-row {
  margin-bottom: 12px;
  color: #555;
}

.notes {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  margin: 15px 0;
}

.medicines {
  margin-top: 20px;
}

.medicines h4 {
  margin-bottom: 12px;
  color: #2c3e50;
}

.medicines ul {
  list-style: none;
}

.medicines li {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.medicine-details {
  display: flex;
  gap: 15px;
  margin-top: 8px;
  font-size: 14px;
  color: #666;
  flex-wrap: wrap;
}

.instructions {
  margin-top: 8px;
  color: #777;
  font-size: 14px;
  font-style: italic;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 2px solid #f5f7fa;
}
</style>
