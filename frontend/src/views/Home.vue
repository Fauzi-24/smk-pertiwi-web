<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero fade-in-up">
      <div class="container hero-content">
        <h1 class="hero-title">{{ $t('hero.welcome') }}</h1>
        <p class="hero-subtitle">{{ $t('hero.subtitle') }}</p>
        <div class="hero-actions">
          <router-link to="/ppdb" class="btn btn-primary">{{ $t('hero.cta_ppdb') }}</router-link>
          <router-link to="/profil" class="btn btn-outline">{{ $t('hero.cta_more') }}</router-link>
        </div>
      </div>
    </section>

    <section class="latest-news section-padding">
      <div class="container">
        <div class="section-header text-center">
          <h2 class="section-title">{{ $t('home_news.title') }}</h2>
          <p class="section-subtitle">{{ $t('home_news.subtitle') }}</p>
        </div>

        <div class="news-grid">
          <div v-for="item in latestNews" :key="item.id" class="news-card">
            <div class="news-image">
              <img :src="item.image" :alt="item.title" loading="lazy">
              <span class="news-category">{{ item.category }}</span>
            </div>
            <div class="news-content">
              <span class="news-date"><i class="far fa-calendar-alt"></i> {{ formatDate(item.date) }}</span>
              <h3>{{ item.title }}</h3>
              <p>{{ truncate(item.summary, 80) }}</p>
              <router-link to="/berita" class="read-more">{{ $t('home_news.read_more') }} <i class="fas fa-arrow-right"></i></router-link>
            </div>
          </div>
        </div>

        <div class="text-center mt-20">
          <router-link to="/berita" class="btn btn-outline">{{ $t('home_news.view_all') }}</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import newsData from '../data/newsData'

export default {
  name: 'Home',
  data() {
    return {
      latestNews: [],
      loading: true
    }
  },
  mounted() {
    // Simulate loading effect for smooth UX
    setTimeout(() => {
      this.latestNews = newsData.slice(0, 3)
      this.loading = false
    }, 300)
  },
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('id-ID', {
        day: 'numeric', month: 'short', year: 'numeric'
      })
    },
    truncate(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
  }
}
</script>

<style scoped>
.hero {
  min-height: 85vh;
  display: flex;
  align-items: center;
  background: var(--background);
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 400px;
  height: 400px;
  background-image: linear-gradient(to right, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  border-radius: 50%;
  z-index: 1;
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -50px;
  left: -50px;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
  filter: blur(80px);
  opacity: 0.1;
  border-radius: 50%;
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.hero-title .highlight {
  background: linear-gradient(120deg, var(--primary-color), #22C55E);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 1.1rem;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  border: 2px solid var(--primary-color);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
}

.btn-outline {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--gray-medium);
}

.btn-outline:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-3px);
  background: rgba(37, 99, 235, 0.05);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .hero-subtitle {
    font-size: 1.1rem;
  }
}

/* News Section */
.section-padding {
  padding: 5rem 0;
}

.section-header {
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-weight: 800;
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.news-card {
  background: var(--surface);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  will-change: transform;
}

.news-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.12);
  border-color: var(--primary-color);
}

.news-image {
  height: 220px;
  position: relative;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.news-card:hover .news-image img {
  transform: scale(1.1);
}

.news-category {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(37, 99, 235, 0.9);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.news-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.news-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.news-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.8rem;
  line-height: 1.4;
  color: var(--text-primary);
  font-weight: 700;
}

.news-content p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.read-more {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: gap 0.2s;
  margin-top: auto;
}

.read-more:hover {
  gap: 0.8rem;
}
</style>
