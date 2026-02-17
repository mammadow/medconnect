<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">{{ t('auth.registerTitle') }}</h1>
      
      <div class="role-selector">
        <button 
          v-for="r in roles" 
          :key="r.value"
          @click="selectedRole = r.value"
          :class="['role-btn', { active: selectedRole === r.value }]"
        >
          {{ r.label }}
        </button>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label class="form-label">{{ t('auth.name') }}</label>
          <input v-model="form.name" type="text" class="form-input" required />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('auth.email') }}</label>
          <input v-model="form.email" type="email" class="form-input" required />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('auth.phone') }}</label>
          <input v-model="form.number" type="tel" class="form-input" required />
        </div>

        <div v-if="selectedRole === 'doctor'" class="form-group">
          <label class="form-label">{{ t('auth.specialization') }}</label>
          <input v-model="form.specialization" type="text" class="form-input" />
        </div>

        <div v-if="selectedRole === 'chemist'" class="form-group">
          <label class="form-label">{{ t('auth.pharmacyName') }}</label>
          <input v-model="form.pharmacy_name" type="text" class="form-input" />
        </div>

        <div v-if="selectedRole === 'patient' || selectedRole === 'chemist'" class="form-group">
          <label class="form-label">{{ t('auth.address') }}</label>
          <input v-model="form.address" type="text" class="form-input" />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('auth.password') }}</label>
          <input v-model="form.password" type="password" class="form-input" required />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? t('auth.registering') : t('auth.registerButton') }}
        </button>
      </form>

      <div class="auth-footer">
        <p>{{ t('auth.haveAccount') }} <router-link to="/login">{{ t('auth.goToLogin') }}</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n'

const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n()

const roles = computed(() => ([
  { value: 'patient', label: t('roles.patient') },
  { value: 'doctor', label: t('roles.doctor') },
  { value: 'chemist', label: t('roles.chemist') }
]))

const selectedRole = ref('patient')
const form = ref({
  name: '',
  email: '',
  number: '',
  password: '',
  specialization: '',
  pharmacy_name: '',
  address: ''
})
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
  
  const result = await authStore.register(selectedRole.value, form.value)
  
  if (result.success) {
    const pendingRoles = ['doctor', 'chemist']
    success.value = pendingRoles.includes(selectedRole.value)
      ? t('auth.registerPending')
      : t('auth.registerSuccess')
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    error.value = result.error
  }
  
  loading.value = false
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  padding: 20px;
}

.auth-card {
  background: var(--surface);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 500px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
  max-height: 90vh;
  overflow-y: auto;
}

.auth-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 32px;
}

.role-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.role-btn {
  flex: 1;
  padding: 12px;
  border: 1px solid var(--border-color);
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
  color: #475569;
}

.role-btn:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.15);
}

.role-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  box-shadow: 0 10px 18px rgba(37, 99, 235, 0.25);
}

.auth-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--secondary-color);
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  transition: border 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  border-left: 4px solid #e74c3c;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  border-left: 4px solid #27ae60;
}

.btn-full {
  width: 100%;
  justify-content: center;
  margin-top: 10px;
}

.auth-footer {
  text-align: center;
  color: #777;
  margin-top: 20px;
}

.auth-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
