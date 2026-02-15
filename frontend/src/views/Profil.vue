<template>
  <div class="page-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1>{{ $t('profile.title') }}</h1>
        <p class="subtitle">{{ $t('profile.subtitle') }}</p>
      </div>
    </div>

    <div class="content-section">
      <div class="card fade-in-up">
        <h2><i class="fas fa-history"></i> {{ $t('profile.history') }}</h2>
        <p>{{ $t('profile.history_content') }}</p>
      </div>

      <div class="grid-2">
        <div class="card fade-in-up delay-1">
          <h2><i class="fas fa-eye"></i> {{ $t('profile.vision') }}</h2>
          <p class="vision-text">"{{ $t('profile.vision_content') }}"</p>
        </div>
        <div class="card fade-in-up delay-2">
          <h2><i class="fas fa-bullseye"></i> {{ $t('profile.mission') }}</h2>
          <ul class="check-list">
            <li v-for="(item, index) in $tm('profile.mission_list')" :key="index">{{ item }}</li>
          </ul>
        </div>
      </div>

      <div class="card fade-in-up delay-3">
        <h2><i class="fas fa-star"></i> {{ $t('profile.advantages_title') }}</h2>
        <div class="tags-container">
          <span v-for="(item, index) in $tm('profile.advantages_list')" :key="index" class="tag">
            {{ item }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'

export default {
  name: 'Profil',
  data() {
    return {
      schoolData
    }
  }
}
</script>

<style scoped>
.page-container {
  padding-top: 60px; /* Space for navbar */
  min-height: 100vh;
  background: var(--background);
}

.hero-section {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  padding: 4rem 2rem;
  text-align: center;
  margin-bottom: 2rem;
  border-radius: 0 0 50% 50% / 20px;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.content-section {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1.5rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background: var(--surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .grid-2 {
    grid-template-columns: 1fr 1fr;
  }
}

h2 {
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid var(--primary-light);
  padding-bottom: 0.5rem;
}

.vision-text {
  font-style: italic;
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: center;
  color: var(--text-primary);
}

.check-list {
  list-style: none;
  padding: 0;
}

.check-list li {
  position: relative;
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.check-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--primary-color);
  font-weight: bold;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag {
  background: var(--surface-2);
  color: var(--text-primary);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 500;
  box-shadow: var(--shadow-light);
  transition: all 0.2s;
}

.tag:hover {
  background: var(--primary-color);
  color: white;
  transform: scale(1.05);
}

/* Animations */
.fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
