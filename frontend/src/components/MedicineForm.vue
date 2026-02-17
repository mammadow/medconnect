<template>
  <div class="medicine-form">
    <div class="form-header">
      <div>
        <h3>{{ t('doctor.medicines') }}</h3>
        <p class="subtitle">{{ t('doctor.medicineSubtitle') }}</p>
      </div>
      <button
        v-if="!readonly"
        type="button"
        class="btn btn-secondary add-btn"
        :disabled="!canAddMore"
        @click="addMedicine"
      >
        + {{ t('doctor.addMedicine') }}
      </button>
    </div>

    <div v-if="!localMedicines.length" class="empty-state">
      <p>{{ t('doctor.emptyMedicines') }}</p>
      <button v-if="!readonly" type="button" class="btn btn-primary" @click="addMedicine">
        {{ t('doctor.addFirstMedicine') }}
      </button>
    </div>

    <div
      v-for="(medicine, index) in localMedicines"
      :key="index"
      class="medicine-card"
    >
      <div class="medicine-header">
        <div class="title">
          <span class="pill">#{{ index + 1 }}</span>
          <h4>{{ t('doctor.medicine') }} {{ index + 1 }}</h4>
        </div>
        <button
          v-if="!readonly"
          type="button"
          class="btn-remove"
          @click="removeMedicine(index)"
        >
          x
        </button>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">{{ t('doctor.medicineName') }} *</label>
          <input
            v-model="medicine.name"
            type="text"
            class="form-input"
            :placeholder="t('doctor.medicineNamePlaceholder')"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('doctor.dosage') }}</label>
          <input
            v-model="medicine.dosage"
            type="text"
            class="form-input"
            :placeholder="t('doctor.dosagePlaceholder')"
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">{{ t('doctor.frequency') }}</label>
          <input
            v-model="medicine.frequency"
            type="text"
            class="form-input"
            :placeholder="t('doctor.frequencyPlaceholder')"
          />
        </div>

        <div class="form-group">
          <label class="form-label">{{ t('doctor.duration') }}</label>
          <input
            v-model="medicine.duration"
            type="text"
            class="form-input"
            :placeholder="t('doctor.durationPlaceholder')"
          />
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">{{ t('doctor.instructions') }}</label>
        <textarea
          v-model="medicine.instructions"
          class="form-textarea"
          :placeholder="t('doctor.instructionsPlaceholder')"
          rows="3"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useI18n } from '../i18n'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 10
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const { t } = useI18n()

const createBlankMedicine = () => ({
  name: '',
  dosage: '',
  frequency: '',
  duration: '',
  instructions: ''
})

const localMedicines = ref([])

watch(
  () => props.modelValue,
  (value) => {
    localMedicines.value = (value || []).map((item) => ({
      ...createBlankMedicine(),
      ...item
    }))
  },
  { immediate: true }
)

watch(
  localMedicines,
  (value) => {
    emit('update:modelValue', value)
    emit('change', value)
  },
  { deep: true }
)

const canAddMore = computed(() => {
  if (props.readonly) return false
  if (!props.maxItems) return true
  return localMedicines.value.length < props.maxItems
})

const addMedicine = () => {
  if (!canAddMore.value) return
  localMedicines.value.push(createBlankMedicine())
}

const removeMedicine = (index) => {
  if (props.readonly) return
  localMedicines.value.splice(index, 1)
}
</script>

<style scoped>
.medicine-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.form-header h3 {
  color: var(--secondary-color);
  margin-bottom: 6px;
}

.subtitle {
  color: #777;
  font-size: 14px;
}

.add-btn {
  align-self: center;
}

.medicine-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.medicine-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pill {
  background: #eef2ff;
  color: #5c6bc0;
  padding: 6px 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 13px;
}

.medicine-header h4 {
  margin: 0;
  color: var(--secondary-color);
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.btn-remove:hover {
  transform: translateY(-1px);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 12px;
}

.form-textarea {
  min-height: 80px;
  resize: vertical;
}
</style>
