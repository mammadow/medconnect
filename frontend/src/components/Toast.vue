<template>
  <transition name="toast">
    <div v-if="message" :class="['toast', `toast-${type}`]">
      <div class="toast-content">
        <span class="toast-icon">
          <AppIcon :name="iconName" class="toast-icon-svg" />
        </span>
        <span class="toast-message">{{ message }}</span>
        <button @click="$emit('close')" class="toast-close">&times;</button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import AppIcon from './AppIcon.vue'

const { message, type } = defineProps({
  message: String,
  type: {
    type: String,
    default: 'success'
  }
})

defineEmits(['close'])

const iconName = computed(() => {
  const icons = {
    success: 'check',
    error: 'info',
    warning: 'pending',
    info: 'info'
  }
  return icons[type] || 'info'
})
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  min-width: 300px;
  max-width: 500px;
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.toast-success {
  background: #27ae60;
  color: white;
}

.toast-error {
  background: #e74c3c;
  color: white;
}

.toast-warning {
  background: #f39c12;
  color: white;
}

.toast-info {
  background: #3498db;
  color: white;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.toast-icon-svg {
  width: 16px;
  height: 16px;
  color: currentColor;
}

.toast-message {
  flex: 1;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.toast-close:hover {
  opacity: 1;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
