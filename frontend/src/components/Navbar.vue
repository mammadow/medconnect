<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-brand">
        <div class="brand-mark" aria-hidden="true">
          <img src="/favicon.ico" alt="" />
        </div>
        <div class="brand-text">
          <h2>MedConnect</h2>
          <p>Connected care, simplified workflows</p>
        </div>
      </router-link>

      <div class="navbar-links">
        <router-link to="/" class="nav-link">{{ t('nav.home') }}</router-link>
        <router-link to="/about" class="nav-link">{{ t('nav.about') }}</router-link>
        <router-link to="/contact" class="nav-link">{{ t('nav.contact') }}</router-link>

        <template v-if="isAuthenticated">
          <router-link to="/profile" class="nav-link">{{ t('nav.profile') }}</router-link>
          <template v-if="userRole === 'doctor'">
            <router-link to="/doctor/dashboard" class="nav-link">{{ t('nav.doctor') }}</router-link>
            <router-link to="/doctor/prescriptions/create" class="nav-link">{{ t('nav.newPrescription') }}</router-link>
          </template>
          <template v-else-if="userRole === 'patient'">
            <router-link to="/patient/dashboard" class="nav-link">{{ t('nav.patient') }}</router-link>
            <router-link to="/patient/prescriptions" class="nav-link">{{ t('nav.prescriptions') }}</router-link>
            <router-link to="/patient/orders" class="nav-link">{{ t('nav.orders') }}</router-link>
          </template>
          <template v-else-if="userRole === 'chemist'">
            <router-link to="/chemist/dashboard" class="nav-link">{{ t('nav.chemist') }}</router-link>
            <router-link to="/chemist/orders" class="nav-link">{{ t('nav.orders') }}</router-link>
          </template>
          <template v-else-if="userRole === 'admin'">
            <router-link to="/admin/dashboard" class="nav-link">{{ t('nav.admin') }}</router-link>
          </template>
        </template>
      </div>

      <div class="navbar-actions">
        <div class="lang-switch">
          <div class="lang-select-wrapper" @click.stop="toggleLangMenu">
            <button type="button" class="lang-select" :aria-label="t('nav.language')">
              {{ currentLangLabel }}
            </button>
            <div v-if="isLangOpen" class="lang-menu">
              <button
                v-for="lang in languages"
                :key="lang.value"
                type="button"
                class="lang-option"
                :class="{ active: lang.value === selectedLocale }"
                @click.stop="setLanguage(lang.value)"
              >
                {{ lang.label }}
              </button>
            </div>
          </div>
        </div>
        <template v-if="isAuthenticated">
          <div class="user-chip">
            <div class="user-name">{{ userName }}</div>
            <div class="user-role">{{ getRoleLabel(userRole) }}</div>
          </div>
          <button @click="handleLogout" class="nav-btn ghost">{{ t('nav.logout') }}</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-btn ghost">{{ t('nav.signIn') }}</router-link>
          <router-link to="/register" class="nav-btn solid">{{ t('nav.getStarted') }}</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n'

const router = useRouter()
const authStore = useAuthStore()
const { t, locale, setLocale, languages } = useI18n()

const selectedLocale = computed({
  get: () => locale.value,
  set: (value) => setLocale(value)
})

const isLangOpen = ref(false)

const currentLangLabel = computed(() => {
  const match = languages.find((lang) => lang.value === selectedLocale.value)
  return match ? match.label : selectedLocale.value
})

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userRole = computed(() => authStore.user?.role || '')
const userName = computed(() => authStore.user?.name || '')

const getRoleLabel = (role) => {
  const labels = {
    doctor: t('roles.doctor'),
    patient: t('roles.patient'),
    chemist: t('roles.chemist'),
    admin: t('roles.admin')
  }
  return labels[role] || role
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const toggleLangMenu = () => {
  isLangOpen.value = !isLangOpen.value
}

const setLanguage = (value) => {
  selectedLocale.value = value
  isLangOpen.value = false
}

const handleOutsideClick = () => {
  isLangOpen.value = false
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
})
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 40px rgba(11, 19, 36, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(11, 19, 36, 0.08);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 24px;
  height: 72px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  color: #fff;
  display: grid;
  place-items: center;
  font-weight: 700;
  letter-spacing: 1px;
  overflow: hidden;
}

.brand-mark img {
  width: 28px;
  height: 28px;
  object-fit: contain;
  filter: drop-shadow(0 6px 12px rgba(15, 23, 42, 0.2));
}

.brand-text h2 {
  color: var(--secondary-color);
  font-size: 20px;
  margin-bottom: 4px;
}

.brand-text p {
  color: #6b7b7a;
  font-size: 13px;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
}

.nav-link {
  text-decoration: none;
  color: #4b5563;
  font-weight: 600;
  padding: 10px 14px;
  border-radius: 10px;
  transition: all 0.2s ease;
  letter-spacing: 0.1px;
}

.nav-link:hover {
  background: var(--surface-alt);
  color: var(--secondary-color);
}

.nav-link.router-link-active {
  background: rgba(15, 118, 110, 0.12);
  color: var(--secondary-color);
  border: 1px solid rgba(15, 118, 110, 0.2);
}

  .navbar-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

.lang-select {
  appearance: none;
  background:
    linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(20, 184, 166, 0.08)),
    var(--surface);
  border: 1px solid rgba(15, 118, 110, 0.25);
  border-radius: 999px;
  padding: 8px 36px 8px 14px;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.6px;
  color: var(--secondary-color);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 10px 18px rgba(15, 118, 110, 0.12);
  min-width: 64px;
  text-align: left;
}

.lang-select:hover {
  border-color: rgba(15, 118, 110, 0.4);
  box-shadow: 0 12px 22px rgba(15, 118, 110, 0.16);
}

.lang-select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.18), 0 12px 22px rgba(15, 118, 110, 0.16);
}

.lang-select-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.lang-select-wrapper::after {
  content: '▾';
  position: absolute;
  right: 12px;
  color: rgba(15, 23, 42, 0.6);
  font-size: 12px;
  pointer-events: none;
}

.lang-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 120px;
  background: var(--surface);
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 18px 40px rgba(11, 19, 36, 0.16);
  border: 1px solid rgba(15, 118, 110, 0.18);
  display: grid;
  gap: 6px;
  z-index: 200;
}

.lang-option {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 8px 12px;
  text-align: left;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.4px;
  color: var(--secondary-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.lang-option:hover {
  background: rgba(15, 118, 110, 0.08);
  border-color: rgba(15, 118, 110, 0.18);
}

.lang-option.active {
  background: rgba(15, 118, 110, 0.14);
  border-color: rgba(15, 118, 110, 0.26);
  color: var(--primary-dark);
}

.nav-btn {
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 700;
  text-decoration: none;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  letter-spacing: 0.2px;
  cursor: pointer;
}

.nav-btn.solid {
  background: linear-gradient(135deg, var(--primary-color), #14b8a6);
  color: #fff;
  box-shadow: 0 12px 25px rgba(15, 118, 110, 0.35);
  border: none;
}

.nav-btn.solid:hover {
  transform: translateY(-1px);
  box-shadow: 0 18px 28px rgba(15, 118, 110, 0.3);
}

.nav-btn.ghost {
  background: var(--surface-alt);
  color: var(--secondary-color);
  border-color: var(--border-color);
}

.nav-btn.ghost:hover {
  background: #e7ece6;
}

.user-chip {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  padding-right: 8px;
  border-right: 1px solid var(--border-color);
}

.user-name {
  font-weight: 700;
  color: var(--secondary-color);
}

.user-role {
  color: #6b7b7a;
  font-size: 13px;
}

@media (max-width: 960px) {
  .navbar-container {
    flex-wrap: wrap;
    height: auto;
    padding: 12px 16px;
    gap: 12px;
  }

  .navbar-links {
    width: 100%;
    order: 3;
    flex-wrap: wrap;
    gap: 10px;
  }

  .navbar-actions {
    margin-left: auto;
  }
}
</style>
