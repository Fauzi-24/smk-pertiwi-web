<template>
  <div class="language-switcher" :class="{ 'is-open': isOpen }">
    <button class="lang-btn" @click="toggleDropdown" title="Change Language">
      <i class="fas fa-globe"></i>
      <span class="code">{{ locale.toUpperCase() }}</span>
      <i class="fas fa-chevron-down text-xs"></i>
    </button>
    <div class="lang-dropdown">
      <button
        v-for="(lang, code) in languages"
        :key="code"
        class="lang-option"
        :class="{ active: locale === code }"
        @click="changeLanguage(code)"
      >
        <span class="flag">{{ lang.flag }}</span>
        <span class="name">{{ lang.name }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'LanguageSwitcher',
  setup() {
    const { locale } = useI18n()
    const isOpen = ref(false)

    const languages = {
      id: { name: 'Indonesia', flag: '🇮🇩' },
      en: { name: 'English', flag: '🇬🇧' },
      de: { name: 'Deutsch', flag: '🇩🇪' },
      ru: { name: 'Русский', flag: '🇷🇺' },
      jp: { name: '日本語', flag: '🇯🇵' },
      ar: { name: 'العربية', flag: '🇸🇦' }
    }

    const currentFlag = computed(() => {
      return languages[locale.value]?.flag || '🌐'
    })

    const toggleDropdown = () => {
      isOpen.value = !isOpen.value
    }

    const changeLanguage = (code) => {
      locale.value = code
      localStorage.setItem('user-locale', code)
      isOpen.value = false
      
      // Handle RTL for Arabic
      if (code === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl')
        document.documentElement.lang = 'ar'
      } else {
        document.documentElement.setAttribute('dir', 'ltr')
        document.documentElement.lang = code
      }
    }

    // Close dropdown when clicking outside
    const closeDropdown = (e) => {
      if (!e.target.closest('.language-switcher')) {
        isOpen.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', closeDropdown)
      // Initial RTL check
      if (locale.value === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl')
      }
    })

    onUnmounted(() => {
      document.removeEventListener('click', closeDropdown)
    })

    return {
      locale,
      languages,
      isOpen,
      currentFlag,
      toggleDropdown,
      changeLanguage
    }
  }
}
</script>

<style scoped>
.language-switcher {
  position: relative;
  z-index: 1000;
}

.lang-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid transparent;
  padding: 0.5rem 0.75rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.9rem;
}

.lang-btn:hover, .language-switcher.is-open .lang-btn {
  background: var(--surface-2);
  border-color: var(--border-color);
  box-shadow: var(--shadow-sm);
}

.text-xs {
  font-size: 0.75rem;
  opacity: 0.7;
}

.flag {
  font-size: 1.2rem;
}

.lang-dropdown {
  position: absolute;
  top: 120%;
  right: 0;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px) scale(0.95);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
  padding: 0.5rem;
  transform-origin: top right;
}

.language-switcher.is-open .lang-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.lang-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 0.95rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.lang-option:hover {
  background: var(--surface-2);
  color: var(--primary-color);
}

.lang-option.active {
  background: rgba(var(--primary-rgb), 0.1);
  color: var(--primary-color);
  font-weight: 600;
}

/* RTL Support */
:deep([dir="rtl"]) .driver {
    direction: rtl;
}
</style>
