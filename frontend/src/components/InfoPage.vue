<template>
  <div class="info-page">
    <!-- Header -->
    <header class="info-header">
      <button class="back-btn" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i>
        Kembali
      </button>
      <div class="info-header-center">
        <img class="info-logo" src="../assets/SMK_PERTIWI_KUNINGAN-removebg-preview.png" alt="SMK Pertiwi Kuningan" />
        <h1>{{ schoolData.name }}</h1>
      </div>
      <div class="spacer"></div>
    </header>

    <!-- Content -->
    <main class="info-content">
      <!-- Tabs -->
      <div class="tabs">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'info' }"
          @click="activeTab = 'info'"
        >
          <i class="fas fa-school"></i>
          Informasi Sekolah
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'jurusan' }"
          @click="activeTab = 'jurusan'"
        >
          <i class="fas fa-book"></i>
          Jurusan
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'about' }"
          @click="activeTab = 'about'"
        >
          <i class="fas fa-users"></i>
          Tentang Kami
        </button>
      </div>

      <!-- Info Tab -->
      <div v-if="activeTab === 'info'" class="tab-content">
        <div class="info-card">
          <h2>Profil Sekolah</h2>
          <div class="info-item"><strong>Nama Lengkap:</strong><p>{{ schoolData.name }}</p></div>
          <div class="info-item"><strong>Alamat:</strong><p>{{ schoolData.address }}</p></div>
          <div class="info-item"><strong>Kepala Sekolah:</strong><p>{{ schoolData.headmaster }}</p></div>
          <div class="info-item"><strong>Profil Singkat:</strong><p>{{ schoolData.history }}</p></div>
          <div class="chips">
            <span v-for="fact in schoolData.quickFacts" :key="fact" class="chip">{{ fact }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Keunggulan Kami</h2>
          <ul class="check-list">
            <li v-for="item in schoolData.advantages" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="info-grid">
          <div class="info-card">
            <h2>Visi</h2>
            <p>{{ schoolData.vision }}</p>
          </div>
          <div class="info-card">
            <h2>Misi</h2>
            <ul class="bullet-list">
              <li v-for="item in schoolData.mission" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>

        <div class="info-card">
          <h2>Tujuan Sekolah</h2>
          <ul class="bullet-list">
            <li v-for="item in schoolData.goals" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="info-grid">
          <div class="info-card">
            <h2>Jadwal Pelajaran</h2>
            <div class="schedule-list">
              <span v-for="slot in schoolData.schedule" :key="slot" class="chip ghost">{{ slot }}</span>
            </div>
          </div>
          <div class="info-card">
            <h2>Daftar Guru</h2>
            <div class="teacher-list">
              <span v-for="teacher in schoolData.teachers" :key="teacher" class="teacher-pill">
                <i :class="getTeacherIcon(teacher)" aria-hidden="true"></i>
                <span class="teacher-name">{{ teacher }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Jurusan Tab -->
      <div v-if="activeTab === 'jurusan'" class="tab-content">
        <div class="jurusan-header">
          <button
            v-for="jurusan in schoolData.majors"
            :key="jurusan.id"
            type="button"
            class="jurusan-chip"
            @click="scrollToJurusan(jurusan.kode)"
          >
            <i :class="jurusan.icon"></i>
            <span>{{ jurusan.kode }}</span>
          </button>
        </div>
        <div class="jurusan-grid">
          <div v-for="jurusan in schoolData.majors" :key="jurusan.id" :id="`jurusan-${jurusan.kode}`" :class="['jurusan-card', { highlight: highlight === jurusan.kode }]">
            <div class="jurusan-logo" :style="{ background: jurusan.accent }">
              <i :class="jurusan.icon"></i>
            </div>
            <h3>{{ jurusan.nama }}</h3>
            <p class="jurusan-kode">{{ jurusan.kode }}</p>
            <p class="jurusan-desc">{{ jurusan.deskripsi }}</p>
          </div>
        </div>
      </div>

      <!-- About Tab -->
      <div v-if="activeTab === 'about'" class="tab-content">
        <div class="about-grid">
      <div class="about-card">
        <h2>Tentang Website</h2>
        <p>PRISM (Pertiwi Responsive Intelligent Smart Model) dibuat sebagai asisten digital resmi SMK Pertiwi Kuningan agar informasi sekolah bisa diakses cepat, rapi, dan konsisten oleh siswa, orang tua, maupun calon peserta didik.</p>
        <p>Alasan dibuatnya web ini:</p>
        <ul class="about-list">
          <li>Memudahkan akses informasi jurusan, guru, dan jadwal tanpa harus bertanya manual.</li>
          <li>Menjadikan data sekolah satu pintu agar jawaban selalu konsisten (bersumber dari <code>schoolData.js</code>).</li>
          <li>Meningkatkan citra sekolah dengan tampilan modern dan fitur AI/voice yang relevan.</li>
          <li>Mengurangi beban administrasi untuk pertanyaan berulang.</li>
        </ul>
        <p>Teknologi yang digunakan:</p>
        <ul class="about-list">
          <li><strong>Frontend:</strong> Vue 3 + Vite, CSS kustom, Font Awesome icons, desain responsif.</li>
          <li><strong>Backend API:</strong> FastAPI (Python) + Uvicorn, CORS aktif, session chat in-memory.</li>
          <li><strong>AI Engine:</strong> Google Gemini via <code>google-generativeai</code> untuk jawaban natural.</li>
          <li><strong>Data & RAG:</strong> Data resmi dari <code>schoolData.js</code> lalu dibentuk menjadi RAG di <code>school_rag.json</code>.</li>
          <li><strong>Pencarian Web:</strong> Opsional via DuckDuckGo (dipakai jika diminta).</li>
          <li><strong>Voice:</strong> Web Speech API (Speech‑to‑Text & Text‑to‑Speech) langsung di browser.</li>
        </ul>
      </div>

          <div class="about-card">
            <h2>Tim Pengembang</h2>
            <ul class="team-list">
              <li v-for="member in teamMembers" :key="member">{{ member }}</li>
            </ul>
            <p class="thanks">Terima kasih kepada Ibu Ramadhirra Azzahra Putri, S.T (Pd. RPL) atas dukungan dan bimbingannya.</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'

export default {
  name: 'InfoPage',
  emits: ['back'],
  props: {
    defaultTab: {
      type: String,
      default: 'info'
    },
    highlight: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      activeTab: this.defaultTab || 'info',
      teamMembers: [
        'Fathurrachman Fauzi (Ketua Kelompok)',
        'Farhan Susanto Putra',
        'Fitriyani Rahmawati',
        'Muhammad Zaenul Falaah',
        'Lutfiyah Alyaa',
        'Zahra Aulia Utami'
      ],
      schoolData
    }
  },
  methods: {
    getTeacherIcon(teacher) {
      const lower = teacher.toLowerCase()
      const match = (pattern) => lower.includes(pattern)

      if (match('kepala sekolah')) return 'fas fa-user-tie'
      if (match('koordinasi bk') || match('bk')) return 'fas fa-comments'
      if (match('pd. rpl') || match('rpl')) return 'fas fa-code'
      if (match('pd. tkj') || match('tkj')) return 'fas fa-network-wired'
      if (match('pd. tkr') || match('tkr')) return 'fas fa-car'
      if (match('pd. tsm') || match('tsm')) return 'fas fa-motorcycle'
      if (match('pd. to') || match('to')) return 'fas fa-microchip'
      if (match('pd. lp') || match('lp')) return 'fas fa-university'
      if (match('pkk')) return 'fas fa-hands-helping'
      if (match('ipas')) return 'fas fa-flask'
      if (match('informatika')) return 'fas fa-laptop-code'
      if (match('matematika')) return 'fas fa-square-root-variable'
      if (match('pai')) return 'fas fa-mosque'
      if (match('olahraga')) return 'fas fa-dumbbell'
      if (match('sejarah')) return 'fas fa-landmark'
      if (match('seni budaya')) return 'fas fa-palette'
      if (match('b. inggris') || match('bahasa inggris')) return 'fas fa-language'
      if (match('b. indonesia') || match('bahasa indonesia')) return 'fas fa-book-open'
      if (match('b. sunda') || match('bahasa sunda')) return 'fas fa-book'

      return 'fas fa-chalkboard-teacher'
    },
    scrollToJurusan(code) {
      if (!code) return
      this.$nextTick(() => {
        const el = document.getElementById(`jurusan-${code}`)
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    }
  },

  mounted() {
      if (this.highlight) {
        this.activeTab = 'jurusan'
        this.$nextTick(() => {
          const el = document.getElementById(`jurusan-${this.highlight}`)
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        })
      }
    },

    watch: {
      defaultTab(newVal) {
        this.activeTab = newVal || 'info'
      },
      highlight(newVal) {
        if (newVal) {
          this.activeTab = 'jurusan'
          this.$nextTick(() => {
            const el = document.getElementById(`jurusan-${newVal}`)
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
          })
        }
      }
    }
}
</script>

<style scoped>
.info-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--background);
  color: var(--text-primary);
}

.info-header {
  background: var(--surface);
  border-bottom: none;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-light);
}

.info-header-center {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-content: center;
  flex: 1;
}

.info-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border: none;
}

.back-btn {
  background: transparent;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-btn:hover {
  color: var(--primary-dark);
  transform: translateX(-2px);
}

.info-header h1 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
}

.spacer {
  width: 40px;
}

.info-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: none;
}

.tab-btn {
  background: transparent;
  border: none;
  padding: 0.75rem 1rem;
  border-bottom: 3px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.tab-content {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-card {
  background: var(--surface);
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-light);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.info-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  color: var(--primary-color);
}

.info-item {
  margin-bottom: 1.25rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item strong {
  display: block;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.info-item p {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.6;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.chip {
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  background: var(--primary-light);
  color: var(--primary-dark);
  font-weight: 600;
  font-size: 0.85rem;
  border: 1px solid var(--border-color);
}

.chip.ghost {
  background: var(--surface-2);
  color: var(--text-primary);
}

.check-list,
.bullet-list {
  margin: 0;
  padding-left: 1.1rem;
  color: var(--text-primary);
  line-height: 1.6;
}

.check-list li {
  margin-bottom: 0.35rem;
  list-style: disc;
}

.bullet-list li {
  margin-bottom: 0.35rem;
}

.schedule-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.teacher-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.5rem;
  max-height: 280px;
  overflow-y: auto;
  padding-right: 4px;
}

.teacher-pill {
  display: block;
  padding: 0.55rem 0.7rem;
  border-radius: 8px;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.92rem;
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.teacher-pill i {
  width: 20px;
  text-align: center;
  color: var(--primary-color);
  font-size: 0.95rem;
}

.teacher-name {
  flex: 1;
}

.info-item ul {
  margin: 0;
  padding-left: 1.5rem;
  color: var(--text-primary);
}

.info-item li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.jurusan-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.jurusan-header {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 1.25rem;
}

.jurusan-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 0.75rem;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--surface-2);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: var(--transition);
}

.jurusan-chip i {
  color: var(--primary-color);
}

.jurusan-chip:hover {
  background: var(--primary-light);
  border-color: var(--primary-color);
  color: var(--primary-dark);
}

.jurusan-card {
  background: var(--surface);
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-light);
}

.jurusan-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
  border-color: var(--primary-color);
}

.jurusan-card.highlight {
  border-color: var(--primary-dark);
  box-shadow: var(--shadow-hover);
  transform: translateY(-6px);
}

.jurusan-logo {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  color: #FFFFFF;
  margin: 0 auto 1rem;
  box-shadow: var(--shadow-light);
}

.jurusan-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.jurusan-kode {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--primary-color);
}

.jurusan-desc {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.about-card {
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.about-card h2 {
  margin: 0 0 1rem;
  font-size: 1.15rem;
  color: var(--primary-color);
}

.about-card p {
  margin: 0 0 1rem;
  color: var(--text-primary);
  line-height: 1.6;
}

.about-list {
  list-style: disc;
  padding-left: 1.2rem;
  margin: 0;
  color: var(--text-primary);
  line-height: 1.6;
}

.about-list li {
  margin-bottom: 0.5rem;
}

.team-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem;
  display: grid;
  gap: 0.5rem;
}

.team-list li {
  padding: 0.6rem 0.75rem;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-weight: 600;
}

.thanks {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .jurusan-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }

  .info-header {
    padding: 1rem;
  }

  .info-content {
    padding: 1rem;
  }

  .info-card {
    padding: 1.25rem;
  }

  .about-card {
    padding: 1.25rem;
  }

  .teacher-list {
    max-height: none;
  }
}

@media (max-width: 480px) {
  .tabs {
    gap: 0.6rem;
  }

  .tab-btn {
    padding: 0.65rem 0.8rem;
    font-size: 0.9rem;
  }

  .info-content {
    padding: 0.9rem;
  }
}
</style>
