<template>
  <div class="lazy-image-wrapper" :style="{ paddingBottom: aspectRatio }">
    <transition name="fade">
      <img
        v-if="loaded"
        :src="src"
        :alt="alt"
        :class="['lazy-image', { loaded }]"
        @load="onLoad"
        @error="onError"
      />
    </transition>
    <div v-if="!loaded && !error" class="placeholder">
      <div class="spinner"></div>
    </div>
    <div v-if="error" class="error-placeholder">
      <i class="fas fa-image"></i>
      <span>{{ errorText }}</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'LazyImage',
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: ''
    },
    aspectRatio: {
      type: String,
      default: '56.25%' // 16:9 default
    },
    errorText: {
      type: String,
      default: 'Gagal memuat gambar'
    }
  },
  setup(props) {
    const loaded = ref(false)
    const error = ref(false)
    const imgElement = ref(null)

    const onLoad = () => {
      loaded.value = true
    }

    const onError = () => {
      error.value = true
      loaded.value = false
    }

    onMounted(() => {
      // IntersectionObserver untuk lazy loading
      if ('IntersectionObserver' in window) {
        const img = new Image()
        
        const observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              img.src = props.src
              img.onload = onLoad
              img.onerror = onError
              observer.disconnect()
            }
          })
        })

        // Observe wrapper element
        const wrapper = document.querySelector('.lazy-image-wrapper')
        if (wrapper) {
          observer.observe(wrapper)
        }
      } else {
        // Fallback tanpa IntersectionObserver
        loaded.value = true
      }
    })

    return {
      loaded,
      error,
      onLoad,
      onError
    }
  }
}
</script>

<style scoped>
.lazy-image-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
  background: var(--surface-2);
}

.lazy-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.lazy-image.loaded {
  opacity: 1;
}

.placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-2);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  background: var(--surface-2);
}

.error-placeholder i {
  font-size: 2rem;
  opacity: 0.5;
}

.error-placeholder span {
  font-size: 0.9rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
