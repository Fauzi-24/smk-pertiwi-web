<template>
  <div v-if="open" class="feedback-overlay" @click.self="$emit('cancel')">
    <div class="feedback-card">
      <div class="feedback-header">
        <h3>Perbaiki Jawaban</h3>
        <button class="icon-btn" type="button" @click="$emit('cancel')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <div class="feedback-section">
        <label>Pertanyaan</label>
        <div class="feedback-preview">{{ question || '-' }}</div>
      </div>

      <div class="feedback-section">
        <label>Jawaban AI</label>
        <div class="feedback-preview">{{ answer || '-' }}</div>
      </div>

      <div class="feedback-section">
        <label>Koreksi / Jawaban yang Benar</label>
        <textarea v-model="correction" rows="4" placeholder="Tulis jawaban yang benar di sini..."></textarea>
      </div>

      <div class="feedback-section">
        <label>Sumber (opsional)</label>
        <input v-model="source" type="text" placeholder="Contoh: Dokumen sekolah, link resmi, dll" />
      </div>

      <div class="feedback-actions">
        <button class="btn cancel" type="button" @click="$emit('cancel')">Batal</button>
        <button class="btn submit" type="button" :disabled="!correction.trim() || loading" @click="submit">
          {{ loading ? 'Mengirim...' : 'Kirim Koreksi' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeedbackDialog',
  props: {
    open: { type: Boolean, default: false },
    question: { type: String, default: '' },
    answer: { type: String, default: '' },
    loading: { type: Boolean, default: false }
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      correction: '',
      source: ''
    }
  },
  watch: {
    open(isOpen) {
      if (isOpen) {
        this.correction = ''
        this.source = ''
      }
    }
  },
  methods: {
    submit() {
      this.$emit('submit', {
        correction: this.correction,
        source: this.source
      })
    }
  }
}
</script>

<style scoped>
.feedback-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 70;
  padding: 1rem;
}

.feedback-card {
  width: min(560px, 92vw);
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.feedback-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.feedback-header h3 {
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

.feedback-section label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-primary);
  display: block;
  margin-bottom: 0.4rem;
}

.feedback-preview {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.6rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  max-height: 120px;
  overflow-y: auto;
  white-space: pre-wrap;
}

.feedback-section textarea,
.feedback-section input {
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  padding: 0.6rem;
  font-family: inherit;
  font-size: 0.9rem;
  background: var(--surface);
  color: var(--text-primary);
}

.feedback-actions {
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
  border-color: var(--primary-color);
  color: var(--text-primary);
}

.btn.submit {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.btn.submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
