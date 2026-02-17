<template>
  <div class="admin-dashboard fade-in">
    <header class="admin-hero">
      <div>
        <p class="eyebrow">{{ t('admin.heroEyebrow') }}</p>
        <h1>{{ t('admin.heroTitle') }}</h1>
        <p class="sub">{{ t('admin.heroSubtitle') }}</p>
      </div>
      <div class="hero-actions">
        <button class="btn btn-secondary" @click="loadOverview" :disabled="loading">
          {{ loading ? t('common.loading') : t('admin.refresh') }}
        </button>
      </div>
    </header>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <section class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-foot">{{ stat.note }}</div>
      </div>
    </section>

    <section class="card">
      <div class="card-header">
        <h2 class="card-title">{{ t('admin.pendingTitle') }}</h2>
        <span class="card-meta">{{ t('admin.pendingSubtitle') }}</span>
      </div>
      <div v-if="pendingLoading" class="loading">{{ t('common.loading') }}</div>
      <div v-else class="user-groups">
        <div class="user-group">
          <h3>{{ t('roles.doctor') }}</h3>
          <div v-if="pendingDoctors.length === 0" class="empty-mini">{{ t('admin.noDoctors') }}</div>
          <div v-else class="user-list">
            <div v-for="doctor in pendingDoctors" :key="doctor.id" class="user-row">
              <div>
                <div class="row-title">{{ doctor.name }}</div>
                <div class="row-sub">{{ doctor.email }}</div>
                <div class="row-sub">{{ doctor.number }}</div>
                <div v-if="doctor.specialization" class="row-sub">{{ t('auth.specialization') }}: {{ doctor.specialization }}</div>
                <div v-if="doctor.created_at" class="row-sub">{{ t('admin.labels.joined') }}: {{ formatDate(doctor.created_at) }}</div>
              </div>
              <div class="action-buttons">
                <button
                  class="btn btn-glow-green btn-sm"
                  :disabled="isApproving('doctor', doctor.id)"
                  @click="approveUser('doctor', doctor.id)"
                >
                  {{ isApproving('doctor', doctor.id) ? t('admin.approving') : t('admin.approve') }}
                </button>
                <button
                  class="btn btn-glow-red btn-sm"
                  :disabled="isRefusing('doctor', doctor.id)"
                  @click="refuseUser('doctor', doctor.id)"
                >
                  {{ isRefusing('doctor', doctor.id) ? t('admin.refusing') : t('admin.refuse') }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="user-group">
          <h3>{{ t('roles.chemist') }}</h3>
          <div v-if="pendingChemists.length === 0" class="empty-mini">{{ t('admin.noChemists') }}</div>
          <div v-else class="user-list">
            <div v-for="chemist in pendingChemists" :key="chemist.id" class="user-row">
              <div>
                <div class="row-title">{{ chemist.pharmacy_name || chemist.name }}</div>
                <div class="row-sub">{{ chemist.email }}</div>
                <div class="row-sub">{{ chemist.number }}</div>
                <div v-if="chemist.address" class="row-sub">{{ chemist.address }}</div>
                <div v-if="chemist.created_at" class="row-sub">{{ t('admin.labels.joined') }}: {{ formatDate(chemist.created_at) }}</div>
              </div>
              <div class="action-buttons">
                <button
                  class="btn btn-glow-green btn-sm"
                  :disabled="isApproving('chemist', chemist.id)"
                  @click="approveUser('chemist', chemist.id)"
                >
                  {{ isApproving('chemist', chemist.id) ? t('admin.approving') : t('admin.approve') }}
                </button>
                <button
                  class="btn btn-glow-red btn-sm"
                  :disabled="isRefusing('chemist', chemist.id)"
                  @click="refuseUser('chemist', chemist.id)"
                >
                  {{ isRefusing('chemist', chemist.id) ? t('admin.refusing') : t('admin.refuse') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="grid grid-2">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">{{ t('admin.recentOrders') }}</h2>
          <span class="card-meta">{{ t('admin.lastRecords', { count: limit }) }}</span>
        </div>
        <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
        <div v-else-if="recentOrders.length === 0" class="empty-state">
          <p class="empty-state-text">{{ t('admin.noOrders') }}</p>
        </div>
        <div v-else class="list">
          <div v-for="order in recentOrders" :key="order.id" class="list-row">
            <div class="row-main">
              <div class="row-title">{{ t('admin.labels.order') }} #{{ order.id }}</div>
              <div class="row-sub">
                <span>{{ t('admin.labels.patient') }}: {{ order.patient?.name || '-' }}</span>
                <span v-if="order.chemist">
                  {{ t('admin.labels.chemist') }}: {{ order.chemist.pharmacy_name || order.chemist.name }}
                </span>
              </div>
            </div>
            <div class="row-meta">
              <span :class="['status-badge', `status-${order.status}`]">
                {{ getOrderStatus(order.status) }}
              </span>
              <span class="row-date">{{ formatDate(order.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2 class="card-title">{{ t('admin.recentPrescriptions') }}</h2>
          <span class="card-meta">{{ t('admin.lastRecords', { count: limit }) }}</span>
        </div>
        <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
        <div v-else-if="recentPrescriptions.length === 0" class="empty-state">
          <p class="empty-state-text">{{ t('admin.noPrescriptions') }}</p>
        </div>
        <div v-else class="list">
          <div v-for="prescription in recentPrescriptions" :key="prescription.id" class="list-row">
            <div class="row-main">
              <div class="row-title">{{ t('admin.labels.prescription') }} #{{ prescription.id }}</div>
              <div class="row-sub">
                <span v-if="prescription.doctor">{{ t('admin.labels.doctor') }}: {{ prescription.doctor.name }}</span>
                <span v-if="prescription.patient">{{ t('admin.labels.patient') }}: {{ prescription.patient.name }}</span>
              </div>
            </div>
            <div class="row-meta">
              <span :class="['status-badge', `status-${prescription.status}`]">
                {{ t(`status.${prescription.status}`) }}
              </span>
              <span class="row-date">{{ formatDate(prescription.date) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="card">
      <div class="card-header">
        <h2 class="card-title">{{ t('admin.newestUsers') }}</h2>
        <span class="card-meta">{{ t('admin.latestSignups') }}</span>
      </div>
      <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
      <div v-else class="user-groups">
        <div class="user-group">
          <h3>{{ t('roles.doctor') }}</h3>
          <div v-if="recentDoctors.length === 0" class="empty-mini">{{ t('admin.noDoctors') }}</div>
          <div v-else class="user-list">
            <div v-for="doctor in recentDoctors" :key="doctor.id" class="user-row">
              <div>
                <div class="row-title">{{ doctor.name }}</div>
                <div class="row-sub">{{ doctor.email }}</div>
              </div>
              <div class="row-date">{{ formatDate(doctor.created_at) }}</div>
            </div>
          </div>
        </div>

        <div class="user-group">
          <h3>{{ t('roles.patient') }}</h3>
          <div v-if="recentPatients.length === 0" class="empty-mini">{{ t('admin.noPatients') }}</div>
          <div v-else class="user-list">
            <div v-for="patient in recentPatients" :key="patient.id" class="user-row">
              <div>
                <div class="row-title">{{ patient.name }}</div>
                <div class="row-sub">{{ patient.email }}</div>
              </div>
              <div class="row-date">{{ formatDate(patient.created_at) }}</div>
            </div>
          </div>
        </div>

        <div class="user-group">
          <h3>{{ t('roles.chemist') }}</h3>
          <div v-if="recentChemists.length === 0" class="empty-mini">{{ t('admin.noChemists') }}</div>
          <div v-else class="user-list">
            <div v-for="chemist in recentChemists" :key="chemist.id" class="user-row">
              <div>
                <div class="row-title">{{ chemist.pharmacy_name || chemist.name }}</div>
                <div class="row-sub">{{ chemist.email }}</div>
              </div>
              <div class="row-date">{{ formatDate(chemist.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '../../services/api'
import { useI18n } from '../../i18n'

const { t, dateLocale } = useI18n()

const overview = ref(null)
const loading = ref(false)
const error = ref('')
const pendingLoading = ref(false)
const approving = ref({})
const refusing = ref({})
const limit = 5

const counts = computed(() => overview.value?.counts || {
  doctors: 0,
  patients: 0,
  chemists: 0,
  prescriptions: 0,
  orders: 0,
  pending_doctors: 0,
  pending_chemists: 0
})

const recentOrders = computed(() => overview.value?.recent?.orders || [])
const recentPrescriptions = computed(() => overview.value?.recent?.prescriptions || [])
const recentDoctors = computed(() => overview.value?.recent?.doctors || [])
const recentPatients = computed(() => overview.value?.recent?.patients || [])
const recentChemists = computed(() => overview.value?.recent?.chemists || [])
const pendingDoctors = ref([])
const pendingChemists = ref([])

const stats = computed(() => ([
  { label: t('admin.metrics.doctors'), value: counts.value.doctors, note: t('admin.metrics.providersNote') },
  { label: t('admin.metrics.patients'), value: counts.value.patients, note: t('admin.metrics.patientsNote') },
  { label: t('admin.metrics.chemists'), value: counts.value.chemists, note: t('admin.metrics.chemistsNote') },
  { label: t('admin.metrics.prescriptions'), value: counts.value.prescriptions, note: t('admin.metrics.prescriptionsNote') },
  { label: t('admin.metrics.orders'), value: counts.value.orders, note: t('admin.metrics.ordersNote') },
  { label: t('admin.metrics.pendingDoctors'), value: counts.value.pending_doctors, note: t('admin.metrics.pendingNote') },
  { label: t('admin.metrics.pendingChemists'), value: counts.value.pending_chemists, note: t('admin.metrics.pendingNote') }
]))

const formatDate = (value) => {
  if (!value) return ''
  return new Date(value).toLocaleString(dateLocale.value, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getOrderStatus = (status) => {
  return t(`status.${status}`)
}

const loadOverview = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await adminApi.getOverview({ limit })
    overview.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load admin overview.'
  } finally {
    loading.value = false
  }
}

const loadPending = async () => {
  pendingLoading.value = true
  try {
    const response = await adminApi.getPending()
    pendingDoctors.value = response.data.doctors || []
    pendingChemists.value = response.data.chemists || []
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load pending approvals.'
  } finally {
    pendingLoading.value = false
  }
}

const isApproving = (role, id) => {
  return !!approving.value[`${role}-${id}`]
}

const isRefusing = (role, id) => {
  return !!refusing.value[`${role}-${id}`]
}

const approveUser = async (role, id) => {
  approving.value = { ...approving.value, [`${role}-${id}`]: true }
  try {
    await adminApi.approveUser({ role, id })
    await loadOverview()
    await loadPending()
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to approve user.'
  } finally {
    const updated = { ...approving.value }
    delete updated[`${role}-${id}`]
    approving.value = updated
  }
}

const refuseUser = async (role, id) => {
  refusing.value = { ...refusing.value, [`${role}-${id}`]: true }
  try {
    await adminApi.refuseUser({ role, id })
    await loadOverview()
    await loadPending()
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to refuse user.'
  } finally {
    const updated = { ...refusing.value }
    delete updated[`${role}-${id}`]
    refusing.value = updated
  }
}

onMounted(() => {
  loadOverview()
  loadPending()
})
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.admin-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  padding: 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(14, 165, 233, 0.15));
  border: 1px solid rgba(37, 99, 235, 0.2);
  box-shadow: var(--shadow-soft);
}

.admin-hero h1 {
  font-size: 32px;
  color: #0f172a;
  margin: 6px 0 8px;
}

.sub {
  color: #51607a;
  font-size: 16px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.error-banner {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fecaca;
  padding: 14px 18px;
  border-radius: 12px;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 18px;
}

.stat-card {
  background: var(--surface);
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #edf1f7;
  box-shadow: var(--shadow-soft);
}

.stat-label {
  font-weight: 600;
  color: #5a6b84;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  font-size: 11px;
}

.stat-value {
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
  margin-top: 8px;
}

.stat-foot {
  margin-top: 10px;
  color: #6b7280;
  font-size: 14px;
}

.card-meta {
  color: #6b7280;
  font-size: 14px;
}

.list {
  display: grid;
  gap: 16px;
}

.list-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  border-radius: 14px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

.row-main {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.row-title {
  font-weight: 700;
  color: #0f172a;
}

.row-sub {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #6b7280;
  font-size: 14px;
}

.row-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  min-width: 120px;
}

.row-date {
  color: #6b7280;
  font-size: 13px;
}

.user-groups {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.user-group h3 {
  margin-bottom: 12px;
  color: #0f172a;
}

.user-list {
  display: grid;
  gap: 12px;
}

.user-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn-glow-green {
  background: #16a34a;
  color: #fff;
  border: none;
  box-shadow: 0 0 0 rgba(22, 163, 74, 0.6);
  animation: greenGlow 2s ease-in-out infinite;
}

.btn-glow-red {
  background: #dc2626;
  color: #fff;
  border: none;
  box-shadow: 0 0 0 rgba(220, 38, 38, 0.6);
  animation: redGlow 2s ease-in-out infinite;
}

.btn-glow-green:disabled,
.btn-glow-red:disabled {
  animation: none;
  box-shadow: none;
  opacity: 0.6;
}

.btn-sm {
  padding: 8px 14px;
  font-size: 14px;
}

.empty-mini {
  color: #6b7280;
  font-size: 14px;
}

@keyframes greenGlow {
  0% {
    box-shadow: 0 0 0 rgba(22, 163, 74, 0.3);
  }
  50% {
    box-shadow: 0 0 18px rgba(22, 163, 74, 0.55);
  }
  100% {
    box-shadow: 0 0 0 rgba(22, 163, 74, 0.3);
  }
}

@keyframes redGlow {
  0% {
    box-shadow: 0 0 0 rgba(220, 38, 38, 0.3);
  }
  50% {
    box-shadow: 0 0 18px rgba(220, 38, 38, 0.55);
  }
  100% {
    box-shadow: 0 0 0 rgba(220, 38, 38, 0.3);
  }
}

@media (max-width: 960px) {
  .admin-hero {
    flex-direction: column;
    align-items: flex-start;
  }

  .row-meta {
    align-items: flex-start;
  }
}
</style>
