<template>
  <div class="main-layout">
    <nav class="navbar" :class="{ 'scrolled': isScrolled }">
      <div class="container nav-content">
        <router-link to="/" class="logo-link">
          <img src="@/assets/SMK_PERTIWI_KUNINGAN-removebg-preview.png" alt="SMK Pertiwi Tech Logo" class="nav-logo" />
          <span class="logo-text">SMK Pertiwi Kuningan</span>
        </router-link>

        <div class="nav-links" :class="{ 'mobile-active': mobileMenuOpen }">
          <router-link to="/" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.home') }}</router-link>
          <router-link to="/profil" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.profile') }}</router-link>
          <router-link to="/jurusan" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.majors') }}</router-link>
          <router-link to="/guru" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.teachers') }}</router-link>
          <router-link to="/galeri" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.gallery') }}</router-link>
          <router-link to="/alumni" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.alumni') }}</router-link>
          <router-link to="/berita" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.news') }}</router-link>
          <router-link to="/kontak" class="nav-item" @click="mobileMenuOpen = false">{{ $t('nav.contact') }}</router-link>
          <router-link to="/chat" class="nav-item" @click="mobileMenuOpen = false">
            <i class="fas fa-comment-dots"></i> Chat AI
          </router-link>
          <router-link to="/ppdb" class="nav-btn-highlight" @click="mobileMenuOpen = false">{{ $t('nav.ppdb') }}</router-link>
          <LanguageSwitcher />
          <button class="theme-toggle" @click="toggleTheme" :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'" :title="isDark ? 'Light Mode' : 'Dark Mode'">
            <i class="fas" :class="isDark ? 'fa-sun' : 'fa-moon'"></i>
          </button>
        </div>

        <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle mobile menu" :aria-expanded="mobileMenuOpen">
          <i class="fas" :class="mobileMenuOpen ? 'fa-times' : 'fa-bars'"></i>
        </button>
      </div>
    </nav>

    <main class="content-wrapper">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <div class="layout-extras">
      <BackToTop />
      <CookieConsent />
      <PWAInstallBanner />
      <SmartWhatsAppButton />
    </div>

    <footer class="main-footer">
      <div class="container footer-content">
        <div class="footer-section brand">
          <img src="@/assets/SMK_PERTIWI_KUNINGAN-removebg-preview.png" alt="Logo Footer" class="footer-logo" />
          <h3>SMK Pertiwi Kuningan</h3>
          <p>{{ $t('footer.desc') }}</p>
        </div>
        <div class="footer-section links">
          <h4>{{ $t('footer.quick_links') }}</h4>
          <ul>
            <li><router-link to="/profil">{{ $t('nav.profile') }}</router-link></li>
            <li><router-link to="/jurusan">{{ $t('nav.majors') }}</router-link></li>
            <li><router-link to="/ppdb">{{ $t('nav.ppdb') }}</router-link></li>
            <li><router-link to="/faq">FAQ</router-link></li>
            <li><router-link to="/kontak">{{ $t('nav.contact') }}</router-link></li>
            <li><router-link to="/admin/login">Login Admin</router-link></li>
          </ul>
        </div>
        <div class="footer-section contact">
          <h4>{{ $t('footer.contact_us') }}</h4>
          <p><i class="fas fa-map-marker-alt"></i> Jalan Siliwangi No. 26A, Kasturi, Kuningan, Jawa Barat</p>
          <p><i class="fas fa-phone"></i> (0232) 871146</p>
          <p><i class="fas fa-envelope"></i> info@smkpertiwi.sch.id</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>{{ $t('footer.copyright') }}</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import ToastNotification from '../components/ToastNotification.vue'
import BackToTop from '../components/BackToTop.vue'
import CookieConsent from '../components/CookieConsent.vue'
import PWAInstallBanner from '../components/PWAInstallBanner.vue'
import SmartWhatsAppButton from '../components/SmartWhatsAppButton.vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

export default {
  name: 'MainLayout',
  components: {
    ToastNotification,
    BackToTop,
    CookieConsent,
    PWAInstallBanner,
    SmartWhatsAppButton,
    LanguageSwitcher
  },
  data() {
    return {
      isScrolled: false,
      mobileMenuOpen: false,
      isDark: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll, { passive: true })
    this.loadTheme()
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      if (this._scrollTimer) return
      this._scrollTimer = requestAnimationFrame(() => {
        this.isScrolled = window.scrollY > 50
        this._scrollTimer = null
      })
    },
    loadTheme() {
      const savedTheme = localStorage.getItem('pertiwi_theme') || 'light'
      this.isDark = savedTheme === 'dark'
      this.applyTheme(savedTheme)
    },
    toggleTheme() {
      this.isDark = !this.isDark
      const theme = this.isDark ? 'dark' : 'light'
      this.applyTheme(theme)
      localStorage.setItem('pertiwi_theme', theme)
    },
    applyTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark')
        document.documentElement.style.setProperty('--background', '#0F172A')
        document.documentElement.style.setProperty('--background-dark', '#0B1220')
        document.documentElement.style.setProperty('--white', '#111827')
        document.documentElement.style.setProperty('--surface', '#111827')
        document.documentElement.style.setProperty('--surface-2', '#1F2937')
        document.documentElement.style.setProperty('--text-primary', '#F9FAFB')
        document.documentElement.style.setProperty('--text-secondary', '#CBD5E1')
        document.documentElement.style.setProperty('--gray-light', '#334155')
        document.documentElement.style.setProperty('--gray-medium', '#475569')
        document.documentElement.style.setProperty('--border-color', '#334155')
        document.documentElement.style.setProperty('--border-rgb', '51, 65, 85')
        document.documentElement.style.setProperty('--surface-rgb', '17, 24, 39')
        document.documentElement.style.setProperty('--shadow', '0 4px 12px rgba(0, 0, 0, 0.35)')
        document.documentElement.style.setProperty('--shadow', '0 4px 12px rgba(0, 0, 0, 0.35)')
        document.documentElement.style.setProperty('--shadow-light', '0 2px 8px rgba(0, 0, 0, 0.2)')
        document.documentElement.style.setProperty('--primary-dark', '#1E40AF')
      } else {
        document.documentElement.classList.remove('dark')
        document.documentElement.style.setProperty('--background', '#F1F5F9') // Slate-100 for contrast
        document.documentElement.style.setProperty('--background-dark', '#E2E8F0')
        document.documentElement.style.setProperty('--white', '#FFFFFF')
        document.documentElement.style.setProperty('--surface', '#FFFFFF')
        document.documentElement.style.setProperty('--surface-2', '#F8FAFC')
        document.documentElement.style.setProperty('--text-primary', '#0F172A') // Slate-900 (Sharper)
        document.documentElement.style.setProperty('--text-secondary', '#475569') // Slate-600
        document.documentElement.style.setProperty('--gray-light', '#E2E8F0')
        document.documentElement.style.setProperty('--gray-medium', '#94A3B8')
        document.documentElement.style.setProperty('--ai-msg-bg', '#FFFFFF')
        document.documentElement.style.setProperty('--ai-msg-text', '#0F172A')
        document.documentElement.style.setProperty('--user-msg-bg', '#2563EB')
        document.documentElement.style.setProperty('--user-msg-text', '#FFFFFF')
        document.documentElement.style.setProperty('--card-bg', '#FFFFFF')
        document.documentElement.style.setProperty('--border-color', '#E2E8F0')
        document.documentElement.style.setProperty('--border-rgb', '226, 232, 240')
        document.documentElement.style.setProperty('--surface-rgb', '255, 255, 255')
        document.documentElement.style.setProperty('--disabled-bg', '#E2E8F0')
        document.documentElement.style.setProperty('--shadow', '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)')
        document.documentElement.style.setProperty('--shadow-light', '0 1px 2px 0 rgba(0, 0, 0, 0.05)')
        document.documentElement.style.setProperty('--shadow-hover', '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)')
        document.documentElement.style.setProperty('--primary-dark', '#1D4ED8')
      }
    }
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: rgba(var(--surface-rgb, 255, 255, 255), 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(var(--border-rgb, 229, 231, 235), 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 1rem 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.navbar.scrolled {
  background: rgba(var(--surface-rgb, 255, 255, 255), 0.85);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(var(--border-rgb, 229, 231, 235), 0.5);
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  text-decoration: none;
  color: var(--text-primary);
}

.nav-logo {
  height: 40px;
  width: auto;
}

.logo-text {
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-item {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s;
  position: relative;
}

.nav-item:hover, .nav-item.router-link-exact-active {
  color: var(--primary-color);
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.nav-item:hover::after, .nav-item.router-link-exact-active::after {
  width: 100%;
}

.nav-btn-highlight {
  background: var(--primary-color);
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

.nav-btn-highlight:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3);
}

.theme-toggle {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.1rem;
}

.theme-toggle:hover {
  background: var(--primary-color);
  color: white;
  transform: rotate(20deg);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-primary);
  cursor: pointer;
}

.content-wrapper {
  flex: 1;
  padding-top: 80px; /* Space for fixed navbar */
}

/* Footer */
.main-footer {
  background: #0f172a; /* Dark background */
  color: #f8fafc;
  padding: 4rem 0 0;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-section h3, .footer-section h4 {
  margin-bottom: 1.2rem;
  color: white;
}

.footer-logo {
  height: 50px;
  margin-bottom: 1rem;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 0.8rem;
}

.footer-section ul li a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-section ul li a:hover {
  color: white;
}

.footer-section.contact p {
  display: flex;
  gap: 0.8rem;
  color: #94a3b8;
  margin-bottom: 0.8rem;
}

.footer-bottom {
  text-align: center;
  padding: 1.5rem 0;
  color: #64748b;
  font-size: 0.9rem;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .mobile-toggle {
    display: block;
  }

  .nav-links {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: rgba(var(--surface-rgb, 255, 255, 255), 0.95);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    flex-direction: column;
    padding: 2rem;
    gap: 1.5rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    transform: translateY(-150%);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 999;
    border-bottom: 1px solid rgba(var(--border-rgb, 229, 231, 235), 0.5);
  }

  .nav-links.mobile-active {
    transform: translateY(0);
  }
}
</style>
