<template>
  <div class="page-container">
    <!-- Header -->
    <div class="header-section fade-in-up">
      <h1>{{ $t('majors.title') }}</h1>
      <p>{{ $t('majors.subtitle') }}</p>
    </div>

    <div class="majors-grid">
      <div 
        v-for="(jurusan, index) in schoolData.majors" 
        :key="jurusan.id" 
        class="major-card"
        :style="{ '--accent': jurusan.accent }"
      >
        <div class="icon-wrapper">
          <i :class="jurusan.icon"></i>
        </div>
        <div class="card-content">
          <h2 class="major-code">{{ jurusan.kode }}</h2>
          <h3 class="major-name">{{ $t(`majors.${jurusan.kode.toLowerCase()}.name`) }}</h3>
          <p class="major-desc">{{ $t(`majors.${jurusan.kode.toLowerCase()}.desc`) }}</p>
        </div>
        <div class="card-footer">
          <button class="btn-detail" @click="openDetail(jurusan)">{{ $t('majors.detail') }}</button>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeDetail">
      <div class="modal-content" :style="{ '--accent': selectedMajor.accent }">
        <button class="btn-close" @click="closeDetail">
          <i class="fas fa-times"></i>
        </button>
        
        <div class="modal-header">
          <div class="modal-icon">
            <i :class="selectedMajor.icon"></i>
          </div>
          <div>
            <span class="modal-code">{{ selectedMajor.kode }}</span>
            <h2>{{ selectedMajor.nama }}</h2>
          </div>
        </div>

        <div class="modal-body">
          <div class="section">
            <h3><i class="fas fa-info-circle"></i> Tentang Jurusan</h3>
            <p>{{ selectedMajor.deskripsi }}</p>
          </div>

          <div class="section">
            <h3><i class="fas fa-book-open"></i> Yang Dipelajari</h3>
            <ul class="subject-list">
              <li v-for="(subject, idx) in selectedMajor.subjects" :key="idx">
                {{ subject }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'

export default {
  name: 'Jurusan',
  data() {
    return {
      schoolData,
      showModal: false,
      selectedMajor: null
    }
  },
  methods: {
    openDetail(jurusan) {
      this.selectedMajor = jurusan
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },
    closeDetail() {
      this.showModal = false
      this.selectedMajor = null
      document.body.style.overflow = 'auto'
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 80px 2rem 4rem;
  min-height: 100vh;
  background: var(--background);
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.header-section h1 {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.header-section p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.majors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.major-card {
  background: var(--surface);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: relative;
}

.major-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--shadow-hover);
  border-color: var(--accent);
}

.icon-wrapper {
  background: var(--accent);
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
}

.card-content {
  padding: 1.5rem;
  flex: 1;
  text-align: center;
}

.major-code {
  color: var(--accent);
  font-size: 2rem;
  margin-bottom: 0.5rem;
  opacity: 0.2;
  position: absolute;
  top: 10px;
  right: 20px;
  font-weight: 900;
}

.major-name {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-weight: 700;
}

.major-desc {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  padding: 1.5rem;
  text-align: center;
  border-top: 1px solid var(--border-color);
  background: var(--surface-2);
}

.btn-detail {
  background: transparent;
  color: var(--accent);
  border: 2px solid var(--accent);
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-detail:hover {
  background: var(--accent);
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
  padding: 1rem;
}

.modal-content {
  background: var(--surface);
  width: 100%;
  max-width: 600px;
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
  animation: slideUp 0.3s ease-out;
  max-height: 90vh;
  overflow-y: auto;
}

.btn-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0,0,0,0.1);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
}

.btn-close:hover {
  background: rgba(0,0,0,0.2);
  transform: rotate(90deg);
}

.modal-header {
  background: linear-gradient(135deg, var(--accent), var(--primary-dark));
  padding: 2rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.modal-icon {
  background: rgba(255,255,255,0.2);
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.modal-header h2 {
  color: white;
  margin: 0;
  font-size: 1.5rem;
}

.modal-code {
  font-size: 0.9rem;
  background: rgba(255,255,255,0.2);
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-weight: 700;
}

.modal-body {
  padding: 2rem;
}

.section {
  margin-bottom: 2rem;
}

.section h3 {
  color: var(--accent);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.subject-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.subject-list li {
  background: var(--surface-2);
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  border-left: 3px solid var(--accent);
  color: var(--text-primary);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
