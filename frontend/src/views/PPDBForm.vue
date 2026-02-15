<template>
  <div class="ppdb-form-page">
    <Breadcrumbs :crumbs="[
      { text: 'PPDB', to: '/ppdb' },
      { text: 'Formulir Pendaftaran' }
    ]" />
    
    <div class="form-header">
      <h1>Pendaftaran Siswa Baru</h1>
      <p>Formulir Pendaftaran SMK Pertiwi Kuningan {{ new Date().getFullYear() }}</p>
    </div>

    <!-- Progress Steps -->
    <div class="progress-steps">
      <div
        v-for="(step, index) in steps"
        :key="index"
        :class="['step', { active: currentStep === index, completed: currentStep > index }]"
      >
        <div class="step-number">
          <i v-if="currentStep > index" class="fas fa-check"></i>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <span class="step-label">{{ step }}</span>
      </div>
    </div>

    <!-- Form Steps -->
    <form @submit.prevent="handleSubmit" class="registration-form" novalidate>
      <!-- Step 1: Data Pribadi -->
      <div v-show="currentStep === 0" class="form-step">
        <h2>Data Pribadi Calon Siswa</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Nama Lengkap <span class="required">*</span></label>
            <input v-model="formData.namaLengkap" type="text" required placeholder="Sesuai ijazah" />
          </div>
          <div class="form-group">
            <label>NISN <span class="required">*</span></label>
            <input v-model="formData.nisn" type="text" required placeholder="10 digit" maxlength="10" />
          </div>
          <div class="form-group">
            <label>Tempat Lahir <span class="required">*</span></label>
            <input v-model="formData.tempatLahir" type="text" required />
          </div>
          <div class="form-group">
            <label>Tanggal Lahir <span class="required">*</span></label>
            <input v-model="formData.tanggalLahir" type="date" required />
          </div>
          <div class="form-group">
            <label>Jenis Kelamin <span class="required">*</span></label>
            <select v-model="formData.jenisKelamin" required>
              <option value="">Pilih...</option>
              <option value="L">Laki-laki</option>
              <option value="P">Perempuan</option>
            </select>
          </div>
          <div class="form-group">
            <label>Agama <span class="required">*</span></label>
            <select v-model="formData.agama" required>
              <option value="">Pilih...</option>
              <option value="Islam">Islam</option>
              <option value="Kristen">Kristen</option>
              <option value="Katolik">Katolik</option>
              <option value="Hindu">Hindu</option>
              <option value="Buddha">Buddha</option>
              <option value="Konghucu">Konghucu</option>
            </select>
          </div>
          <div class="form-group full-width">
            <label>Alamat Lengkap <span class="required">*</span></label>
            <textarea v-model="formData.alamat" required rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>No. Telepon/HP <span class="required">*</span></label>
            <input v-model="formData.noTelp" type="tel" required placeholder="08xxxxxxxxxx" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="formData.email" type="email" placeholder="email@contoh.com" />
          </div>
        </div>
      </div>

      <!-- Step 2: Data Orang Tua -->
      <div v-show="currentStep === 1" class="form-step">
        <h2>Data Orang Tua/Wali</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Nama Ayah <span class="required">*</span></label>
            <input v-model="formData.namaAyah" type="text" required />
          </div>
          <div class="form-group">
            <label>Pekerjaan Ayah <span class="required">*</span></label>
            <input v-model="formData.pekerjaanAyah" type="text" required />
          </div>
          <div class="form-group">
            <label>Nama Ibu <span class="required">*</span></label>
            <input v-model="formData.namaIbu" type="text" required />
          </div>
          <div class="form-group">
            <label>Pekerjaan Ibu <span class="required">*</span></label>
            <input v-model="formData.pekerjaanIbu" type="text" required />
          </div>
          <div class="form-group">
            <label>No. Telp Orang Tua <span class="required">*</span></label>
            <input v-model="formData.noTelpOrtu" type="tel" required placeholder="08xxxxxxxxxx" />
          </div>
          <div class="form-group">
            <label>Penghasilan Orang Tua <span class="required">*</span></label>
            <select v-model="formData.penghasilan" required>
              <option value="">Pilih...</option>
              <option value="< 1 juta">< 1 Juta</option>
              <option value="1-3 juta">1 - 3 Juta</option>
              <option value="3-5 juta">3 - 5 Juta</option>
              <option value="> 5 juta">> 5 Juta</option>
            </select>
          </div>
          <div class="form-group full-width">
            <label>Alamat Orang Tua <span class="required">*</span></label>
            <textarea v-model="formData.alamatOrtu" required rows="3"></textarea>
          </div>
        </div>
      </div>

      <!-- Step 3: Pilihan Jurusan & Asal Sekolah -->
      <div v-show="currentStep === 2" class="form-step">
        <h2>Pilihan Jurusan & Asal Sekolah</h2>
        <div class="form-grid">
          <div class="form-group full-width">
            <label>Pilihan Jurusan <span class="required">*</span></label>
            <select v-model="formData.jurusan" required>
              <option value="">Pilih Jurusan...</option>
              <option value="RPL">Rekayasa Perangkat Lunak (RPL)</option>
              <option value="TKJ">Teknik Komputer dan Jaringan (TKJ)</option>
              <option value="TKR">Teknik Kendaraan Ringan (TKR)</option>
              <option value="TSM">Teknik Sepeda Motor (TSM)</option>
              <option value="TO">Teknik Otomasi (TO)</option>
              <option value="LP">Layanan Perbankan (LP)</option>
              <option value="BDP">Bisnis Daring dan Pemasaran (BDP)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Asal Sekolah (SMP) <span class="required">*</span></label>
            <input v-model="formData.asalSekolah" type="text" required placeholder="Nama SMP" />
          </div>
          <div class="form-group">
            <label>Tahun Lulus <span class="required">*</span></label>
            <input v-model="formData.tahunLulus" type="number" required min="2020" max="2026" />
          </div>
          <div class="form-group">
            <label>Nilai Rata-rata UN/Ijazah</label>
            <input v-model="formData.nilaiRataRata" type="number" step="0.01" min="0" max="100" placeholder="0-100" />
          </div>
        </div>
      </div>

      <!-- Step 4: Konfirmasi -->
      <div v-show="currentStep === 3" class="form-step">
        <h2>Konfirmasi Data</h2>
        <div class="confirmation-box">
          <div class="confirm-section">
            <h3><i class="fas fa-user"></i> Data Pribadi</h3>
            <p><strong>Nama:</strong> {{ formData.namaLengkap }}</p>
            <p><strong>NISN:</strong> {{ formData.nisn }}</p>
            <p><strong>Tempat, Tanggal Lahir:</strong> {{ formData.tempatLahir }}, {{ formatDate(formData.tanggalLahir) }}</p>
            <p><strong>Jenis Kelamin:</strong> {{ formData.jenisKelamin === 'L' ? 'Laki-laki' : 'Perempuan' }}</p>
            <p><strong>Alamat:</strong> {{ formData.alamat }}</p>
            <p><strong>No. Telp:</strong> {{ formData.noTelp }}</p>
          </div>
          <div class="confirm-section">
            <h3><i class="fas fa-users"></i> Data Orang Tua</h3>
            <p><strong>Ayah:</strong> {{ formData.namaAyah }} ({{ formData.pekerjaanAyah }})</p>
            <p><strong>Ibu:</strong> {{ formData.namaIbu }} ({{ formData.pekerjaanIbu }})</p>
            <p><strong>Penghasilan:</strong> {{ formData.penghasilan }}</p>
          </div>
          <div class="confirm-section">
            <h3><i class="fas fa-graduation-cap"></i> Pendidikan</h3>
            <p><strong>Jurusan Pilihan:</strong> {{ formData.jurusan }}</p>
            <p><strong>Asal Sekolah:</strong> {{ formData.asalSekolah }}</p>
            <p><strong>Tahun Lulus:</strong> {{ formData.tahunLulus }}</p>
          </div>
        </div>
        <div class="agreement">
          <label class="checkbox-label">
            <input v-model="agreed" type="checkbox" required />
            <span>Saya menyatakan bahwa data yang saya masukkan adalah benar dan dapat dipertanggungjawabkan</span>
          </label>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="form-navigation">
        <button
          v-if="currentStep > 0"
          type="button"
          class="btn btn-secondary"
          @click="prevStep"
        >
          <i class="fas fa-arrow-left"></i> Kembali
        </button>
        <button
          v-if="currentStep < 3"
          type="button"
          class="btn btn-primary"
          @click="nextStep"
        >
          Lanjut <i class="fas fa-arrow-right"></i>
        </button>
        <button
          v-if="currentStep === 3"
          type="submit"
          class="btn btn-success"
          :disabled="!agreed || submitting"
        >
          <i class="fas fa-paper-plane"></i>
          {{ submitting ? 'Mengirim...' : 'Kirim Pendaftaran' }}
        </button>
      </div>
    </form>

    <!-- Success Modal -->
    <div v-if="showSuccess" class="modal">
      <div class="modal-content success">
        <div class="success-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <h2>Pendaftaran Berhasil!</h2>
        <p>Nomor Pendaftaran Anda:</p>
        <div class="registration-number">{{ registrationNumber }}</div>
        <p class="info-text">Simpan nomor pendaftaran ini untuk cek status</p>
        <button class="btn btn-primary" @click="resetForm">Daftar Lagi</button>
        <button class="btn btn-secondary" @click="goHome">Kembali ke Beranda</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import { ChatAPI } from '../services/api'

export default {
  name: 'PPDBForm',
  components: {
    Breadcrumbs
  },
  setup() {
    const router = useRouter()
    const currentStep = ref(0)
    const agreed = ref(false)
    const submitting = ref(false)
    const showSuccess = ref(false)
    const registrationNumber = ref('')

    const steps = ['Data Pribadi', 'Data Orang Tua', 'Pilihan Jurusan', 'Konfirmasi']

    const formData = reactive({
      namaLengkap: '',
      nisn: '',
      tempatLahir: '',
      tanggalLahir: '',
      jenisKelamin: '',
      agama: '',
      alamat: '',
      noTelp: '',
      email: '',
      namaAyah: '',
      pekerjaanAyah: '',
      namaIbu: '',
      pekerjaanIbu: '',
      noTelpOrtu: '',
      penghasilan: '',
      alamatOrtu: '',
      jurusan: '',
      asalSekolah: '',
      tahunLulus: new Date().getFullYear(),
      nilaiRataRata: ''
    })

    const validateCurrentStep = () => {
      // Step 0: Data Pribadi
      if (currentStep.value === 0) {
        if (!formData.namaLengkap) return 'Nama Lengkap harus diisi'
        if (!formData.nisn || formData.nisn.length !== 10) return 'NISN harus 10 digit'
        if (!formData.tempatLahir) return 'Tempat Lahir harus diisi'
        if (!formData.tanggalLahir) return 'Tanggal Lahir harus diisi'
        if (!formData.jenisKelamin) return 'Jenis Kelamin harus dipilih'
        if (!formData.agama) return 'Agama harus dipilih'
        if (!formData.alamat) return 'Alamat harus diisi'
        if (!formData.noTelp) return 'No. Telepon harus diisi'
      }
      
      // Step 1: Data Orang Tua
      if (currentStep.value === 1) {
        if (!formData.namaAyah) return 'Nama Ayah harus diisi'
        if (!formData.pekerjaanAyah) return 'Pekerjaan Ayah harus diisi'
        if (!formData.namaIbu) return 'Nama Ibu harus diisi'
        if (!formData.pekerjaanIbu) return 'Pekerjaan Ibu harus diisi'
        if (!formData.noTelpOrtu) return 'No. Telp Orang Tua harus diisi'
        if (!formData.penghasilan) return 'Penghasilan Orang Tua harus dipilih'
        if (!formData.alamatOrtu) return 'Alamat Orang Tua harus diisi'
      }
      
      // Step 2: Jurusan & Sekolah
      if (currentStep.value === 2) {
        if (!formData.jurusan) return 'Jurusan harus dipilih'
        if (!formData.asalSekolah) return 'Asal Sekolah harus diisi'
        if (!formData.tahunLulus) return 'Tahun Lulus harus diisi'
      }
      
      return null // No error
    }

    const nextStep = () => {
      const error = validateCurrentStep()
      if (error) {
        alert(error)
        return
      }

      if (currentStep.value < 3) {
        currentStep.value++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const prevStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
    }

    const generateRegistrationNumber = () => {
      const year = new Date().getFullYear()
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `PPDB${year}${random}`
    }

    const handleSubmit = async () => {
      if (!agreed.value) {
        alert('Anda harus menyetujui pernyataan terlebih dahulu')
        return
      }

      // Final validation pass
      for (let i = 0; i < 3; i++) {
        currentStep.value = i
        const error = validateCurrentStep()
        if (error) {
          alert(`Mohon lengkapi data di langkah ${i+1}: ${error}`)
          return
        }
      }
      currentStep.value = 3 // Back to confirmation

      submitting.value = true

      try {
        // Map form data to backend schema
        const payload = {
          nisn: formData.nisn,
          full_name: formData.namaLengkap,
          place_of_birth: formData.tempatLahir,
          date_of_birth: formData.tanggalLahir,
          gender: formData.jenisKelamin,
          religion: formData.agama,
          school_origin: formData.asalSekolah,
          email: formData.email,
          phone: formData.noTelp,
          address: formData.alamat,
          father_name: formData.namaAyah,
          father_job: formData.pekerjaanAyah,
          mother_name: formData.namaIbu,
          mother_job: formData.pekerjaanIbu,
          parent_phone: formData.noTelpOrtu,
          parent_income: formData.penghasilan,
          parent_address: formData.alamatOrtu,
          major_choice: formData.jurusan,
          graduation_year: parseInt(formData.tahunLulus),
          average_score: formData.nilaiRataRata ? formData.nilaiRataRata.toString() : null
        }

        const response = await ChatAPI.registerPPDB(payload)
        
        registrationNumber.value = response.nisn
        
        // Save to localStorage as backup/history
        const submissions = JSON.parse(localStorage.getItem('ppdb_submissions') || '[]')
        submissions.push({
          ...formData,
          registrationStatus: response.status,
          submittedAt: new Date().toISOString()
        })
        localStorage.setItem('ppdb_submissions', JSON.stringify(submissions))
        
        // Show success notification
        // alert(`🎉 PENDAFTARAN BERHASIL!\n\nNISN: ${response.nisn}\nNama: ${formData.namaLengkap}\n\n✅ Data tersimpan\n✅ Email konfirmasi dikirim ke: ${formData.email}\n\nSilakan cek inbox email Anda!`)
        if (window.$toast) {
            window.$toast(`🎉 PENDAFTARAN BERHASIL! Silakan cek email ${formData.email}`, 'success', 8000)
        }
        
        // Show success modal
        showSuccess.value = true
        
        // Auto reset form after showing modal
        setTimeout(() => {
          resetForm()
          showSuccess.value = false
        }, 5000)
        
      } catch (error) {
        console.error('PPDB Registration Error:', error)
        
        // Show clear error message
        const errorMsg = error.message || 'Pendaftaran gagal. Silakan coba lagi.'
        // alert(`❌ PENDAFTARAN GAGAL!\n\n${errorMsg}\n\nTips:\n- Pastikan NISN belum terdaftar\n- Cek semua field sudah diisi\n- Coba dengan NISN berbeda`)
        
        // Also show toast if available
        if (window.$toast) {
          window.$toast(`❌ Gagal: ${errorMsg}`, 'error', 8000)
        }
      } finally {
        submitting.value = false
      }
    }

    const resetForm = () => {
      Object.keys(formData).forEach(key => {
        formData[key] = ''
      })
      formData.tahunLulus = new Date().getFullYear()
      currentStep.value = 0
      agreed.value = false
      showSuccess.value = false
      registrationNumber.value = ''
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const goHome = () => {
      router.push('/')
    }

    return {
      currentStep,
      steps,
      formData,
      agreed,
      submitting,
      showSuccess,
      registrationNumber,
      nextStep,
      prevStep,
      formatDate,
      handleSubmit,
      resetForm,
      goHome
    }
  }
}
</script>

<style scoped>
.ppdb-form-page {
  min-height: 100vh;
  padding: 100px 1rem 3rem;
  max-width: 900px;
  margin: 0 auto;
}

.form-header {
  text-align: center;
  margin-bottom: 3rem;
}

.form-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Progress Steps */
.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3rem;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-color);
  z-index: 0;
}

.step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--surface);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.step-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-align: center;
}

.step.active .step-label {
  color: var(--primary-color);
  font-weight: 600;
}

/* Form */
.registration-form {
  background: var(--surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.form-step h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--surface);
  color: var(--text-primary);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
}

/* Confirmation */
.confirmation-box {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.confirm-section {
  background: var(--surface-2);
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid var(--primary-color);
}

.confirm-section h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.confirm-section p {
  margin: 0.5rem 0;
  color: var(--text-primary);
}

.agreement {
  background: #fef3c7;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #f59e0b;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  margin-top: 0.25rem;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Navigation */
.form-navigation {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(var(--primary-rgb), 0.3);
}

.btn-secondary {
  background: var(--surface-2);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--gray-light);
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #059669;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
}

.modal-content {
  background: var(--surface);
  padding: 3rem;
  border-radius: 20px;
  text-align: center;
  max-width: 500px;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.success-icon {
  font-size: 5rem;
  color: #10b981;
  margin-bottom: 1rem;
}

.registration-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  padding: 1rem;
  background: rgba(var(--primary-rgb), 0.1);
  border-radius: 12px;
  margin: 1rem 0;
  letter-spacing: 2px;
}

.info-text {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin: 1rem 0;
}

.modal-content .btn {
  margin-top: 1rem;
  width: 100%;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .progress-steps {
    flex-wrap: wrap;
    gap: 1rem;
  }

  .step {
    flex: 0 0 calc(50% - 0.5rem);
  }

  .registration-form {
    padding: 1.5rem;
  }

  .form-navigation {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
