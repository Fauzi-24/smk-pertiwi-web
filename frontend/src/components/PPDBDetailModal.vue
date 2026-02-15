<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content detail-modal">
        <div class="modal-header">
          <h2><i class="fas fa-user-graduate"></i> Detail Pendaftar</h2>
          <button @click="closeModal" class="close-btn" aria-label="Tutup">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div v-if="data" class="detail-sections">
            <!-- Personal Info -->
            <div class="detail-section">
              <h3><i class="fas fa-user"></i> Data Pribadi</h3>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>NISN</label>
                  <p>{{ data.nisn }}</p>
                </div>
                <div class="detail-item">
                  <label>NIK</label>
                  <p>{{ data.nik }}</p>
                </div>
                <div class="detail-item full-width">
                  <label>Nama Lengkap</label>
                  <p class="highlight">{{ data.full_name }}</p>
                </div>
                <div class="detail-item">
                  <label>Tempat Lahir</label>
                  <p>{{ data.birthplace }}</p>
                </div>
                <div class="detail-item">
                  <label>Tanggal Lahir</label>
                  <p>{{ formatDate(data.birthdate) }}</p>
                </div>
                <div class="detail-item">
                  <label>Jenis Kelamin</label>
                  <p>{{ data.gender === 'L' ? 'Laki-laki' : 'Perempuan' }}</p>
                </div>
                <div class="detail-item">
                  <label>Agama</label>
                  <p>{{ data.religion }}</p>
                </div>
                <div class="detail-item full-width">
                  <label>Alamat</label>
                  <p>{{ data.address }}</p>
                </div>
                <div class="detail-item">
                  <label>No. HP</label>
                  <p><i class="fas fa-phone"></i> {{ data.phone }}</p>
                </div>
                <div class="detail-item">
                  <label>Email</label>
                  <p><i class="fas fa-envelope"></i> {{ data.email }}</p>
                </div>
              </div>
            </div>

            <!-- School Info -->
            <div class="detail-section">
              <h3><i class="fas fa-graduation-cap"></i> Data Sekolah</h3>
              <div class="detail-grid">
                <div class="detail-item full-width">
                  <label>Asal Sekolah</label>
                  <p>{{ data.previous_school || data.school_origin }}</p>
                </div>
                <div class="detail-item">
                  <label>Jurusan Dipilih</label>
                  <p class="badge-major">{{ data.major }}</p>
                </div>
              </div>
            </div>

            <!-- Parent Info -->
            <div class="detail-section">
              <h3><i class="fas fa-users"></i> Data Orang Tua</h3>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>Nama Ayah</label>
                  <p>{{ data.father_name }}</p>
                </div>
                <div class="detail-item">
                  <label>Pekerjaan Ayah</label>
                  <p>{{ data.father_job }}</p>
                </div>
                <div class="detail-item">
                  <label>Nama Ibu</label>
                  <p>{{ data.mother_name }}</p>
                </div>
                <div class="detail-item">
                  <label>Pekerjaan Ibu</label>
                  <p>{{ data.mother_job }}</p>
                </div>
                <div class="detail-item full-width">
                  <label>No. HP Orang Tua</label>
                  <p><i class="fas fa-phone"></i> {{ data.parent_phone }}</p>
                </div>
              </div>
            </div>

            <!-- Registration Info -->
            <div class="detail-section">
              <h3><i class="fas fa-info-circle"></i> Informasi Pendaftaran</h3>
              <div class="detail-grid">
                <div class="detail-item">
                  <label>Tanggal Daftar</label>
                  <p>{{ formatDateTime(data.created_at) }}</p>
                </div>
                <div class="detail-item">
                  <label>Status</label>
                  <p>
                    <span :class="['status-badge', `status-${data.status}`]">
                      {{ getStatusText(data.status) }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-secondary">
            <i class="fas fa-times"></i> Tutup
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'PPDBDetailModal',
  props: {
    isOpen: Boolean,
    data: Object
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('id-ID', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    },
    formatDateTime(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('id-ID', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    getStatusText(status) {
      const statusMap = {
        'pending': 'Menunggu',
        'accepted': 'Diterima',
        'rejected': 'Ditolak'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  overflow-y: auto;
}

.modal-content.detail-modal {
  background: var(--surface);
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--surface-2);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: var(--hover);
  color: var(--text-primary);
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.detail-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.detail-section {
  background: var(--surface-2);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
}

.detail-section h3 {
  margin: 0 0 1.25rem 0;
  color: var(--primary-color);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--primary-color);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.25rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item p {
  margin: 0;
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 500;
}

.detail-item p.highlight {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary-color);
}

.detail-item p i {
  margin-right: 0.5rem;
  color: var(--primary-color);
}

.badge-major {
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 600;
  display: inline-block;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: capitalize;
  display: inline-block;
}

.status-pending { background: #fef3c7; color: #d97706; }
.status-accepted { background: #dcfce7; color: #16a34a; }
.status-rejected { background: #fee2e2; color: #dc2626; }

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: var(--surface-2);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-secondary {
  background: var(--border-color);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: var(--hover);
  transform: translateY(-2px);
}

/* Animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: transform 0.3s;
}

.modal-fade-enter-from .modal-content {
  transform: scale(0.9);
}

.modal-fade-leave-to .modal-content {
  transform: scale(0.9);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .modal-content.detail-modal {
    max-height: 95vh;
  }

  .modal-header,
  .modal-footer {
    padding: 1rem 1.5rem;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .detail-item.full-width {
    grid-column: 1;
  }
}
</style>
