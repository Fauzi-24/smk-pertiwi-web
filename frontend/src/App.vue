<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <ProgressBar />
    <ToastNotification />
  </div>
</template>

<script>
import ToastNotification from './components/ToastNotification.vue'
import ProgressBar from './components/ProgressBar.vue'

export default {
  name: 'App',
  components: {
    ToastNotification,
    ProgressBar
  }
}
</script>

<style>
/* Reset and global styles */
:root {
  --primary-color: #2563EB;
  --primary-dark: #1E40AF;
  --primary-rgb: 37, 99, 235;
  --text-primary: #0F172A; /* Slate-900 */
  --text-secondary: #475569; /* Slate-600 */
  --background: #F1F5F9; /* Slate-100 */
  --background-dark: #E2E8F0;
  --white: #FFFFFF;
  --surface: #FFFFFF;
  --surface-2: #F8FAFC;
  --surface-rgb: 255, 255, 255;
  --gray-light: #E2E8F0;
  --gray-medium: #94A3B8;
  --border-color: #E2E8F0;
  --border-rgb: 226, 232, 240;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-light: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--text-primary);
  background: white;
}

html {
  scroll-behavior: smooth;
}

* {
  box-sizing: border-box;
}

/* Entrance Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

/* Staggered children - only apply to card-like elements */
.stagger-children > .news-card,
.stagger-children > .alumni-card,
.stagger-children > .gallery-item,
.stagger-children > .stat-card {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0.1s; }
.stagger-children > *:nth-child(2) { animation-delay: 0.2s; }
.stagger-children > *:nth-child(3) { animation-delay: 0.3s; }
.stagger-children > *:nth-child(4) { animation-delay: 0.4s; }
.stagger-children > *:nth-child(5) { animation-delay: 0.5s; }
.stagger-children > *:nth-child(6) { animation-delay: 0.6s; }

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Page Transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Print Styles */
@media print {
  /* Hide non-essential elements */
  .navbar,
  .main-footer,
  .whatsapp-float,
  .back-to-top,
  .toast-container,
  button:not(.print-btn),
  .social-share,
  .share-buttons {
    display: none !important;
  }

  /* Reset layout for print */
  body {
    background: white !important;
    color: black !important;
  }

  .page-container,
  .content-wrapper {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }

  /* Ensure content fits */
  * {
    box-shadow: none !important;
    text-shadow: none !important;
  }

  /* Page breaks */
  h1, h2, h3 {
    page-break-after: avoid;
  }

  img {
    max-width: 100% !important;
    page-break-inside: avoid;
  }

  /* Print-specific visibility */
  .print-only {
    display: block !important;
  }

  .no-print {
    display: none !important;
  }
}
</style>
