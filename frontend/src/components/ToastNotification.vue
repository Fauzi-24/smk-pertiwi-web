<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', toast.type]"
      >
        <i :class="getIcon(toast.type)"></i>
        <span>{{ toast.message }}</span>
        <button @click="removeToast(toast.id)" class="toast-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'ToastNotification',
  setup() {
    const toasts = ref([])
    let toastId = 0

    const addToast = (message, type = 'info', duration = 3000) => {
      const id = toastId++
      toasts.value.push({ id, message, type })
      
      if (duration > 0) {
        setTimeout(() => {
          removeToast(id)
        }, duration)
      }
    }

    const removeToast = (id) => {
      const index = toasts.value.findIndex(t => t.id === id)
      if (index > -1) {
        toasts.value.splice(index, 1)
      }
    }

    const getIcon = (type) => {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      }
      return icons[type] || icons.info
    }

    // Event listener for custom event
    const handleToastEvent = (e) => {
      const { message, type, duration } = e.detail
      addToast(message, type, duration)
    }

    // Lifecycle hooks
    // Lifecycle hooks
    onMounted(() => {
      window.addEventListener('toast-notification', handleToastEvent)
      
      // Global helper that dispatches event
      // Only define if not already defined to avoid conflict
      if (!window.$toast || window.$toast.isHelper) {
        window.$toast = (message, type, duration) => {
          window.dispatchEvent(new CustomEvent('toast-notification', {
            detail: { message, type, duration }
          }))
        }
        window.$toast.isHelper = true
      }
    })

    onUnmounted(() => {
      window.removeEventListener('toast-notification', handleToastEvent)
    })

    return {
      toasts,
      removeToast,
      getIcon
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 10001;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: var(--surface);
  border-left: 4px solid;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
}

.toast.success {
  border-color: #10b981;
  background: #ecfdf5;
}

.toast.success i {
  color: #10b981;
}

.toast.error {
  border-color: #ef4444;
  background: #fef2f2;
}

.toast.error i {
  color: #ef4444;
}

.toast.warning {
  border-color: #f59e0b;
  background: #fffbeb;
}

.toast.warning i {
  color: #f59e0b;
}

.toast.info {
  border-color: #3b82f6;
  background: #eff6ff;
}

.toast.info i {
  color: #3b82f6;
}

.toast i:first-child {
  font-size: 1.25rem;
}

.toast span {
  flex: 1;
  font-weight: 500;
  color: var(--text-primary);
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.toast-close:hover {
  color: var(--text-primary);
}

/* Animations */
.toast-enter-active {
  animation: slideIn 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .toast-container {
    right: 10px;
    left: 10px;
    max-width: none;
  }
  
  .toast {
    min-width: auto;
  }
}
</style>
