<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-content">
        <h1><i class="fas fa-tachometer-alt"></i> Admin Dashboard</h1>
        <div class="header-actions">
           <span class="admin-badge"><i class="fas fa-user-circle"></i> Administrator</span>
           <button @click="handleLogout" class="logout-btn">
             <i class="fas fa-sign-out-alt"></i> Logout
           </button>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
       <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon blue"><i class="fas fa-users"></i></div>
            <div class="stat-info">
              <h3>Total Pendaftar</h3>
              <p>{{ stats.total }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon orange"><i class="fas fa-clock"></i></div>
            <div class="stat-info">
              <h3>Menunggu</h3>
              <p>{{ stats.pending }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon green"><i class="fas fa-check-circle"></i></div>
            <div class="stat-info">
              <h3>Diterima</h3>
              <p>{{ stats.accepted }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon red"><i class="fas fa-times-circle"></i></div>
            <div class="stat-info">
              <h3>Ditolak</h3>
              <p>{{ stats.rejected }}</p>
            </div>
          </div>
       </div>

       <div class="charts-section" v-if="stats.total > 0">
         <div class="chart-card">
           <h3><i class="fas fa-chart-bar"></i> Statistik Pendaftar per Jurusan</h3>
           <div class="bar-chart">
             <div v-for="(count, major) in stats.per_major" :key="major" class="bar-item">
               <div class="bar-label">{{ major }}</div>
               <div class="bar-track">
                 <div class="bar-fill" :style="{ width: (count / stats.total * 100) + '%' }"></div>
                 <span class="bar-value">{{ count }}</span>
               </div>
             </div>
           </div>
         </div>
       </div>

       <div class="data-section">
         <div class="section-header">
           <h2><i class="fas fa-table"></i> Data PPDB Online</h2>
           <div class="header-actions">
             <div class="search-box">
               <i class="fas fa-search"></i>
               <input v-model="searchQuery" placeholder="Cari nama atau NISN...">
             </div>
             <button @click="exportToExcel" class="btn-export" title="Export ke Excel">
               <i class="fas fa-file-excel"></i> Export Excel
             </button>
           </div>
         </div>

         <div class="filter-section">
           <div class="filter-group">
             <label><i class="fas fa-filter"></i> Filter Jurusan:</label>
             <select v-model="filterJurusan" class="filter-select">
               <option value="">Semua Jurusan</option>
               <option value="Teknik Komputer dan Jaringan">TKJ</option>
               <option value="Rekayasa Perangkat Lunak">RPL</option>
               <option value="Multimedia">Multimedia</option>
               <option value="Bisnis Daring dan Pemasaran">BDP</option>
               <option value="Otomatisasi Tata Kelola Perkantoran">OTKP</option>
               <option value="Akuntansi dan Keuangan Lembaga">AKL</option>
             </select>
           </div>
           
           <div class="filter-group">
             <label><i class="fas fa-calendar-alt"></i> Tanggal:</label>
             <input type="date" v-model="filterStartDate" class="filter-date" placeholder="Dari">
             <span class="separator">-</span>
             <input type="date" v-model="filterEndDate" class="filter-date" placeholder="Sampai">
           </div>

           <button v-if="hasActiveFilters" @click="resetFilters" class="btn-reset-filters" title="Reset Filter">
             <i class="fas fa-undo"></i> Reset
           </button>
         </div>

         <div class="tabs-container">
           <button 
             :class="['tab-btn', { active: activeTab === 'all' }]" 
             @click="activeTab = 'all'"
           >
             Semua
           </button>
           <button 
             :class="['tab-btn', { active: activeTab === 'pending' }]" 
             @click="activeTab = 'pending'"
           >
             Pending <span v-if="pendingCount" class="tab-badge">{{ pendingCount }}</span>
           </button>
           <button 
             :class="['tab-btn', { active: activeTab === 'accepted' }]" 
             @click="activeTab = 'accepted'"
           >
             Diterima
           </button>
           <button 
             :class="['tab-btn', { active: activeTab === 'rejected' }]" 
             @click="activeTab = 'rejected'"
           >
             Ditolak
           </button>
         </div>

        <div v-if="loading" class="loading-state">
          <i class="fas fa-spinner fa-spin"></i> Memuat Data...
        </div>

        <div v-else-if="error" class="error-state">
          <i class="fas fa-exclamation-triangle"></i> {{ error }}
        </div>

        <div v-else class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th @click="sortBy('created_at')" class="sortable">
                  Tanggal 
                  <i v-if="sortColumn === 'created_at'" :class="sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'"></i>
                  <i v-else class="fas fa-sort" style="opacity: 0.3"></i>
                </th>
                <th @click="sortBy('nisn')" class="sortable">
                  NISN 
                  <i v-if="sortColumn === 'nisn'" :class="sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'"></i>
                  <i v-else class="fas fa-sort" style="opacity: 0.3"></i>
                </th>
                <th @click="sortBy('full_name')" class="sortable">
                  Nama Lengkap 
                  <i v-if="sortColumn === 'full_name'" :class="sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'"></i>
                  <i v-else class="fas fa-sort" style="opacity: 0.3"></i>
                </th>
                <th>Jurusan</th>
                <th>Asal Sekolah</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in filteredData" :key="item.id">
                <td>{{ index + 1 }}</td>
                <td>{{ formatDate(item.created_at) }}</td>
                <td><span class="mono">{{ item.nisn }}</span></td>
                <td class="name-cell">{{ item.full_name }}</td>
                <td><span class="badge badge-major">{{ item.major_choice }}</span></td>
                <td>{{ item.school_origin }}</td>
                <td>
                  <span :class="['status-badge', item.status.toLowerCase()]">{{ item.status }}</span>
                </td>
                <td>
                  <div class="action-btns">
                    <button @click="viewDetail(item)" class="btn-icon" title="Lihat Detail">
                      <i class="fas fa-eye"></i>
                    </button>
                    <button v-if="item.status === 'pending'" @click="confirmUpdate(item.id, 'accepted')" class="btn-icon success" title="Terima">
                      <i class="fas fa-check"></i>
                    </button>
                    <button v-if="item.status === 'pending'" @click="confirmUpdate(item.id, 'rejected')" class="btn-icon danger" title="Tolak">
                      <i class="fas fa-times"></i>
                    </button>
                    <button @click="confirmDelete(item.id)" class="btn-icon danger" title="Hapus">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredData.length === 0">
                <td colspan="8" class="empty-row">Tidak ada data ditemukan.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <PPDBDetailModal
      :is-open="detailModal.isOpen"
      :data="detailModal.data"
      @close="detailModal.isOpen = false"
    />

    <!-- Confirmation Modal -->
    <ConfirmationModal 
      :is-open="modal.isOpen"
      :title="modal.title"
      :message="modal.message"
      :confirm-text="modal.confirmText"
      :type="modal.type"
      @close="modal.isOpen = false"
      @confirm="handleConfirm"
    />
  </div>
</template>

<script>
import { ChatAPI } from '../services/api'
import ConfirmationModal from '../components/ConfirmationModal.vue'
import PPDBDetailModal from '../components/PPDBDetailModal.vue'

export default {
  name: 'AdminDashboard',
  components: {
    ConfirmationModal,
    PPDBDetailModal
  },
  data() {
    return {
      ppdbData: [],
      loading: true,
      error: '',
      searchQuery: '',
      activeTab: 'all',
      sortColumn: '', 
      sortDirection: 'asc',
      filterJurusan: '',
      filterStartDate: '',
      filterEndDate: '',
      detailModal: {
        isOpen: false,
        data: null
      },
      modal: {
        isOpen: false,
        title: '',
        message: '',
        confirmText: 'Ya',
        type: 'primary',
        action: null
      },
      stats: {
        total: 0,
        verified: 0,
        pending: 0,
        rejected: 0,
        per_major: {}
      }
    }
  },
  computed: {
    filteredData() {
      let data = this.ppdbData
      
      // Filter by Tab
      if (this.activeTab !== 'all') {
        data = data.filter(item => item.status === this.activeTab)
      }

      // Filter by search
      if (this.searchQuery) {
        const lower = this.searchQuery.toLowerCase()
        data = data.filter(item => 
          item.full_name.toLowerCase().includes(lower) ||
          item.nisn.toLowerCase().includes(lower) ||
          item.school_origin.toLowerCase().includes(lower)
        )
      }

      // Filter by Jurusan
      if (this.filterJurusan) {
        data = data.filter(item => item.major_choice === this.filterJurusan)
      }

      // Filter by Date Range
      if (this.filterStartDate) {
        const start = new Date(this.filterStartDate)
        start.setHours(0, 0, 0, 0) // Start of day
        data = data.filter(item => new Date(item.created_at) >= start)
      }

      if (this.filterEndDate) {
        const end = new Date(this.filterEndDate)
        end.setHours(23, 59, 59, 999) // End of day
        data = data.filter(item => new Date(item.created_at) <= end)
      }

      // Apply sorting
      if (this.sortColumn) {
        data = [...data].sort((a, b) => {
          let aVal = a[this.sortColumn]
          let bVal = b[this.sortColumn]

          // Handle dates
          if (this.sortColumn === 'created_at') {
            aVal = new Date(aVal)
            bVal = new Date(bVal)
          } else {
            // Convert to lowercase for string comparison
            aVal = String(aVal).toLowerCase()
            bVal = String(bVal).toLowerCase()
          }

          if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1
          if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1
          return 0
        })
      }

      return data
    },
    pendingCount() {
      return this.ppdbData.filter(i => i.status === 'pending').length
    },
    acceptedCount() {
      return this.ppdbData.filter(i => i.status === 'accepted').length
    },
    rejectedCount() {
      return this.ppdbData.filter(i => i.status === 'rejected').length
    },
    hasActiveFilters() {
      return this.filterJurusan || this.filterStartDate || this.filterEndDate
    }
  },
  async mounted() {
    await Promise.all([
      this.loadData(),
      this.getStats()
    ])
  },
  methods: {
    async loadData() {
      this.loading = true
      const token = localStorage.getItem('admin_token')
      
      if (!token) {
        this.$router.push('/admin/login')
        return
      }

      try {
        const data = await ChatAPI.getPPDBData(token)
        this.ppdbData = data
      } catch (err) {
        this.error = 'Gagal memuat data. Sesi mungkin kadaluarsa.'
        if (err.message.includes('401') || err.message.includes('Unauthorized')) {
          localStorage.removeItem('admin_token')
          this.$router.push('/admin/login')
        }
      } finally {
        this.loading = false
      }
    },
    async getStats() {
      const token = localStorage.getItem('admin_token')
      if (!token) return
      
      try {
        const stats = await ChatAPI.getDashboardStats(token)
        this.stats = stats
      } catch (err) {
        console.error('Failed to load stats:', err)
      }
    },
    confirmUpdate(id, status) {
      this.modal = {
        isOpen: true,
        title: status === 'accepted' ? 'Terima Pendaftaran' : 'Tolak Pendaftaran',
        message: `Apakah Anda yakin ingin ${status === 'accepted' ? 'menerima' : 'menolak'} pendaftaran ini?`,
        confirmText: status === 'accepted' ? 'Ya, Terima' : 'Ya, Tolak',
        type: status === 'accepted' ? 'success' : 'danger',
        action: () => this.updateStatus(id, status)
      }
    },
    confirmDelete(id) {
       this.modal = {
        isOpen: true,
        title: 'Hapus Data',
        message: 'Apakah Anda yakin ingin menghapus data ini? Data yang dihapus tidak dapat dikembalikan.',
        confirmText: 'Ya, Hapus',
        type: 'danger',
        action: () => this.deleteItem(id)
      }
    },
    handleConfirm() {
      if (this.modal.action) {
        this.modal.action()
      }
      this.modal.isOpen = false
    },
    async updateStatus(id, newStatus) {
      const token = localStorage.getItem('admin_token')
      try {
        await ChatAPI.updatePPDBStatus(id, newStatus, token)
        
        // Update local state
        const index = this.ppdbData.findIndex(item => item.id === id)
        if (index !== -1) {
          this.ppdbData[index].status = newStatus
        }
        
        if (window.$toast) window.$toast(`Status berhasil diubah ke ${newStatus}`, 'success')
      } catch (err) {
        if (window.$toast) window.$toast('Gagal mengubah status', 'error')
      }
    },
    async deleteItem(id) {
      const token = localStorage.getItem('admin_token')
      try {
        await ChatAPI.deletePPDBData(id, token)
        this.ppdbData = this.ppdbData.filter(item => item.id !== id)
        if (window.$toast) window.$toast('Data berhasil dihapus', 'success')
      } catch (err) {
        if (window.$toast) window.$toast('Gagal menghapus data', 'error')
      }
    },
    handleLogout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/admin/login')
    },
    resetFilters() {
      this.filterJurusan = ''
      this.filterStartDate = ''
      this.filterEndDate = ''
    },
    exportToExcel() {
      if (this.filteredData.length === 0) {
        window.$toast('Tidak ada data untuk di-export', 'warning')
        return
      }

      // Prepare headers with clear sections
      const headers = [
        '=== DATA PRIBADI ===',
        'No',
        'Tanggal Daftar',
        'NISN',
        'NIK',
        'Nama Lengkap',
        'Tempat Lahir',
        'Tanggal Lahir',
        'Jenis Kelamin',
        'Agama',
        'Alamat',
        'No. HP Siswa',
        'Email Siswa',
        '',
        '=== DATA SEKOLAH ===',
        'Asal Sekolah',
        'Jurusan Dipilih',
        '',
        '=== DATA ORANG TUA ===',
        'Nama Ayah',
        'Pekerjaan Ayah',
        'Nama Ibu',
        'Pekerjaan Ibu',
        'No. HP Orang Tua',
        '',
        '=== STATUS PENDAFTARAN ===',
        'Status'
      ]

      // Build CSV with organized structure
      let csvContent = ''
      
      // Add title row
      csvContent += `"DATA PENDAFTARAN PPDB SMK PERTIWI KUNINGAN"\n`
      csvContent += `"Tanggal Export: ${new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}"\n`
      csvContent += `"Total Data: ${this.filteredData.length} pendaftar"\n`
      csvContent += '\n'

      // Add data rows
      this.filteredData.forEach((item, index) => {
        const row = [
          '', // Section marker
          index + 1,
          this.formatDate(item.created_at),
          item.nisn || '-',
          item.nik || '-',
          item.full_name || '-',
          item.birthplace || '-',
          item.birthdate || '-',
          item.gender === 'L' ? 'Laki-laki' : item.gender === 'P' ? 'Perempuan' : '-',
          item.religion || '-',
          item.address || '-',
          item.phone || '-',
          item.email || '-',
          '',
          '', // School section marker
          item.previous_school || item.school_origin || '-',
          item.major || item.major_choice || '-',
          '',
          '', // Parent section marker
          item.father_name || '-',
          item.father_job || '-',
          item.mother_name || '-',
          item.mother_job || '-',
          item.parent_phone || '-',
          '',
          '', // Status section marker
          this.getStatusText(item.status)
        ]
        
        // Escape and join
        const escapedRow = row.map(value => {
          const str = String(value)
          return `"${str.replace(/"/g, '""')}"`
        }).join(',')
        
        csvContent += escapedRow + '\n'
      })

      // Create download
      const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      const date = new Date().toISOString().split('T')[0]
      
      link.setAttribute('href', url)
      link.setAttribute('download', `PPDB_SMK_Pertiwi_${date}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      window.$toast(`${this.filteredData.length} data berhasil di-export!`, 'success')
    },
    getStatusText(status) {
      const statusMap = {
        'pending': 'Menunggu',
        'accepted': 'Diterima',
        'rejected': 'Ditolak'
      }
      return statusMap[status] || status
    },
    sortBy(column) {
      // Toggle direction if clicking same column
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        // New column, default to ascending
        this.sortColumn = column
        this.sortDirection = 'asc'
      }
    },
    viewDetail(item) {
      this.detailModal = {
        isOpen: true,
        data: item
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('id-ID', {
        day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: var(--background);
  padding-bottom: 4rem;
}

.dashboard-header {
  background: var(--surface);
  border-bottom: 1px solid var(--border-color);
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.admin-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.logout-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #b91c1c;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--surface);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: var(--shadow);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.blue { background: rgba(37, 99, 235, 0.1); color: var(--primary-color); }
.stat-icon.orange { background: #fef3c7; color: #d97706; }
.stat-icon.green { background: #dcfce7; color: #16a34a; }

.tabs-container {
  padding: 0 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  gap: 1rem;
  background: var(--surface-2);
}

.tab-btn {
  background: none;
  border: none;
  padding: 1rem 0.5rem;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn:hover {
  color: var(--primary-color);
}

.tab-btn.active {
  color: var(--primary-color);
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary-color);
}

.tab-badge {
  background: #dc2626;
  color: white;
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
}

.stat-info h3 { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.25rem; font-weight: 500; }
.stat-info p { font-size: 1.75rem; font-weight: 700; color: var(--text-primary); }

.data-section {
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  box-shadow: var(--shadow);
}

.section-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h2 { font-size: 1.25rem; display: flex; align-items: center; gap: 0.75rem; }

.search-box {
  position: relative;
  width: 300px;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-box input {
  width: 100%;
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--surface-2);
  color: var(--text-primary);
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table th {
  background: var(--surface-2);
  color: var(--text-primary);
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid var(--border-color);
  font-size: 0.9rem;
  white-space: nowrap;
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.data-table th.sortable:hover {
  background: var(--hover);
}

.data-table th.sortable i {
  margin-left: 0.5rem;
  font-size: 0.85rem;
}

.data-table td { font-size: 0.95rem; color: var(--text-primary); }
.data-table tr:hover { background: rgba(0,0,0,0.02); }

.mono { font-family: monospace; font-size: 1rem; }
.name-cell { font-weight: 600; }

.badge-major {
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.pending { background: #fef08a; color: #854d0e; }
.status-badge.verified { background: #bfdbfe; color: #1e40af; }
.status-badge.accepted { background: #bbf7d0; color: #166534; }
.status-badge.rejected { background: #fecaca; color: #991b1b; }

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btns {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-icon {
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.btn-icon:hover {
  transform: translateY(-2px);
  background: rgba(37, 99, 235, 0.2);
}

.btn-icon.success {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}

.btn-icon.success:hover {
  background: rgba(22, 163, 74, 0.2);
}

.btn-icon.danger {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.btn-icon.danger:hover {
  background: rgba(220, 38, 38, 0.2);
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-btn:hover { background: rgba(0,0,0,0.05); transform: scale(1.1); }

.action-btn.approve { color: #16a34a; }
.action-btn.approve:hover { background: #dcfce7; }
.action-btn.reject { color: #dc2626; }
.action-btn.reject:hover { background: #fee2e2; }

.action-btn.delete { color: #991b1b; }
.action-btn.delete:hover { background: #fee2e2; }

.loading-state, .error-state, .empty-row {
  padding: 4rem;
  text-align: center;
  color: var(--text-secondary);
}

.error-state { color: #dc2626; }

/* Section Header Actions */
.section-header .header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-export:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-export i {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .section-header .header-actions {
    flex-direction: column;
    width: 100%;
    gap: 0.75rem;
  }
  
  .search-box,
  .btn-export {
    width: 100%;
  }
}

/* Advanced Filters Styles */
.filter-section {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-weight: 500;
  color: #64748b;
  font-size: 0.9rem;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #1e293b;
  min-width: 200px;
  outline: none;
  transition: all 0.3s ease;
}

.filter-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-date {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #1e293b;
  outline: none;
  transition: all 0.3s ease;
}

.filter-date:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.separator {
  color: #94a3b8;
  font-weight: 500;
}

.btn-reset-filters {
  margin-left: auto;
  background: #f1f5f9;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-reset-filters:hover {
  background: #e2e8f0;
  color: #475569;
}

/* Dashboard Analytics Styles */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.2s;
  border: 1px solid #e2e8f0;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  background: #f1f5f9;
  color: #475569;
}

.stat-icon.blue { background: #eff6ff; color: #3b82f6; }
.stat-icon.orange { background: #fff7ed; color: #f97316; }
.stat-icon.green { background: #f0fdf4; color: #22c55e; }
.stat-icon.red { background: #fef2f2; color: #ef4444; }

.stat-info h3 {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-info p {
  margin: 0.25rem 0 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
}

.charts-section {
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.chart-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  width: 240px;
  font-size: 0.9rem;
  color: #475569;
  font-weight: 500;
  text-align: right;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  background: #f1f5f9;
  height: 28px;
  border-radius: 6px;
  position: relative;
  overflow: visible; /* Allow value to sit outside if needed, though we put inside */
  display: flex;
  align-items: center;
}

.bar-fill {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  height: 100%;
  border-radius: 6px;
  transition: width 1s ease-out;
  min-width: 4px; /* Ensure tiny bars are visible */
}

.bar-value {
  margin-left: 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
  position: absolute;
  left: 100%;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .bar-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .bar-label {
    width: 100%;
    text-align: left;
  }
  
  .bar-track {
    width: 100%;
  }
  
  .bar-value {
    position: relative;
    left: auto;
  }
}
</style>
