<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">{{ t('auth.adminLoginTitle') }}</h1>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label">{{ t('auth.email') }}</label>
          <input
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="admin@example.com"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('auth.password') }}</label>
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            :placeholder="t('auth.adminPasswordPlaceholder')"
            required
          />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? t('auth.signingIn') : t('auth.signIn') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useI18n } from '../../i18n'

const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n()

const form = ref({
  email: '',
  password: ''
})
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  const result = await authStore.login('admin', form.value)

  if (result.success) {
    router.push('/admin/dashboard')
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
  max-width: 420px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.auth-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 32px;
}

.auth-form {
  margin-bottom: 10px;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 10px;
  margin-top: 12px;
  border-left: 4px solid #e74c3c;
}

.btn-full {
  width: 100%;
  justify-content: center;
  margin-top: 10px;
}
</style>
