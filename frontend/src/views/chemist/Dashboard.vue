<template>
  <div class="dashboard">
    <header class="dash-head">
      <div>
        <p class="eyebrow">{{ t('chemist.dashboardEyebrow') }}</p>
        <h1>{{ t('chemist.dashboardTitle') }}</h1>
        <p class="sub">{{ t('chemist.dashboardSubtitle') }}</p>
      </div>
      <router-link to="/chemist/orders" class="btn btn-primary">{{ t('chemist.viewOrders') }}</router-link>
    </header>

    <section class="card">
      <h3>{{ t('chemist.quickActionsTitle') }}</h3>
      <ul class="actions">
        <li>{{ t('chemist.quickAction1') }}</li>
        <li>{{ t('chemist.quickAction2') }}</li>
        <li>{{ t('chemist.quickAction3') }}</li>
      </ul>
      <router-link to="/chemist/orders" class="btn btn-secondary">{{ t('chemist.goToOrders') }}</router-link>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from '../../i18n'

const { t } = useI18n()
</script>

<style scoped>
.dashboard {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 0;
}

.dash-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.dash-head h1 {
  margin: 4px 0;
}

.sub {
  color: #6b7280;
}

.card {
  padding: 18px;
}

.actions {
  margin: 12px 0 16px;
  padding-left: 18px;
  color: #374151;
  display: grid;
  gap: 6px;
}
</style>
