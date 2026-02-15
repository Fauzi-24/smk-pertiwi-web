<template>
  <div v-if="isOpen" class="modal-backdrop" @click="close">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="icon-wrapper" :class="type">
          <i :class="iconClass"></i>
        </div>
        <h3>{{ title }}</h3>
      </div>
      
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>

      <div class="modal-actions">
        <button class="btn-cancel" @click="close">Batal</button>
        <button class="btn-confirm" :class="type" @click="confirm">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmationModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Konfirmasi'
    },
    message: {
      type: String,
      default: 'Apakah Anda yakin?'
    },
    confirmText: {
      type: String,
      default: 'Ya, Lanjutkan'
    },
    type: {
      type: String,
      default: 'primary', // primary, danger, success
      validator: (value) => ['primary', 'danger', 'success'].includes(value)
    }
  },
  computed: {
    iconClass() {
      switch (this.type) {
        case 'danger': return 'fas fa-exclamation-triangle';
        case 'success': return 'fas fa-check-circle';
        default: return 'fas fa-info-circle';
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    confirm() {
      this.$emit('confirm');
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease-out;
}

.modal-container {
  background: var(--surface, #ffffff);
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 1.5rem;
  border: 1px solid var(--border-color, #e2e8f0);
  transform: scale(0.95);
  animation: popup 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.modal-header {
  text-align: center;
  margin-bottom: 1rem;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
}

.icon-wrapper.danger { background: #fee2e2; color: #dc2626; }
.icon-wrapper.success { background: #dcfce7; color: #16a34a; }
.icon-wrapper.primary { background: #dbeafe; color: #2563eb; }

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.modal-body {
  text-align: center;
  margin-bottom: 2rem;
}

.modal-body p {
  color: var(--text-secondary);
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.modal-actions button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background: var(--surface-2);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-cancel:hover {
  background: var(--border-color);
}

.btn-confirm.primary { background: var(--primary-color); color: white; }
.btn-confirm.primary:hover { background: var(--primary-dark); }

.btn-confirm.danger { background: #dc2626; color: white; }
.btn-confirm.danger:hover { background: #b91c1c; }

.btn-confirm.success { background: #16a34a; color: white; }
.btn-confirm.success:hover { background: #15803d; }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes popup {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
