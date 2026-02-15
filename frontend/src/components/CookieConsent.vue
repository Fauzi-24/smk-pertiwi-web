<template>
  <transition name="slide-up">
    <div v-if="showBanner" class="cookie-consent">
      <div class="cookie-content">
        <i class="fas fa-cookie-bite"></i>
        <div class="cookie-text">
          <p><strong>Kami menggunakan cookies</strong> untuk meningkatkan pengalaman Anda. Dengan melanjutkan, Anda menyetujui penggunaan cookies kami.</p>
        </div>
      </div>
      <div class="cookie-actions">
        <button @click="acceptCookies" class="btn-accept">
          Terima
        </button>
        <button @click="declineCookies" class="btn-decline">
          Tolak
        </button>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'CookieConsent',
  setup() {
    const showBanner = ref(false)

    onMounted(() => {
      const consent = localStorage.getItem('cookie_consent')
      if (!consent) {
        setTimeout(() => {
          showBanner.value = true
        }, 1000)
      }
    })

    const acceptCookies = () => {
      localStorage.setItem('cookie_consent', 'accepted')
      showBanner.value = false
      if (window.$toast) {
        window.$toast('Preferensi cookies disimpan', 'success')
      }
    }

    const declineCookies = () => {
      localStorage.setItem('cookie_consent', 'declined')
      showBanner.value = false
    }

    return {
      showBanner,
      acceptCookies,
      declineCookies
    }
  }
}
</script>

<style scoped>
.cookie-consent {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--surface);
  border-top: 2px solid var(--primary-color);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
}

.cookie-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.cookie-content i {
  font-size: 2.5rem;
  color: var(--primary-color);
}

.cookie-text p {
  margin: 0;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.cookie-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-accept,
.btn-decline {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-accept {
  background: var(--primary-color);
  color: white;
}

.btn-accept:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-decline {
  background: var(--surface-2);
  color: var(--text-secondary);
}

.btn-decline:hover {
  background: var(--gray-light);
}

.slide-up-enter-active {
  animation: slideUp 0.5s ease-out;
}

.slide-up-leave-active {
  animation: slideDown 0.5s ease-in;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(100%);
  }
}

@media (max-width: 768px) {
  .cookie-consent {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .cookie-actions {
    width: 100%;
  }
  
  .btn-accept,
  .btn-decline {
    flex: 1;
  }
}
</style>
