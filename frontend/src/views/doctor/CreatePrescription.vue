<template>
  <div class="create-prescription">
    <h1>{{ t('doctor.createTitle') }}</h1>

    <form @submit.prevent="handleSubmit" class="prescription-form">
      <div class="card">
        <h3>{{ t('doctor.selectPatient') }}</h3>
        
        <div class="form-group">
          <label class="form-label">{{ t('doctor.searchPatientLabel') }}</label>
          <input 
            v-model="searchQuery"
            @input="searchPatients"
            type="text"
            class="form-input"
            :placeholder="t('doctor.searchPatientPlaceholder')"
          />
          
          <div v-if="searchResults.length > 0" class="search-results">
            <div 
              v-for="patient in searchResults" 
              :key="patient.id"
              @click="selectPatient(patient)"
              class="search-result-item"
            >
              <strong>{{ patient.name }}</strong>
              <span>{{ patient.email }}</span>
            </div>
          </div>
        </div>

        <div v-if="selectedPatient" class="selected-patient">
          <strong>{{ t('doctor.selectedPatient') }}:</strong> {{ selectedPatient.name }} ({{ selectedPatient.email }})
        </div>
      </div>

      <div class="card">
        <h3>{{ t('doctor.prescriptionInfo') }}</h3>
        
        <div class="form-group">
          <label class="form-label">{{ t('doctor.diagnosis') }} *</label>
          <textarea 
            v-model="form.diagnosis"
            class="form-textarea"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('doctor.notes') }}</label>
          <textarea 
            v-model="form.notes"
            class="form-textarea"
          ></textarea>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>{{ t('doctor.medicines') }}</h3>
          <button type="button" @click="addMedicine" class="btn btn-secondary">
            + {{ t('doctor.addMedicine') }}
          </button>
        </div>

        <div v-for="(medicine, index) in form.medicines" :key="index" class="medicine-item">
          <div class="medicine-header">
            <h4>{{ t('doctor.medicine') }} {{ index + 1 }}</h4>
            <button type="button" @click="removeMedicine(index)" class="btn-remove">x</button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">{{ t('doctor.medicineName') }} *</label>
              <input v-model="medicine.name" type="text" class="form-input" required />
            </div>

            <div class="form-group">
              <label class="form-label">{{ t('doctor.dosage') }}</label>
              <input v-model="medicine.dosage" type="text" class="form-input" placeholder="500mg" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">{{ t('doctor.frequency') }}</label>
              <input v-model="medicine.frequency" type="text" class="form-input" placeholder="3x" />
            </div>

            <div class="form-group">
              <label class="form-label">{{ t('doctor.duration') }}</label>
              <input v-model="medicine.duration" type="text" class="form-input" placeholder="7" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">{{ t('doctor.instructions') }}</label>
            <textarea v-model="medicine.instructions" class="form-textarea"></textarea>
          </div>
        </div>

        <div v-if="form.medicines.length === 0" class="empty-medicines">
          <p>{{ t('doctor.emptyMedicines') }}</p>
        </div>
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="loading || !selectedPatient">
          {{ loading ? t('doctor.saving') : t('doctor.savePrescription') }}
        </button>
        <router-link to="/doctor/dashboard" class="btn btn-secondary">{{ t('doctor.cancel') }}</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePrescriptionStore } from '../../stores/prescription'
import { patientApi } from '../../services/api'
import { useI18n } from '../../i18n'

const router = useRouter()
const prescriptionStore = usePrescriptionStore()
const { t } = useI18n()

const searchQuery = ref('')
const searchResults = ref([])
const selectedPatient = ref(null)
const form = ref({
  diagnosis: '',
  notes: '',
  patient_id: null,
  medicines: []
})
const error = ref('')
const loading = ref(false)

let searchTimeout = null

const searchPatients = () => {
  clearTimeout(searchTimeout)
  
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await patientApi.search(searchQuery.value)
      searchResults.value = response.data
    } catch (err) {
      console.error('Search failed:', err)
    }
  }, 300)
}

const selectPatient = (patient) => {
  selectedPatient.value = patient
  form.value.patient_id = patient.id
  searchResults.value = []
  searchQuery.value = ''
}

const addMedicine = () => {
  form.value.medicines.push({
    name: '',
    dosage: '',
    frequency: '',
    duration: '',
    instructions: ''
  })
}

const removeMedicine = (index) => {
  form.value.medicines.splice(index, 1)
}

const handleSubmit = async () => {
  if (!selectedPatient.value) {
    error.value = t('doctor.errors.selectPatient')
    return
  }

  if (form.value.medicines.length === 0) {
    error.value = t('doctor.errors.addMedicine')
    return
  }

  error.value = ''
  loading.value = true

  const result = await prescriptionStore.createPrescription(form.value)

  if (result.success) {
    window.showToast(t('doctor.toastCreated'), 'success')
    router.push('/doctor/dashboard')
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.create-prescription {
  max-width: 900px;
  margin: 0 auto;
}

.create-prescription h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.prescription-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-results {
  position: absolute;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 2px solid #ddd;
  border-top: none;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 10;
}

.search-result-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  transition: background 0.2s;
}

.search-result-item:hover {
  background: #f8f9fa;
}

.selected-patient {
  background: #d4edda;
  color: #155724;
  padding: 12px;
  border-radius: 8px;
  margin-top: 10px;
}

.medicine-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.medicine-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.empty-medicines {
  text-align: center;
  padding: 40px;
  color: #999;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}
</style>
