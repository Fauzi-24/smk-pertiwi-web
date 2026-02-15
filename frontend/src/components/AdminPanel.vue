<template>
  <div v-if="open" class="admin-overlay" @click.self="$emit('close')">
    <div class="admin-card">
      <div class="admin-header">
        <div>
          <h3>Admin Panel</h3>
          <p>Kelola data, feedback, dan konten.</p>
        </div>
        <button class="icon-btn" type="button" @click="$emit('close')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <div class="admin-tabs">
        <button 
          :class="['tab-btn', { active: activeTab === 'feedback' }]"
          @click="activeTab = 'feedback'"
        >
          Feedback
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'ppdb' }]"
          @click="loadPpdb"
        >
          PPDB
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'news' }]"
          @click="activeTab = 'news'"
        >
          Berita
        </button>
      </div>

      <div class="admin-controls">
        <div class="admin-status">
          <span class="status-dot"></span>
          <span>Login sebagai Admin</span>
        </div>
        <div class="admin-actions-row">
          <button class="btn refresh" type="button" :disabled="loading" @click="handleRefresh">
            <i class="fas fa-rotate"></i>
            {{ loading ? 'Memuat...' : 'Refresh' }}
          </button>
          <button class="btn logout" type="button" @click="$emit('logout')">
            <i class="fas fa-right-from-bracket"></i>
            Logout
          </button>
        </div>
      </div>

      <div v-if="error" class="admin-error">{{ error }}</div>

      <!-- Feedback Tab -->
      <div v-if="activeTab === 'feedback'" class="admin-list">
        <div v-if="!loading && items.length === 0" class="admin-empty">
          Tidak ada koreksi yang menunggu review.
        </div>
        <div v-for="item in items" :key="item.id" class="admin-item">
          <div class="admin-item-header">
            <span class="admin-id">ID: {{ item.id }}</span>
            <span class="admin-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <div class="admin-block"><strong>Pertanyaan:</strong> <p>{{ item.question || '-' }}</p></div>
          <div class="admin-block"><strong>Jawaban AI:</strong> <p>{{ item.answer || '-' }}</p></div>
          <div class="admin-block"><strong>Koreksi:</strong> <p>{{ item.correction }}</p></div>
          <div class="admin-actions">
            <button class="btn reject" type="button" @click="$emit('reject', item.id)">Tolak</button>
            <button class="btn approve" type="button" @click="$emit('approve', item.id)">Setujui</button>
          </div>
        </div>
      </div>

      <!-- PPDB Tab -->
      <div v-if="activeTab === 'ppdb'" class="admin-list">
        <div v-if="!loading && ppdbItems.length === 0" class="admin-empty">
          Belum ada pendaftar.
        </div>
        <div v-for="item in ppdbItems" :key="item.id" class="admin-item">
          <div class="admin-item-header">
            <span class="admin-id">NISN: {{ item.nisn }}</span>
            <span :class="['badge', item.status]">{{ item.status.toUpperCase() }}</span>
          </div>
          <div class="admin-grid-2">
            <div class="admin-block"><strong>Nama:</strong> <p>{{ item.full_name }}</p></div>
            <div class="admin-block"><strong>Asal:</strong> <p>{{ item.school_origin }}</p></div>
            <div class="admin-block"><strong>Jurusan:</strong> <p>{{ item.major_choice }}</p></div>
            <div class="admin-block"><strong>Ortu:</strong> <p>{{ item.parent_name }} ({{ item.parent_phone }})</p></div>
          </div>
          <div class="admin-actions">
            <button v-if="item.status !== 'verified'" class="btn verify" @click="updatePpdbStatus(item.nisn, 'verified')">Verifikasi</button>
            <button v-if="item.status !== 'accepted'" class="btn approve" @click="updatePpdbStatus(item.nisn, 'accepted')">Terima</button>
            <button v-if="item.status !== 'rejected'" class="btn reject" @click="updatePpdbStatus(item.nisn, 'rejected')">Tolak</button>
          </div>
        </div>
      </div>

      <!-- News Tab -->
      <div v-if="activeTab === 'news'" class="admin-list">
        <div class="news-form admin-item">
          <h4>Tambah Berita Baru</h4>
          <form @submit.prevent="createNews" class="admin-form">
            <div class="form-group">
              <label>Judul Berita</label>
              <input v-model="newsForm.title" type="text" required placeholder="Contoh: Juara 1 LKS Provinsi">
            </div>
            <div class="form-group">
              <label>Link Gambar (Opsional)</label>
              <input v-model="newsForm.image_url" type="url" placeholder="https://...">
            </div>
            <div class="form-group">
              <label>Konten Berita</label>
              <textarea v-model="newsForm.content" rows="4" required placeholder="Isi berita..."></textarea>
            </div>
            <div class="admin-actions">
              <button type="submit" class="btn approve" :disabled="newsLoading">
                {{ newsLoading ? 'Menyimpan...' : 'Publikasikan' }}
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = 'http://localhost:8000/api'

export default {
  name: 'AdminPanel',
  props: {
    open: { type: Boolean, default: false },
    items: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' },
    adminKey: { type: String, default: '' }
  },
  emits: ['close', 'refresh', 'approve', 'reject', 'logout', 'export'],
  data() {
    return {
      activeTab: 'feedback',
      ppdbItems: [],
      ppdbLoading: false,
      newsForm: {
        title: '',
        content: '',
        image_url: ''
      },
      newsLoading: false
    }
  },
  methods: {
    handleRefresh() {
      if (this.activeTab === 'feedback') {
        this.$emit('refresh')
      } else if (this.activeTab === 'ppdb') {
        this.loadPpdb()
      }
    },
    formatTime(value) {
      if (!value) return ''
      return new Date(value).toLocaleString('id-ID')
    },
    async loadPpdb() {
      this.activeTab = 'ppdb'
      this.ppdbLoading = true
      try {
        const key = localStorage.getItem('prism_admin_key')
        const res = await axios.get(`${API_URL}/admin/ppdb`, {
          headers: { 'x-admin-key': key }
        })
        this.ppdbItems = res.data.items || []
      } catch (err) {
        console.error(err)
      } finally {
        this.ppdbLoading = false
      }
    },
    async updatePpdbStatus(nisn, status) {
      if (!confirm(`Ubah status ke ${status}?`)) return
      try {
        const key = localStorage.getItem('prism_admin_key')
        await axios.post(`${API_URL}/admin/ppdb/${nisn}/status?status=${status}`, {}, {
          headers: { 'x-admin-key': key }
        })
        this.loadPpdb()
      } catch (err) {
        alert('Gagal update status')
      }
    },
    async createNews() {
      this.newsLoading = true
      try {
        const key = localStorage.getItem('prism_admin_key')
        await axios.post(`${API_URL}/admin/news`, this.newsForm, {
          headers: { 'x-admin-key': key }
        })
        alert('Berita berhasil dipublikasikan!')
        this.newsForm = { title: '', content: '', image_url: '' }
      } catch (err) {
        alert('Gagal membuat berita: ' + (err.response?.data?.detail || err.message))
      } finally {
        this.newsLoading = false
      }
    }
  },
  watch: {
    open(val) {
      if (val && this.activeTab === 'ppdb') {
        this.loadPpdb()
      }
    }
  }
}
</script>

<style scoped>
/* Inherited styles + new additions */
.admin-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.45); display: flex; align-items: center; justify-content: center; z-index: 80; padding: 1rem; }
.admin-card { width: min(820px, 96vw); max-height: 90vh; background: var(--surface); border: 1px solid var(--border-color); border-radius: 14px; padding: 1.25rem; box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 1rem; overflow-y: auto; }
.admin-header, .admin-controls { display: flex; justify-content: space-between; align-items: center; }
.admin-tabs { display: flex; gap: 1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.tab-btn { background: none; border: none; padding: 0.5rem 1rem; cursor: pointer; color: var(--text-secondary); border-bottom: 2px solid transparent; font-weight: 600; }
.tab-btn.active { color: var(--primary-color); border-bottom-color: var(--primary-color); }
.admin-list { display: flex; flex-direction: column; gap: 1rem; }
.admin-item { background: var(--surface-2); padding: 1rem; border-radius: 8px; border: 1px solid var(--border-color); }
.admin-item-header { display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); }
.admin-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
.btn { padding: 0.4rem 0.8rem; border-radius: 6px; cursor: pointer; border: 1px solid transparent; font-size: 0.85rem; font-weight: 600; }
.btn.approve { background: #10B981; color: white; }
.btn.reject { background: transparent; border-color: #EF4444; color: #EF4444; }
.btn.verify { background: #3B82F6; color: white; }
.btn.refresh { background: var(--surface-2); color: var(--text-secondary); border-color: var(--border-color); }
.btn.logout { color: #EF4444; background: transparent; }
.icon-btn { background: none; border: none; cursor: pointer; font-size: 1.2rem; color: var(--text-secondary); }
.status-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block; margin-right: 0.5rem; }
.badge { padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; background: #E5E7EB; color: #374151; }
.badge.pending { background: #FEF3C7; color: #D97706; }
.badge.verified { background: #DBEAFE; color: #1E40AF; }
.badge.accepted { background: #D1FAE5; color: #065F46; }
.badge.rejected { background: #FEE2E2; color: #991B1B; }

/* Form Styles */
.admin-form { display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem; }
.form-group label { display: block; margin-bottom: 0.4rem; font-size: 0.9rem; font-weight: 600; }
.form-group input, .form-group textarea { width: 100%; padding: 0.6rem; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.95rem; }
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--primary-color); }
h4 { margin: 0; color: var(--text-primary); }
</style>
