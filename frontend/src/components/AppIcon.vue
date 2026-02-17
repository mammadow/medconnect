<template>
  <svg
    :class="['app-icon', $attrs.class]"
    :width="size"
    :height="size"
    :viewBox="icon.viewBox"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <path v-for="(d, idx) in icon.paths" :key="idx" :d="d" />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [Number, String],
    default: 20
  }
})

const icons = {
  add: {
    viewBox: '0 0 24 24',
    paths: ['M12 5v14', 'M5 12h14']
  },
  prescription: {
    viewBox: '0 0 24 24',
    paths: ['M7 3h7l5 5v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z', 'M14 3v5h5', 'M9 14h6', 'M9 17h6']
  },
  order: {
    viewBox: '0 0 24 24',
    paths: ['M4 7h16l-1.5 12.5a1 1 0 0 1-1 .9H6.5a1 1 0 0 1-1-.9L4 7z', 'M9 7a3 3 0 0 1 6 0']
  },
  pharmacy: {
    viewBox: '0 0 24 24',
    paths: ['M12 6v12', 'M6 12h12', 'M4 4h16v16H4z']
  },
  calendar: {
    viewBox: '0 0 24 24',
    paths: ['M4 7h16', 'M7 3v4', 'M17 3v4', 'M5 7h14v12H5z']
  },
  doctor: {
    viewBox: '0 0 24 24',
    paths: ['M12 12a4 4 0 1 0-4-4', 'M4 21a8 8 0 0 1 16 0']
  },
  note: {
    viewBox: '0 0 24 24',
    paths: ['M6 3h9l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z', 'M14 3v5h5', 'M8 13h8', 'M8 16h8']
  },
  medicine: {
    viewBox: '0 0 24 24',
    paths: ['M7 17l10-10', 'M7 7a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6-6z']
  },
  location: {
    viewBox: '0 0 24 24',
    paths: ['M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z', 'M12 9a2 2 0 1 0 0 4 2 2 0 0 0 0-4z']
  },
  update: {
    viewBox: '0 0 24 24',
    paths: ['M21 12a9 9 0 1 1-3-6.7', 'M21 3v6h-6']
  },
  info: {
    viewBox: '0 0 24 24',
    paths: ['M12 8h.01', 'M11 12h2v6', 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z']
  },
  check: {
    viewBox: '0 0 24 24',
    paths: ['M5 13l4 4L19 7']
  },
  pending: {
    viewBox: '0 0 24 24',
    paths: ['M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z', 'M12 7v6l4 2']
  },
  patient: {
    viewBox: '0 0 24 24',
    paths: ['M12 12a4 4 0 1 0-4-4', 'M5 21a7 7 0 0 1 14 0']
  }
}

const icon = computed(() => icons[props.name] || icons.info)
</script>

<style scoped>
.app-icon {
  display: block;
}
</style>
