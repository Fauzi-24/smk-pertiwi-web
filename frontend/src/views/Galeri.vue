<template>
  <div class="galeri-page">
    <!-- Header -->
    <div class="galeri-header">
      <h1>{{ $t('gallery.title') }}</h1>
      <p>{{ $t('gallery.subtitle') }}</p>
    </div>

    <!-- Filter Categories -->
    <div class="filter-section">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="['filter-btn', { active: selectedCategory === cat }]"
        @click="selectedCategory = cat"
      >
        {{ cat === 'Semua' ? $t('gallery.filter_all') : $t('gallery.categories.' + cat) }}
      </button>
    </div>

    <!-- Loading Skeletons -->
    <div v-if="loading" class="gallery-grid">
      <SkeletonCard v-for="n in 12" :key="n" />
    </div>

    <!-- Gallery Grid -->
    <div v-else class="gallery-grid" id="gallery-grid">
      <div
        v-for="(item, index) in filteredGallery"
        :key="item.id"
        class="gallery-item fade-in"
        :style="{ animationDelay: `${index * 0.05}s` }"
        @click="openLightbox(index)"
      >
        <div class="image-wrapper">
          <img :src="item.image" :alt="$t('gallery_data.item_' + item.id + '.title')" loading="lazy">
          <div class="overlay">
            <i class="fas fa-search-plus"></i>
          </div>
        </div>
        <div class="item-info">
          <span class="category-badge">{{ $t('gallery.categories.' + item.category) }}</span>
          <h3>{{ $t('gallery_data.item_' + item.id + '.title') }}</h3>
          <p>{{ $t('gallery_data.item_' + item.id + '.description') }}</p>
          <p class="date">
            <i class="fas fa-calendar"></i>
            {{ formatDate(item.date) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxOpen" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button class="close-btn" @click="closeLightbox">
            <i class="fas fa-times"></i>
        </button>
        <img :src="selectedImage?.image" :alt="$t('gallery_data.item_' + selectedImage?.id + '.title')" />
        <div class="lightbox-info">
          <h2>{{ $t('gallery_data.item_' + selectedImage?.id + '.title') }}</h2>
          <p class="description">{{ $t('gallery_data.item_' + selectedImage?.id + '.description') }}</p>
          <p class="date">
            <i class="fas fa-calendar"></i>
            {{ formatDate(selectedImage?.date) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { galleryData, categories } from '../data/galleryData.js'
import SkeletonCard from '../components/SkeletonCard.vue'

export default {
  name: 'Galeri',
  components: {
    SkeletonCard
  },
  setup() {
    const selectedCategory = ref('Semua')
    const lightboxOpen = ref(false)
    const loading = ref(true)
    const selectedImage = ref(null)

    const filteredGallery = computed(() => {
      if (selectedCategory.value === 'Semua') {
        return galleryData
      }
      return galleryData.filter(item => item.category === selectedCategory.value)
    })

    const openLightbox = (index) => {
      selectedImage.value = filteredGallery.value[index]
      lightboxOpen.value = true
      document.body.style.overflow = 'hidden'
    }

    const closeLightbox = () => {
      lightboxOpen.value = false
      selectedImage.value = null
      document.body.style.overflow = 'auto'
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('id-ID', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/600x400/2563eb/ffffff?text=SMK+Pertiwi+Kuningan'
    }

    onMounted(() => {
      // Simulate loading delay
      setTimeout(() => {
        loading.value = false
      }, 800)
    })

    return {
      categories,
      selectedCategory,
      filteredGallery,
      lightboxOpen,
      loading,
      selectedImage,
      openLightbox,
      closeLightbox,
      formatDate,
      handleImageError
    }
  }
}
</script>

<style scoped>
.galeri-page {
  min-height: 100vh;
  padding: 100px 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.galeri-header {
  text-align: center;
  margin-bottom: 3rem;
}

.galeri-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.galeri-header p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 2.5rem;
}

.filter-btn {
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  border: 2px solid var(--border-color);
  background: var(--surface);
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-btn:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.gallery-item {
  background: var(--surface);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid var(--border-color);
}

.gallery-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 240px;
  overflow: hidden;
  background: var(--surface-2);
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.gallery-item:hover .image-wrapper img {
  transform: scale(1.1);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(37, 99, 235, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gallery-item:hover .overlay {
  opacity: 1;
}

.overlay i {
  font-size: 3rem;
  color: white;
}

.item-info {
  padding: 1.2rem;
}

.category-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  background: rgba(var(--primary-rgb), 0.1);
  color: var(--primary-color);
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.item-info h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: var(--text-primary);
}

.item-info .date {
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.close-btn {
  position: absolute;
  top: 2rem;
  right: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid white;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10001;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.lightbox-content {
  max-width: 1000px;
  width: 100%;
  background: var(--surface);
  border-radius: 20px;
  overflow: hidden;
  animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.lightbox-content img {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
  background: #000;
}

.lightbox-info {
  padding: 2rem;
}

.lightbox-info h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.8rem;
}

.lightbox-info .description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .galeri-header h1 {
    font-size: 2rem;
  }

  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  .lightbox {
    padding: 1rem;
  }

  .close-btn {
    top: 1rem;
    right: 1rem;
    width: 40px;
    height: 40px;
  }
}
</style>
