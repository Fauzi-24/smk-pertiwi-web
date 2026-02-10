<template>
  <div v-if="open" class="confirm-overlay" @click.self="$emit('cancel')">
    <div class="confirm-card">
      <h3>{{ title }}</h3>
      <p>{{ message }}</p>
      <div class="confirm-actions">
        <button class="btn cancel" type="button" @click="$emit('cancel')">
          {{ cancelLabel }}
        </button>
        <button class="btn confirm" type="button" @click="$emit('confirm')">
          {{ confirmLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    open: { type: Boolean, default: false },
    title: { type: String, default: 'Konfirmasi' },
    message: { type: String, default: 'Anda yakin?' },
    confirmLabel: { type: String, default: 'Ya' },
    cancelLabel: { type: String, default: 'Batal' }
  },
  emits: ['confirm', 'cancel']
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 60;
  padding: 1rem;
}

.confirm-card {
  width: min(420px, 90vw);
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: var(--shadow);
}

.confirm-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: var(--text-primary);
}

.confirm-card p {
  margin: 0 0 1rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}

.btn {
  padding: 0.55rem 1rem;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn.cancel {
  background: transparent;
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.btn.cancel:hover {
  color: var(--text-primary);
  border-color: var(--primary-color);
}

.btn.confirm {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

.btn.confirm:hover {
  background: #dc2626;
  border-color: #dc2626;
}
</style>
