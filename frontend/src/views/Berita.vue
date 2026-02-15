<template>
  <div class="page-container">
    <div class="header-section fade-in-up">
      <h1>{{ $t('news_page.title') }}</h1>
      <p>{{ $t('news_page.subtitle') }}</p>
    </div>

    <div v-if="loading" class="news-grid">
      <SkeletonLoader type="card" v-for="i in 6" :key="i" />
    </div>

    <div v-else-if="newsItems.length === 0" class="empty-state">
      {{ $t('news_page.empty') }}
    </div>

    <div v-else class="news-grid stagger-children">
      <div v-for="item in newsItems" :key="item.id" class="news-card">
        <div class="news-image">
          <img :src="item.image || 'https://via.placeholder.com/400x250?text=SMK+Pertiwi'" :alt="$t('news_data.item_' + item.id + '.title')" loading="lazy">
          <span class="news-category">{{ item.category }}</span>
          <span v-if="index === 0" class="badge-latest">New</span>
        </div>
        <div class="news-content">
          <span class="news-date">
            <i class="far fa-calendar-alt"></i> {{ formatDate(item.date) }}
          </span>
          <h3>{{ $t('news_data.item_' + item.id + '.title') }}</h3>
          <p>{{ $t('news_data.item_' + item.id + '.summary') }}</p>
          <button class="read-more">
            {{ $t('news_page.read_more') }} <i class="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import newsData from '../data/newsData'
import SkeletonLoader from '../components/SkeletonLoader.vue'

export default {
  name: 'Berita',
  components: {
    SkeletonLoader
  },
  data() {
    return {
      newsItems: [],
      loading: true
    }
  },
  mounted() {
    this.loadNews()
  },
  methods: {
    async loadNews() {
      // Simulate API delay for smooth UX
      setTimeout(() => {
        this.newsItems = newsData
        this.loading = false
      }, 500)
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('id-ID', {
        day: 'numeric', month: 'long', year: 'numeric'
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
.page-container {
  padding: 80px 2rem 4rem;
  min-height: 100vh;
  background: var(--background);
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.news-card {
  background: var(--surface);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.news-card:hover {
  transform: translateY(-5px);
}

.news-image {
  height: 200px;
  overflow: hidden;
  background: var(--surface-2);
  position: relative;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
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

.news-card:hover .news-image img {
  transform: scale(1.05);
}

.badge-latest {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: #dc2626;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.3);
  z-index: 2;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.news-card:hover .read-more {
  color: var(--primary-dark);
  gap: 1rem;
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
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.news-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
  line-height: 1.4;
}

.news-content p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.read-more {
  background: transparent;
  color: var(--primary-color);
  font-weight: 600;
  border: none;
  cursor: pointer;
  text-align: left;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: gap 0.2s;
}

.read-more:hover {
  gap: 0.8rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.fade-in { animation: fadeIn 0.5s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
