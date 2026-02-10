<template>
  <div v-if="open" class="admin-overlay" @click.self="$emit('close')">
    <div class="admin-card">
      <div class="admin-header">
        <div>
          <h3>Admin Review</h3>
          <p>Review koreksi dari user sebelum dipakai AI.</p>
        </div>
        <button class="icon-btn" type="button" @click="$emit('close')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <div class="admin-controls">
        <div class="admin-status">
          <span class="status-dot"></span>
          <span>Login sebagai Admin</span>
        </div>
        <div class="admin-actions-row">
          <button class="btn refresh" type="button" :disabled="loading" @click="$emit('refresh')">
            <i class="fas fa-rotate"></i>
            {{ loading ? 'Memuat...' : 'Refresh' }}
          </button>
          <button class="btn logout" type="button" @click="$emit('logout')">
            <i class="fas fa-right-from-bracket"></i>
            Logout
          </button>
        </div>
      </div>
      <div class="admin-export">
        <span>Export:</span>
        <button class="btn export" type="button" @click="$emit('export', 'pending')">
          Pending
        </button>
        <button class="btn export" type="button" @click="$emit('export', 'approved')">
          Approved
        </button>
        <button class="btn export" type="button" @click="$emit('export', 'audit')">
          Audit Log
        </button>
      </div>

      <div v-if="error" class="admin-error">{{ error }}</div>

      <div class="admin-list">
        <div v-if="!loading && items.length === 0" class="admin-empty">
          Tidak ada koreksi yang menunggu review.
        </div>
        <div v-for="item in items" :key="item.id" class="admin-item">
          <div class="admin-item-header">
            <span class="admin-id">ID: {{ item.id }}</span>
            <span class="admin-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <div class="admin-block">
            <strong>Pertanyaan</strong>
            <p>{{ item.question || '-' }}</p>
          </div>
          <div class="admin-block">
            <strong>Jawaban AI</strong>
            <p>{{ item.answer || '-' }}</p>
          </div>
          <div class="admin-block">
            <strong>Koreksi</strong>
            <p>{{ item.correction }}</p>
          </div>
          <div class="admin-block">
            <strong>Sumber</strong>
            <p>{{ item.source || '-' }}</p>
          </div>
          <div class="admin-actions">
            <button class="btn reject" type="button" @click="$emit('reject', item.id)">Tolak</button>
            <button class="btn approve" type="button" @click="$emit('approve', item.id)">Setujui</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  props: {
    open: { type: Boolean, default: false },
    items: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' }
  },
  emits: ['close', 'refresh', 'approve', 'reject', 'logout', 'export'],
  methods: {
    formatTime(value) {
      if (!value) return ''
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return ''
      return date.toLocaleString('id-ID', {
        day: '2-digit',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.admin-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 80;
  padding: 1rem;
}

.admin-card {
  width: min(820px, 96vw);
  max-height: 90vh;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 1.25rem;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.admin-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.admin-header p {
  margin: 0.25rem 0 0;
  color: var(--text-secondary);
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

.admin-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

.admin-status {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.2);
}

.admin-actions-row {
  display: inline-flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.admin-export {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.btn.export {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
}

.btn.export:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn {
  padding: 0.55rem 1rem;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  font-weight: 600;
}

.btn.refresh {
  background: var(--surface-2);
  border-color: var(--border-color);
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.btn.logout {
  background: transparent;
  border-color: var(--border-color);
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.btn.logout:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.admin-error {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid #ef4444;
  color: #ef4444;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
}

.admin-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.admin-item {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.9rem;
  background: var(--surface-2);
}

.admin-item-header {
  display: flex;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 0.8rem;
  margin-bottom: 0.6rem;
}

.admin-block strong {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 0.2rem;
}

.admin-block p {
  margin: 0 0 0.5rem;
  color: var(--text-primary);
  white-space: pre-wrap;
}

.admin-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}

.btn.reject {
  background: transparent;
  border-color: #ef4444;
  color: #ef4444;
}

.btn.approve {
  background: #22c55e;
  border-color: #22c55e;
  color: #fff;
}

.admin-empty {
  text-align: center;
  color: var(--text-secondary);
  padding: 1.5rem;
}
</style>
