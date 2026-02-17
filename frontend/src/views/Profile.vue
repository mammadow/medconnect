<template>
  <div class="profile-page fade-in">
    <header class="profile-head">
      <div>
        <p class="eyebrow">{{ t('profile.eyebrow') }}</p>
        <h1>{{ t('profile.title') }}</h1>
        <p class="sub">{{ t('profile.subtitle') }}</p>
      </div>
      <div v-if="role" class="status-pill" :class="approvalClass">
        {{ approvalLabel }}
      </div>
    </header>

    <div v-if="error" class="error-banner">{{ error }}</div>
    <div v-if="success" class="success-banner">{{ success }}</div>

    <section class="card">
      <form @submit.prevent="saveProfile" class="profile-form">
        <div class="grid grid-2">
          <div class="form-group">
            <label class="form-label">{{ t('auth.name') }}</label>
            <input v-model="form.name" type="text" class="form-input" required />
          </div>

          <div class="form-group" v-if="showNumber">
            <label class="form-label">{{ t('auth.phone') }}</label>
            <input v-model="form.number" type="tel" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">{{ t('auth.email') }}</label>
            <input v-model="form.email" type="email" class="form-input" required />
          </div>

          <div class="form-group" v-if="role === 'doctor'">
            <label class="form-label">{{ t('auth.specialization') }}</label>
            <input v-model="form.specialization" type="text" class="form-input" />
          </div>

          <div class="form-group" v-if="role === 'chemist'">
            <label class="form-label">{{ t('auth.pharmacyName') }}</label>
            <input v-model="form.pharmacy_name" type="text" class="form-input" />
          </div>

          <div class="form-group" v-if="role === 'patient' || role === 'chemist'">
            <label class="form-label">{{ t('auth.address') }}</label>
            <input v-model="form.address" type="text" class="form-input" />
          </div>

          <div class="form-group" v-if="role === 'patient'">
            <label class="form-label">{{ t('auth.dateOfBirth') }}</label>
            <input v-model="form.date_of_birth" type="date" class="form-input" />
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? t('profile.saving') : t('profile.save') }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { profileApi } from '../services/api'
import { useI18n } from '../i18n'

const authStore = useAuthStore()
const { t } = useI18n()

const form = ref({
  name: '',
  email: '',
  number: '',
  specialization: '',
  pharmacy_name: '',
  address: '',
  date_of_birth: ''
})

const role = ref('')
const approved = ref(true)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref('')

const showNumber = computed(() => ['doctor', 'patient', 'chemist'].includes(role.value))

const approvalLabel = computed(() => {
  if (!['doctor', 'chemist'].includes(role.value)) {
    const labels = {
      doctor: t('roles.doctor'),
      patient: t('roles.patient'),
      chemist: t('roles.chemist'),
      admin: t('roles.admin')
    }
    return labels[role.value] || ''
  }
  return approved.value ? t('profile.statusApproved') : t('profile.statusPending')
})

const approvalClass = computed(() => {
  if (!['doctor', 'chemist'].includes(role.value)) {
    return 'status-neutral'
  }
  return approved.value ? 'status-approved' : 'status-pending'
})

const loadProfile = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await profileApi.get()
    const data = response.data
    role.value = data.role || authStore.user?.role || ''
    approved.value = data.approved !== false
    form.value = {
      name: data.name || '',
      email: data.email || '',
      number: data.number || '',
      specialization: data.specialization || '',
      pharmacy_name: data.pharmacy_name || '',
      address: data.address || '',
      date_of_birth: data.date_of_birth || ''
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load profile.'
  } finally {
    loading.value = false
  }
}

const buildPayload = () => {
  if (role.value === 'doctor') {
    return {
      name: form.value.name,
      email: form.value.email,
      number: form.value.number,
      specialization: form.value.specialization
    }
  }
  if (role.value === 'patient') {
    return {
      name: form.value.name,
      email: form.value.email,
      number: form.value.number,
      address: form.value.address,
      date_of_birth: form.value.date_of_birth || null
    }
  }
  if (role.value === 'chemist') {
    return {
      name: form.value.name,
      email: form.value.email,
      number: form.value.number,
      pharmacy_name: form.value.pharmacy_name,
      address: form.value.address
    }
  }
  return {
    name: form.value.name,
    email: form.value.email
  }
}

const saveProfile = async () => {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    const response = await profileApi.update(buildPayload())
    const user = response.data.user || {}
    authStore.updateUser(user)
    success.value = t('profile.success')
    approved.value = user.approved !== false
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to update profile.'
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
}

.profile-head h1 {
  margin: 6px 0 6px;
}

.sub {
  color: #64748b;
}

.status-pill {
  padding: 8px 14px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.status-approved {
  background: rgba(22, 163, 74, 0.12);
  color: #15803d;
}

.status-pending {
  background: rgba(245, 158, 11, 0.14);
  color: #b45309;
}

.status-neutral {
  background: rgba(148, 163, 184, 0.2);
  color: #475569;
}

.error-banner,
.success-banner {
  padding: 14px 18px;
  border-radius: 12px;
  font-weight: 600;
}

.error-banner {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.success-banner {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 960px) {
  .profile-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
