<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <RouterView />
    </main>
    <Toast 
      v-if="toastMessage" 
      :message="toastMessage" 
      :type="toastType"
      @close="clearToast"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Toast from './components/Toast.vue'

// Toast notification system
const toastMessage = ref('')
const toastType = ref('success')

const showToast = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => {
    clearToast()
  }, 4000)
}

const clearToast = () => {
  toastMessage.value = ''
}

// Make showToast available globally
window.showToast = showToast
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  background:
    radial-gradient(circle at 12% 12%, rgba(15, 118, 110, 0.12), transparent 45%),
    radial-gradient(circle at 88% 6%, rgba(56, 189, 248, 0.12), transparent 40%),
    linear-gradient(180deg, #f8fbfa 0%, #eef3f2 100%);
  color: var(--secondary-color);
}

a {
  color: inherit;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 1.6px;
  font-weight: 700;
  font-size: 12px;
  color: #6b7b7a;
}

#app {
  min-height: 100vh;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 20px 40px;
}
</style>
