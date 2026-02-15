<template>
  <div class="alumni-page">
    <!-- Header Section -->
    <div class="hero-section">
      <h1>{{ $t('alumni.title') }}</h1>
      <p>{{ $t('alumni.subtitle') }}</p>
    </div>

    <!-- Statistics -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-users"></i>
        </div>
        <div class="stat-number">{{ stats.totalAlumni }}+</div>
        <div class="stat-label">{{ $t('alumni.stat_total') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-briefcase"></i>
        </div>
        <div class="stat-number">{{ stats.employed }}%</div>
        <div class="stat-label">{{ $t('alumni.stat_employed') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-store"></i>
        </div>
        <div class="stat-number">{{ stats.entrepreneurs }}%</div>
        <div class="stat-label">{{ $t('alumni.stat_entrepreneur') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-dollar-sign"></i>
        </div>
        <div class="stat-number">{{ stats.averageSalary }}</div>
        <div class="stat-label">{{ $t('alumni.stat_salary') }}</div>
      </div>
    </div>

    <!-- Featured Alumni -->
    <section class="featured-section">
      <h2>{{ $t('alumni.featured_title') }}</h2>
      <div class="alumni-grid">
        <div
          v-for="alumni in featuredAlumni"
          :key="alumni.id"
          class="alumni-card featured"
        >
          <div class="alumni-photo">
            <img :src="alumni.photo" :alt="alumni.name" loading="lazy" />
            <div class="badge">Featured</div>
          </div>
          <div class="alumni-info">
            <h3>{{ alumni.name }}</h3>
            <div class="alumni-meta">
              <span class="major">{{ alumni.major }}</span>
              <span class="year">Class of {{ alumni.year }}</span>
            </div>
            <div class="alumni-work">
              <i class="fas fa-building"></i>
              <div>
                <div class="position">{{ alumni.position }}</div>
                <div class="company">{{ alumni.company }}</div>
              </div>
            </div>
            <p class="achievement">{{ $t('alumni_data.profile_' + alumni.id + '.achievement') }}</p>
            <a
              v-if="alumni.linkedin"
              :href="alumni.linkedin"
              target="_blank"
              class="linkedin-btn"
              rel="noopener noreferrer"
            >
              <i class="fab fa-linkedin"></i> LinkedIn
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- All Alumni -->
    <section class="all-alumni-section">
      <h2>{{ $t('alumni.all_title') }}</h2>
      <div class="alumni-grid compact">
        <div
          v-for="alumni in regularAlumni"
          :key="alumni.id"
          class="alumni-card"
        >
          <div class="alumni-photo small">
            <img :src="alumni.photo" :alt="alumni.name" loading="lazy" />
          </div>
          <div class="alumni-info">
            <h3>{{ alumni.name }}</h3>
            <div class="alumni-meta">
              <span class="major">{{ alumni.major }}</span>
              <span class="year">{{ alumni.year }}</span>
            </div>
            <div class="alumni-work">
              <div class="position">{{ alumni.position }}</div>
              <div class="company">{{ alumni.company }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <h2>{{ $t('alumni.cta_title') }}</h2>
      <p>{{ $t('alumni.cta_desc') }}</p>
      <router-link to="/ppdb" class="cta-btn">
        <i class="fas fa-graduation-cap"></i>
        {{ $t('alumni.cta_btn') }}
      </router-link>
    </section>
  </div>
</template>

<script>
import { computed } from 'vue'
import { alumniData, alumniStats } from '../data/alumniData'

export default {
  name: 'Alumni',
  setup() {
    const stats = alumniStats

    const featuredAlumni = computed(() => {
      return alumniData.filter(a => a.featured)
    })

    const regularAlumni = computed(() => {
      return alumniData.filter(a => !a.featured)
    })

    return {
      stats,
      featuredAlumni,
      regularAlumni
    }
  }
}
</script>

<style scoped>
.alumni-page {
  min-height: 100vh;
  padding-top: 80px;
  background: var(--background);
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
}

.hero-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  opacity: 0.95;
}

/* Statistics */
.stats-section {
  max-width: 1200px;
  margin: -3rem auto 4rem;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: var(--surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-8px);
}

.stat-icon {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Alumni Sections */
.featured-section,
.all-alumni-section {
  max-width: 1200px;
  margin: 0 auto 4rem;
  padding: 0 2rem;
}

.featured-section h2,
.all-alumni-section h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  color: var(--text-primary);
}

.alumni-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.alumni-grid.compact {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.alumni-card {
  background: var(--surface);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.alumni-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.alumni-card.featured {
  border: 2px solid var(--primary-color);
}

.alumni-photo {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.alumni-photo.small {
  height: 200px;
}

.alumni-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--primary-color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.alumni-info {
  padding: 1.5rem;
}

.alumni-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.alumni-meta {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.alumni-meta .major {
  background: rgba(var(--primary-rgb), 0.1);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.alumni-meta .year {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.alumni-work {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--surface-2);
  border-radius: 8px;
}

.alumni-work i {
  color: var(--primary-color);
  font-size: 1.25rem;
  margin-top: 0.25rem;
}

.position {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.company {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.achievement {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.linkedin-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #0077b5;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.linkedin-btn:hover {
  background: #006399;
  transform: translateY(-2px);
}

/* CTA Section */
.cta-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.1) 0%, rgba(var(--primary-rgb), 0.05) 100%);
  margin: 4rem 0 0;
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.cta-section p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s;
}

.cta-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--primary-rgb), 0.3);
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }

  .alumni-grid {
    grid-template-columns: 1fr;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
