<template>
  <div class="chat-page">
    <!-- Back Button -->
    <div class="chat-header">
      <router-link to="/" class="back-button">
        <i class="fas fa-arrow-left"></i> Kembali ke Beranda
      </router-link>
    </div>
    
    <ChatWidget :alwaysOpen="true" />
  </div>
</template>

<script>
import ChatWidget from '../components/ChatWidget.vue'

export default {
  name: 'Chat',
  components: {
    ChatWidget
  }
}
</script>

<style scoped>
.chat-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  background: var(--background);
  display: flex;
  flex-direction: column;
}

.chat-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10000;
  background: rgba(var(--surface-rgb, 255, 255, 255), 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border-color);
  padding: 0.8rem 1.5rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1.2rem;
  background: var(--surface);
  color: var(--primary-color);
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 0.9rem;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.back-button i {
  font-size: 0.8rem;
  transition: transform 0.3s;
}

.back-button:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateX(-5px);
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
}

.back-button:hover i {
  transform: translateX(-3px);
}

.chat-page :deep(.chat-toggle-btn) {
  display: none !important;
}

.chat-page :deep(.chat-container) {
  position: fixed !important;
  top: 65px !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100% !important;
  height: calc(100% - 65px) !important;
  transform: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
</style>
