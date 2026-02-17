<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">{{ t('auth.loginTitle') }}</h1>
      
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

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label">{{ t('auth.email') }}</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="form-input"
            :placeholder="t('auth.emailPlaceholder')"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('auth.password') }}</label>
          <input 
            v-model="form.password" 
            type="password" 
            class="form-input"
            :placeholder="t('auth.passwordPlaceholder')"
            required
          />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="pendingApproval" class="info-message">
          {{ t('auth.pendingApprovalNotice') }}
        </div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? t('auth.signingIn') : t('auth.signIn') }}
        </button>
      </form>

      <div class="auth-footer">
        <p>{{ t('auth.noAccount') }} <router-link to="/register">{{ t('auth.goToRegister') }}</router-link></p>
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
  email: '',
  password: ''
})
const error = ref('')
const pendingApproval = ref(false)
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  pendingApproval.value = false
  loading.value = true
  
  const result = await authStore.login(selectedRole.value, form.value)
  
  if (result.success) {
    if (selectedRole.value === 'doctor') {
      router.push('/doctor/dashboard')
    } else if (selectedRole.value === 'patient') {
      router.push('/patient/dashboard')
    } else if (selectedRole.value === 'chemist') {
      router.push('/chemist/dashboard')
    }
  } else {
    const message = result.error || 'Login failed'
    if (message === 'Account pending admin approval') {
      pendingApproval.value = true
    } else if (message === 'User not found') {
      error.value = t('auth.errors.userNotFound')
    } else if (message === 'Incorrect password') {
      error.value = t('auth.errors.incorrectPassword')
    } else {
      error.value = t('auth.errors.loginFailed')
    }
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
  max-width: 450px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
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
  transform: translateY(-1px);
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

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 10px;
  margin-top: 12px;
  border-left: 4px solid #e74c3c;
}

.info-message {
  background: #e0ecff;
  color: #1d4ed8;
  padding: 12px;
  border-radius: 10px;
  margin-top: 12px;
  border-left: 4px solid #2563eb;
}

.btn-full {
  width: 100%;
  justify-content: center;
  margin-top: 10px;
}

.auth-footer {
  text-align: center;
  color: #777;
}
</style>
