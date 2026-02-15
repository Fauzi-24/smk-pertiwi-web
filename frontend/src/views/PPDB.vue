<template>
  <div class="page-container">
    <div class="header-section">
      <h1>{{ $t('ppdb.title') }}</h1>
      <p>{{ $t('ppdb.subtitle') }}</p>
    </div>

    <div class="ppdb-container">
      <div class="tabs">
        <button 
          :class="['tab-btn', { active: activeTab === 'register' }]"
          @click="activeTab = 'register'"
        >
          <i class="fas fa-user-plus"></i> {{ $t('ppdb.tab_register') }}
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'check' }]"
          @click="activeTab = 'check'"
        >
          <i class="fas fa-search"></i> {{ $t('ppdb.tab_check') }}
        </button>
      </div>

      <!-- Register Form -->
      <div v-if="activeTab === 'register'" class="form-card fade-in">
        <div class="register-info">
          <div class="info-icon">
            <i class="fas fa-graduation-cap"></i>
          </div>
          <h2>{{ $t('ppdb.info_title') }} {{ new Date().getFullYear() + 1 }}</h2>
          <p>{{ $t('ppdb.info_desc') }}</p>
          
          <div class="info-cards">
            <div class="info-card">
              <i class="fas fa-calendar"></i>
              <h3>{{ $t('ppdb.period') }}</h3>
              <p>1 Januari - 31 Maret {{ new Date().getFullYear() }}</p>
            </div>
            <div class="info-card">
              <i class="fas fa-book"></i>
              <h3>7 Jurusan</h3>
              <p>RPL, TKJ, TKR, TSM, TO, LP, BDP</p>
            </div>
            <div class="info-card">
              <i class="fas fa-users"></i>
              <h3>{{ $t('ppdb.quota') }}</h3>
              <p>{{ $t('ppdb.quota_desc') }}</p>
            </div>
          </div>

          <router-link to="/ppdb/daftar" class="btn-register">
            <i class="fas fa-edit"></i>
            {{ $t('ppdb.btn_start') }}
          </router-link>
        </div>
      </div>

      <!-- Check Status -->
      <div v-if="activeTab === 'check'" class="form-card fade-in">
        <div class="check-box">
          <label>{{ $t('ppdb.input_nisn') }}</label>
          <div class="input-group">
            <input v-model="checkNisn" type="text" :placeholder="$t('ppdb.search_placeholder')">
            <button @click="checkStatus" :disabled="loading">
              <i class="fas fa-search"></i>
            </button>
          </div>
        </div>

        <div v-if="checkResult" class="status-result slide-up">
          <h3>{{ $t('ppdb.status_title') }}</h3>
          <div class="result-details">
            <div class="detail-row">
              <span>Nama:</span>
              <strong>{{ checkResult.full_name }}</strong>
            </div>
            <div class="detail-row">
              <span>Asal Sekolah:</span>
              <strong>{{ checkResult.school_origin }}</strong>
            </div>
            <div class="detail-row">
              <span>Jurusan:</span>
              <strong>{{ checkResult.major_choice }}</strong>
            </div>
            <div class="detail-row">
              <span>Status:</span>
              <span :class="['badge', checkResult.status]">{{ $t('ppdb.status_' + checkResult.status.toLowerCase()) }}</span>
            </div>
             <div class="detail-row" v-if="checkResult.notes">
              <span>Catatan:</span>
              <p>{{ checkResult.notes }}</p>
            </div>
          </div>
        </div>
        <div v-if="checkError" class="error-alert">{{ checkError }}</div>
      </div>
    </div>

    <!-- Print Area (Hidden unless printing) -->
    <div id="print-area" class="print-only" v-if="regSuccess">
      <div class="print-header">
        <img src="../assets/SMK_PERTIWI_KUNINGAN-removebg-preview.png" alt="Logo SMK Pertiwi Kuningan" loading="lazy">
        <div class="header-text">
          <h2>PANITIAP PENERIMAAN PESERTA DIDIK BARU</h2>
          <h3>SMK PERTIWI KUNINGAN</h3>
          <p>Jl. Siliwangi No.26A, Kasturi, Kec. Cilimus, Kabupaten Kuningan</p>
        </div>
      </div>
      <hr>
      <div class="print-content">
        <h4>BUKTI PENDAFTARAN ONLINE</h4>
        <table>
          <tr><td>No. Pendaftaran</td><td>: {{ regResult.id || '-' }}</td></tr>
          <tr><td>NISN</td><td>: {{ regResult.nisn }}</td></tr>
          <tr><td>Nama Lengkap</td><td>: {{ regResult.full_name }}</td></tr>
          <tr><td>Asal Sekolah</td><td>: {{ regResult.school_origin }}</td></tr>
          <tr><td>Jurusan Pilihan</td><td>: {{ regResult.major_choice }}</td></tr>
          <tr><td>Tanggal Daftar</td><td>: {{ new Date().toLocaleDateString() }}</td></tr>
        </table>
        <div class="print-notes">
          <p>Simpan bukti ini dan bawa saat verifikasi berkas di sekolah.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'
import ChatAPI from '../services/api' /* Utilizing ChatAPI for Axios instance if possible, or fetch directly */
/* We need to ensure ChatAPI can handle custom requests or import axios */
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export default {
  name: 'PPDB',
  data() {
    return {
      activeTab: 'register',
      majors: schoolData.majors,
      form: {
        nisn: '',
        full_name: '',
        school_origin: '',
        email: '',
        phone: '',
        parent_name: '',
        parent_phone: '',
        major_choice: '',
        address: ''
      },
      loading: false,
      error: '',
      regSuccess: false,
      regResult: null,
      checkNisn: '',
      checkResult: null,
      checkError: ''
    }
  },
  methods: {
    async submitRegistration() {
      this.loading = true
      this.error = ''
      try {
        const res = await axios.post(`${API_URL}/ppdb/register`, this.form)
        this.regResult = res.data
        this.regSuccess = true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Gagal mendaftar. Coba lagi.'
      } finally {
        this.loading = false
      }
    },
    async checkStatus() {
      if (!this.checkNisn) return
      this.loading = true
      this.checkError = ''
      this.checkResult = null
      try {
        const res = await axios.get(`${API_URL}/ppdb/status/${this.checkNisn}`)
        this.checkResult = res.data
      } catch (err) {
        this.checkError = 'Data tidak ditemukan.'
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.regSuccess = false
      this.form = {
        nisn: '', full_name: '', school_origin: '', email: '',
        phone: '', parent_name: '', parent_phone: '', major_choice: '', address: ''
      }
    },
    printProof() {
      window.print()
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 80px 1.5rem 4rem;
  min-height: 100vh;
  background: var(--background);
}

.header-section {
  text-align: center;
  margin-bottom: 2rem;
}

.ppdb-container {
  max-width: 800px;
  margin: 0 auto;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tab-btn {
  background: var(--surface);
  border: 1px solid var(--border-color);
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.form-card {
  background: var(--surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.register-info {
  text-align: center;
}

.info-icon {
  font-size: 4rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.register-info h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.register-info p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 2rem 0;
}

.info-card {
  background: var(--surface-2);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  text-align: center;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.info-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 0.75rem;
  display: block;
}

.info-card h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.info-card p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
}

.btn-register {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.5rem;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.btn-register:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--primary-rgb), 0.35);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.full {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--background);
  color: var(--text-primary);
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-submit {
  width: 100%;
  margin-top: 2rem;
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-submit:disabled {
  background: var(--gray-medium);
  cursor: not-allowed;
}

.success-message {
  text-align: center;
  padding: 2rem 0;
}

.success-message i {
  font-size: 4rem;
  color: #10B981;
  margin-bottom: 1rem;
}

.result-details {
  background: var(--surface-2);
  padding: 1.5rem;
  border-radius: 8px;
  text-align: left;
  margin: 1.5rem 0;
  border: 1px solid var(--border-color);
}

.result-details p {
  margin: 0.5rem 0;
  color: var(--text-primary);
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.badge.pending { background: #FEF3C7; color: #D97706; }
.badge.verified { background: #D1FAE5; color: #059669; }
.badge.rejected { background: #FEE2E2; color: #DC2626; }

.check-box {
  max-width: 500px;
  margin: 0 auto 2rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.input-group button {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.error-alert {
  background: #FEE2E2;
  color: #DC2626;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}

.print-only {
  display: none;
}

@media print {
  body * {
    visibility: hidden;
  }
  .print-only, .print-only * {
    visibility: visible;
  }
  .print-only {
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    padding: 2cm;
    background: white;
    color: black;
  }
  
  .print-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .print-header img {
    height: 80px;
  }
  
  .header-text h2 { margin: 0; font-size: 14pt; }
  .header-text h3 { margin: 0; font-size: 12pt; }
  .header-text p { margin: 0; font-size: 10pt; }
  
  table {
    width: 100%;
    margin-top: 2rem;
    border-collapse: collapse;
  }
  
  td {
    padding: 0.5rem;
    font-size: 12pt;
  }
}

.fade-in { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
