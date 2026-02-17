<template>
  <div class="page">
    <header class="page-hero">
      <p class="eyebrow">{{ t('contact.eyebrow') }}</p>
      <h1>{{ t('contact.title') }}</h1>
      <p>{{ t('contact.subtitle') }}</p>
    </header>

    <section class="contact-grid">
      <div class="card">
        <h3>{{ t('contact.sendTitle') }}</h3>
        <form @submit.prevent="handleSubmit" class="form">
          <label>
            {{ t('contact.fullName') }}
            <input v-model="form.name" type="text" required />
          </label>
          <label>
            {{ t('auth.email') }}
            <input v-model="form.email" type="email" required />
          </label>
          <label>
            {{ t('contact.roleLabel') }}
            <select v-model="form.role">
              <option value="doctor">{{ t('roles.doctor') }}</option>
              <option value="patient">{{ t('roles.patient') }}</option>
              <option value="chemist">{{ t('roles.chemist') }}</option>
              <option value="other">{{ t('roles.other') }}</option>
            </select>
          </label>
          <label>
            {{ t('contact.messageLabel') }}
            <textarea v-model="form.message" rows="4" required></textarea>
          </label>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? t('contact.sending') : t('contact.sendButton') }}
          </button>
          <p v-if="feedback" class="feedback">{{ feedback }}</p>
        </form>
      </div>

      <div class="card info">
        <h3>{{ t('contact.otherWays') }}</h3>
        <div class="info-item">
          <h4>{{ t('contact.supportTitle') }}</h4>
          <p>support@medconnect.app</p>
          <p>{{ t('contact.supportText') }}</p>
        </div>
        <div class="info-item">
          <h4>{{ t('contact.salesTitle') }}</h4>
          <p>onboarding@medconnect.app</p>
          <p>{{ t('contact.salesText') }}</p>
        </div>
        <div class="info-item">
          <h4>{{ t('contact.officeTitle') }}</h4>
          <p>{{ t('contact.officeText') }}</p>
          <p>{{ t('contact.officeHours') }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

const form = ref({
  name: '',
  email: '',
  role: 'doctor',
  message: ''
})

const feedback = ref('')
const submitting = ref(false)

const handleSubmit = () => {
  submitting.value = true
  feedback.value = t('contact.feedback')

  if (typeof window !== 'undefined' && typeof window.showToast === 'function') {
    window.showToast(t('contact.toast'))
  }

  setTimeout(() => {
    submitting.value = false
  }, 800)
}
</script>

<style scoped>
.page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 20px 80px;
}

.page-hero {
  background: linear-gradient(135deg, #f8fbff, #edf4ff);
  color: #0f172a;
  padding: 26px;
  border-radius: 16px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow);
  display: grid;
  gap: 10px;
}

.page-hero h1 {
  font-size: 30px;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  margin-top: 26px;
}

.card {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  border: 1px solid #e4ebf7;
  box-shadow: var(--shadow-soft);
}

.form {
  display: grid;
  gap: 12px;
}

label {
  font-weight: 600;
  color: #0f172a;
  display: grid;
  gap: 6px;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #dbe1e8;
  font-size: 15px;
}

textarea {
  resize: vertical;
}

.feedback {
  color: #16a34a;
  font-weight: 600;
}

.info h4 {
  margin-bottom: 4px;
}

.info-item {
  background: #f7faff;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #e4ebf7;
  margin-top: 10px;
}
</style>
