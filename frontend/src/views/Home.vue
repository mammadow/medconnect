<template>
  <div class="landing">
    <section class="hero fade-in" style="animation-delay: 0s;">
      <div class="hero-copy">
        <p class="eyebrow">{{ t('home.heroEyebrow') }}</p>
        <h1>{{ t('home.heroTitle') }}</h1>
        <p class="lede">
          {{ t('home.heroLead') }}
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn btn-primary">{{ t('home.heroPrimary') }}</router-link>
          <router-link to="/contact" class="btn btn-secondary">{{ t('home.heroSecondary') }}</router-link>
        </div>
        <div class="hero-metrics">
          <div class="metric-card">
            <span class="metric-value">99.9%</span>
            <span class="metric-label">{{ t('home.metrics.uptime') }}</span>
          </div>
          <div class="metric-card">
            <span class="metric-value">2.5k+</span>
            <span class="metric-label">{{ t('home.metrics.prescriptions') }}</span>
          </div>
          <div class="metric-card">
            <span class="metric-value">3</span>
            <span class="metric-label">{{ t('home.metrics.roles') }}</span>
          </div>
        </div>
      </div>

      <div class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="eyebrow">{{ t('home.liveEyebrow') }}</p>
              <h3>{{ t('home.liveTitle') }}</h3>
            </div>
            <span class="status-pill">{{ t('home.liveStatus') }}</span>
          </div>
          <div class="panel-grid">
            <div class="panel-stat">
              <p>{{ t('home.liveStats.newPrescriptions') }}</p>
              <h4>12</h4>
            </div>
            <div class="panel-stat">
              <p>{{ t('home.liveStats.awaitingPickup') }}</p>
              <h4>8</h4>
            </div>
            <div class="panel-stat">
              <p>{{ t('home.liveStats.confirmedPatients') }}</p>
              <h4>21</h4>
            </div>
            <div class="panel-stat">
              <p>{{ t('home.liveStats.ordersCompleted') }}</p>
              <h4>34</h4>
            </div>
          </div>
        </div>

        <div class="panel-card subtle">
          <h4>{{ t('home.workflowTitle') }}</h4>
          <ul class="panel-list">
            <li>
              <span class="dot dot-blue"></span>
              <div>
                <strong>{{ t('home.workflow.doctorTitle') }}</strong>
                <p>{{ t('home.workflow.doctorText') }}</p>
              </div>
            </li>
            <li>
              <span class="dot dot-teal"></span>
              <div>
                <strong>{{ t('home.workflow.patientTitle') }}</strong>
                <p>{{ t('home.workflow.patientText') }}</p>
              </div>
            </li>
            <li>
              <span class="dot dot-indigo"></span>
              <div>
                <strong>{{ t('home.workflow.chemistTitle') }}</strong>
                <p>{{ t('home.workflow.chemistText') }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section fade-in" style="animation-delay: 0.05s;">
      <div class="section-header">
        <p class="eyebrow">{{ t('home.rolesEyebrow') }}</p>
        <h2>{{ t('home.rolesTitle') }}</h2>
        <p class="section-subtitle">{{ t('home.rolesSubtitle') }}</p>
      </div>

      <div class="feature-grid">
        <article class="feature-card">
          <div class="icon-wrap">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="12" cy="7" r="3"></circle>
              <path d="M5 20c1.8-3.6 5-5 7-5s5.2 1.4 7 5"></path>
              <path d="M12 10v4"></path>
              <path d="M10 12h4"></path>
            </svg>
          </div>
          <h3>{{ t('home.featureDoctor.title') }}</h3>
          <p>{{ t('home.featureDoctor.text') }}</p>
          <ul>
            <li v-for="item in doctorBullets" :key="item">{{ item }}</li>
          </ul>
        </article>
        <article class="feature-card">
          <div class="icon-wrap">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="12" cy="8" r="3.2"></circle>
              <path d="M4.5 20c2-4 5-5.5 7.5-5.5s5.5 1.5 7.5 5.5"></path>
            </svg>
          </div>
          <h3>{{ t('home.featurePatient.title') }}</h3>
          <p>{{ t('home.featurePatient.text') }}</p>
          <ul>
            <li v-for="item in patientBullets" :key="item">{{ item }}</li>
          </ul>
        </article>
        <article class="feature-card">
          <div class="icon-wrap">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <rect x="3.5" y="7" width="17" height="10" rx="5"></rect>
              <path d="M12 7v10"></path>
            </svg>
          </div>
          <h3>{{ t('home.featureChemist.title') }}</h3>
          <p>{{ t('home.featureChemist.text') }}</p>
          <ul>
            <li v-for="item in chemistBullets" :key="item">{{ item }}</li>
          </ul>
        </article>
      </div>
    </section>

    <section class="section fade-in" style="animation-delay: 0.1s;">
      <div class="section-header">
        <p class="eyebrow">{{ t('home.howEyebrow') }}</p>
        <h2>{{ t('home.howTitle') }}</h2>
      </div>
      <div class="steps-grid">
        <div class="step-card">
          <span class="step-number">01</span>
          <h4>{{ t('home.steps.createTitle') }}</h4>
          <p>{{ t('home.steps.createText') }}</p>
        </div>
        <div class="step-card">
          <span class="step-number">02</span>
          <h4>{{ t('home.steps.confirmTitle') }}</h4>
          <p>{{ t('home.steps.confirmText') }}</p>
        </div>
        <div class="step-card">
          <span class="step-number">03</span>
          <h4>{{ t('home.steps.fulfillTitle') }}</h4>
          <p>{{ t('home.steps.fulfillText') }}</p>
        </div>
      </div>
    </section>

    <section class="section fade-in" style="animation-delay: 0.15s;">
      <div class="section-header">
        <p class="eyebrow">{{ t('home.trustEyebrow') }}</p>
        <h2>{{ t('home.trustTitle') }}</h2>
        <p class="section-subtitle">{{ t('home.trustSubtitle') }}</p>
      </div>
      <div class="trust-grid">
        <div class="trust-card">
          <h4>{{ t('home.trustCards.secureTitle') }}</h4>
          <p>{{ t('home.trustCards.secureText') }}</p>
        </div>
        <div class="trust-card">
          <h4>{{ t('home.trustCards.auditTitle') }}</h4>
          <p>{{ t('home.trustCards.auditText') }}</p>
        </div>
        <div class="trust-card">
          <h4>{{ t('home.trustCards.reliableTitle') }}</h4>
          <p>{{ t('home.trustCards.reliableText') }}</p>
        </div>
      </div>
    </section>

    <section class="cta fade-in" style="animation-delay: 0.2s;">
      <div class="cta-card">
        <div>
          <p class="eyebrow">{{ t('home.ctaEyebrow') }}</p>
          <h2>{{ t('home.ctaTitle') }}</h2>
          <p>{{ t('home.ctaText') }}</p>
        </div>
        <div class="cta-actions">
          <router-link to="/register" class="btn btn-primary">{{ t('home.ctaPrimary') }}</router-link>
          <router-link to="/about" class="btn btn-secondary">{{ t('home.ctaSecondary') }}</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

const doctorBullets = computed(() => t('home.featureDoctor.bullets') || [])
const patientBullets = computed(() => t('home.featurePatient.bullets') || [])
const chemistBullets = computed(() => t('home.featureChemist.bullets') || [])
</script>

<style scoped>
.landing {
  display: grid;
  gap: 64px;
  padding: 24px 0 80px;
}

.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  padding: 36px;
  background: linear-gradient(135deg, #f8fbff 0%, #edf4ff 55%, #f2f7ff 100%);
  border-radius: 24px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow);
}

.hero-copy {
  display: grid;
  gap: 16px;
}

.hero h1 {
  font-size: 40px;
  line-height: 1.1;
  color: #0f172a;
}

.lede {
  font-size: 18px;
  color: #5b6b83;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.metric-card {
  background: #fff;
  border-radius: 16px;
  padding: 14px 16px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow-soft);
  display: grid;
  gap: 4px;
}

.metric-value {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}

.metric-label {
  color: #5b6b83;
  font-size: 13px;
}

.hero-panel {
  display: grid;
  gap: 16px;
}

.panel-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 18px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow-soft);
}

.panel-card.subtle {
  background: #f7faff;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.status-pill {
  background: rgba(22, 163, 74, 0.12);
  color: #15803d;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 12px;
}

.panel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.panel-stat {
  background: #f3f7ff;
  border-radius: 14px;
  padding: 12px;
  border: 1px solid #e1e9f8;
}

.panel-stat p {
  font-size: 13px;
  color: #5b6b83;
  margin-bottom: 6px;
}

.panel-stat h4 {
  font-size: 20px;
}

.panel-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: grid;
  gap: 12px;
}

.panel-list li {
  display: grid;
  grid-template-columns: 18px 1fr;
  gap: 10px;
  align-items: start;
}

.panel-list p {
  margin: 4px 0 0;
  color: #5b6b83;
  font-size: 13px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 6px;
}

.dot-blue {
  background: #2563eb;
}

.dot-teal {
  background: #0ea5e9;
}

.dot-indigo {
  background: #6366f1;
}

.section {
  display: grid;
  gap: 24px;
}

.section-header {
  text-align: center;
  max-width: 720px;
  margin: 0 auto;
  display: grid;
  gap: 8px;
}

.section-header h2 {
  font-size: 30px;
  color: #0f172a;
}

.section-subtitle {
  color: #5b6b83;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 18px;
}

.feature-card {
  background: #fff;
  border-radius: 18px;
  padding: 20px;
  border: 1px solid #e4ebf7;
  box-shadow: var(--shadow-soft);
  display: grid;
  gap: 12px;
}

.icon-wrap {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: #eef3ff;
  display: grid;
  place-items: center;
  color: #2563eb;
}

.icon-wrap svg {
  width: 28px;
  height: 28px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.feature-card h3 {
  font-size: 20px;
  color: #0f172a;
}

.feature-card p {
  color: #5b6b83;
}

.feature-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
  color: #1f2937;
}

.feature-card ul li::before {
  content: "-";
  color: #2563eb;
  margin-right: 8px;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.step-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #e3ecf8;
  box-shadow: var(--shadow-soft);
  display: grid;
  gap: 8px;
}

.step-number {
  font-weight: 700;
  color: #2563eb;
}

.trust-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.trust-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #e4ebf7;
  box-shadow: var(--shadow-soft);
}

.trust-card p {
  color: #5b6b83;
  margin-top: 6px;
}

.cta-card {
  background: linear-gradient(135deg, #ffffff, #eef3ff);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid #dde7f5;
  box-shadow: var(--shadow);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.cta-card p {
  color: #5b6b83;
}

.cta-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .hero {
    padding: 28px;
  }

  .hero h1 {
    font-size: 32px;
  }
}
</style>
