<template>
  <div v-if="open" class="login-overlay" @click.self="$emit('cancel')">
    <div class="login-card">
      <div class="login-header">
        <h3>Login Admin</h3>
        <button class="icon-btn" type="button" @click="$emit('cancel')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <p>Masukkan Admin Key untuk membuka panel review.</p>

      <input
        :value="adminKey"
        type="password"
        placeholder="ADMIN_KEY"
        @input="$emit('update-key', $event.target.value)"
      />

      <div v-if="error" class="login-error">{{ error }}</div>

      <div class="login-actions">
        <button class="btn cancel" type="button" @click="$emit('cancel')">Batal</button>
        <button class="btn submit" type="button" :disabled="loading" @click="$emit('submit')">
          {{ loading ? 'Memeriksa...' : 'Login' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLoginDialog',
  props: {
    open: { type: Boolean, default: false },
    adminKey: { type: String, default: '' },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' }
  },
  emits: ['cancel', 'submit', 'update-key']
}
</script>

<style scoped>
.login-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
  padding: 1rem;
}

.login-card {
  width: min(420px, 90vw);
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.login-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.login-header h3 {
  margin: 0;
  font-size: 1rem;
}

.icon-btn {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
}

.login-card p {
  margin: 0;
  color: var(--text-secondary);
}

.login-card input {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.6rem;
  font-family: inherit;
}

.login-actions {
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
}

.btn.cancel {
  background: transparent;
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.btn.submit {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.login-error {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid #ef4444;
  color: #ef4444;
  padding: 0.5rem 0.7rem;
  border-radius: 8px;
}
</style>
