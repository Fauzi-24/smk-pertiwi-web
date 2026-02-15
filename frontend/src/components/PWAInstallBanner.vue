<template>
  <transition name="slide-up">
    <div v-if="showInstallPrompt" class="pwa-install-banner">
      <div class="banner-content">
        <div class="banner-icon">
          <i class="fas fa-mobile-alt"></i>
        </div>
        <div class="banner-text">
          <h4>Install Aplikasi</h4>
          <p>Install SMK Pertiwi di perangkat Anda untuk akses lebih cepat!</p>
        </div>
        <div class="banner-actions">
          <button @click="installPWA" class="btn-install">
            <i class="fas fa-download"></i> Install
          </button>
          <button @click="dismissPrompt" class="btn-dismiss" aria-label="Tutup">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'PWAInstallBanner',
  data() {
    return {
      showInstallPrompt: false,
      deferredPrompt: null
    }
  },
  mounted() {
    // Listen for beforeinstallprompt event
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent the default browser install prompt
      e.preventDefault()
      
      // Store the event for later use
      this.deferredPrompt = e
      
      // Check if user has previously dismissed
      const dismissed = localStorage.getItem('pwa-install-dismissed')
      if (!dismissed) {
        // Show custom install prompt
        setTimeout(() => {
          this.showInstallPrompt = true
        }, 3000) // Show after 3 seconds
      }
    })

    // Listen for app installed event
    window.addEventListener('appinstalled', () => {
      this.showInstallPrompt = false
      this.deferredPrompt = null
      console.log('PWA successfully installed')
    })
  },
  methods: {
    async installPWA() {
      if (!this.deferredPrompt) {
        return
      }

      // Show the install prompt
      this.deferredPrompt.prompt()

      // Wait for the user's response
      const { outcome } = await this.deferredPrompt.userChoice
      
      if (outcome === 'accepted') {
        console.log('User accepted the install prompt')
      } else {
        console.log('User dismissed the install prompt')
      }

      // Clear the deferredPrompt
      this.deferredPrompt = null
      this.showInstallPrompt = false
    },
    dismissPrompt() {
      this.showInstallPrompt = false
      // Remember dismissal for 7 days
      const expiryTime = new Date().getTime() + (7 * 24 * 60 * 60 * 1000)
      localStorage.setItem('pwa-install-dismissed', expiryTime.toString())
    }
  }
}
</script>

<style scoped>
.pwa-install-banner {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  max-width: 500px;
  width: calc(100% - 40px);
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  z-index: 999;
  padding: 1rem 1.5rem;
  border: 1px solid var(--border);
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.banner-icon {
  font-size: 2rem;
  color: var(--primary-color);
  flex-shrink: 0;
}

.banner-text {
  flex: 1;
}

.banner-text h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.banner-text p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.banner-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-install {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-install:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-dismiss {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.625rem;
  border-radius: 8px;
  transition: all 0.3s;
}

.btn-dismiss:hover {
  background: var(--hover);
  color: var(--text-primary);
}

/* Slide up animation */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translate(-50%, 20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}

/* Mobile responsive */
@media (max-width: 640px) {
  .pwa-install-banner {
    bottom: 10px;
    width: calc(100% - 20px);
    padding: 0.875rem 1rem;
  }

  .banner-content {
    gap: 0.75rem;
  }

  .banner-icon {
    font-size: 1.5rem;
  }

  .banner-text h4 {
    font-size: 0.9rem;
  }

  .banner-text p {
    font-size: 0.75rem;
  }

  .btn-install {
    padding: 0.5rem 0.875rem;
    font-size: 0.85rem;
  }
}
</style>
