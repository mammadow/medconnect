<template>
  <div class="page">
    <header class="page-hero">
      <p class="eyebrow">{{ t('about.eyebrow') }}</p>
      <h1>{{ t('about.title') }}</h1>
      <p>
        {{ t('about.intro') }}
      </p>
    </header>

    <section class="section-grid">
      <div class="panel">
        <h3>{{ t('about.focusTitle') }}</h3>
        <p>
          {{ t('about.focusText') }}
        </p>
      </div>
      <div class="panel">
        <h3>{{ t('about.guideTitle') }}</h3>
        <ul>
          <li v-for="item in guideBullets" :key="item">{{ item }}</li>
        </ul>
      </div>
      <div class="panel">
        <h3>{{ t('about.serveTitle') }}</h3>
        <p>
          {{ t('about.serveText') }}
        </p>
      </div>
    </section>

    <section class="pillars">
      <h2>{{ t('about.pillarsTitle') }}</h2>
      <div class="pillar-grid">
        <div class="pillar">
          <span class="badge">01</span>
          <h4>{{ t('about.pillarConnectedTitle') }}</h4>
          <p>{{ t('about.pillarConnectedText') }}</p>
        </div>
        <div class="pillar">
          <span class="badge">02</span>
          <h4>{{ t('about.pillarTraceTitle') }}</h4>
          <p>{{ t('about.pillarTraceText') }}</p>
        </div>
        <div class="pillar">
          <span class="badge">03</span>
          <h4>{{ t('about.pillarReliableTitle') }}</h4>
          <p>{{ t('about.pillarReliableText') }}</p>
        </div>
      </div>
    </section>

    <section class="timeline">
      <h2>{{ t('about.roadmapTitle') }}</h2>
      <div class="timeline-list">
        <div class="timeline-item">
          <div class="dot"></div>
          <div>
            <h4>{{ t('about.roadmapMessagingTitle') }}</h4>
            <p>{{ t('about.roadmapMessagingText') }}</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="dot"></div>
          <div>
            <h4>{{ t('about.roadmapAnalyticsTitle') }}</h4>
            <p>{{ t('about.roadmapAnalyticsText') }}</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="dot"></div>
          <div>
            <h4>{{ t('about.roadmapRemindersTitle') }}</h4>
            <p>{{ t('about.roadmapRemindersText') }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

const guideBullets = computed(() => t('about.guideBullets') || [])
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 80px;
}

.page-hero {
  background: linear-gradient(135deg, #f8fbff, #edf4ff);
  color: #0f172a;
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow);
  display: grid;
  gap: 12px;
}

.page-hero h1 {
  font-size: 32px;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.panel {
  background: #fff;
  border-radius: 14px;
  padding: 18px;
  border: 1px solid #e4ebf7;
  box-shadow: var(--shadow-soft);
}

.panel h3 {
  margin-bottom: 8px;
  color: #0f172a;
}

.panel p {
  color: #5b6b83;
}

.panel ul {
  padding-left: 18px;
  color: #1f2937;
  display: grid;
  gap: 6px;
}

.pillars {
  margin-top: 40px;
  background: #ffffff;
  color: #0f172a;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e4ebf7;
  box-shadow: var(--shadow);
}

.pillars h2 {
  margin-bottom: 14px;
}

.pillar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
}

.pillar {
  background: #f7faff;
  border: 1px solid #e4ebf7;
  padding: 16px;
  border-radius: 14px;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: rgba(37, 99, 235, 0.12);
  color: #1e3a8a;
  font-weight: 800;
  margin-bottom: 10px;
}

.timeline {
  margin-top: 40px;
}

.timeline h2 {
  margin-bottom: 14px;
}

.timeline-list {
  display: grid;
  gap: 12px;
}

.timeline-item {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: center;
  gap: 10px;
  background: #fff;
  border: 1px solid #e4ebf7;
  padding: 14px;
  border-radius: 12px;
  box-shadow: var(--shadow-soft);
}

.timeline-item h4 {
  margin-bottom: 6px;
}

.timeline-item p {
  color: #5b6b83;
}

.dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  box-shadow: 0 0 0 6px #e0f2fe;
  justify-self: center;
}
</style>
