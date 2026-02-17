<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>{{ t('doctor.dashboardTitle') }}</h1>
      <router-link to="/doctor/prescriptions/create" class="btn btn-primary">
        + {{ t('doctor.newPrescription') }}
      </router-link>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <AppIcon name="prescription" class="stat-icon-svg" />
        </div>
        <div class="stat-info">
          <h3>{{ prescriptions.length }}</h3>
          <p>{{ t('doctor.totalPrescriptions') }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <AppIcon name="check" class="stat-icon-svg" />
        </div>
        <div class="stat-info">
          <h3>{{ activePrescriptions }}</h3>
          <p>{{ t('doctor.activePrescriptions') }}</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">{{ t('doctor.recentPrescriptions') }}</h2>
      </div>
      
      <div v-if="loading" class="loading">{{ t('doctor.loading') }}</div>
      
      <div v-else-if="prescriptions.length === 0" class="empty-state">
        <AppIcon name="prescription" class="empty-state-icon" />
        <p class="empty-state-text">{{ t('doctor.emptyTitle') }}</p>
        <router-link to="/doctor/prescriptions/create" class="btn btn-primary">
          {{ t('doctor.createFirst') }}
        </router-link>
      </div>
      
      <div v-else>
        <PrescriptionCard 
          v-for="prescription in prescriptions" 
          :key="prescription.id"
          :prescription="prescription"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePrescriptionStore } from '../../stores/prescription'
import PrescriptionCard from '../../components/PrescriptionCard.vue'
import { useI18n } from '../../i18n'
import AppIcon from '../../components/AppIcon.vue'

const { t } = useI18n()
const prescriptionStore = usePrescriptionStore()
const prescriptions = computed(() => prescriptionStore.prescriptions)
const loading = computed(() => prescriptionStore.loading)

const activePrescriptions = computed(() => {
  return prescriptions.value.filter((p) => p.status === 'active').length
})

onMounted(() => {
  prescriptionStore.fetchPrescriptions()
})
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #2c3e50;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-svg {
  width: 26px;
  height: 26px;
  color: #2c3e50;
}

.empty-state-icon {
  width: 56px;
  height: 56px;
  margin-bottom: 12px;
  color: #2c3e50;
}

.stat-info h3 {
  font-size: 36px;
  color: #3498db;
  margin-bottom: 5px;
}

.stat-info p {
  color: #777;
  font-size: 14px;
}
</style>
