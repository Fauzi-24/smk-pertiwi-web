<template>
  <div class="page-container">
    <div class="header-section">
      <h1>{{ $t('teachers.title') }}</h1>
      <p>{{ $t('teachers.subtitle') }}</p>
    </div>

    <!-- Featured Headmaster -->
    <div class="featured-headmaster fade-in">
      <div class="headmaster-card">
        <div class="headmaster-avatar">
          <i class="fas fa-user-tie"></i>
        </div>
        <div class="headmaster-info">
          <span class="badge">{{ $t('teachers.headmaster_role') }}</span>
          <h2>{{ schoolData.headmaster }}</h2>
          <p>{{ $t('teachers.headmaster_desc') }}</p>
        </div>
      </div>
    </div>

    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        :placeholder="$t('teachers.search_placeholder')"
        class="search-input"
      >
      <i class="fas fa-search search-icon"></i>
    </div>

    <div class="teachers-grid">
      <div 
        v-for="(teacher, index) in filteredTeachers" 
        :key="index" 
        class="teacher-card fade-in"
        :style="{ animationDelay: `${index * 0.03}s` }"
      >
        <div class="avatar">
          <i class="fas fa-user-tie"></i>
        </div>
        <div class="info">
          <h3>{{ parseTeacher(teacher).name }}</h3>
          <span class="role">{{ parseTeacher(teacher).role }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'

export default {
  name: 'Guru',
  data() {
    return {
      schoolData,
      searchQuery: ''
    }
  },
  computed: {
    filteredTeachers() {
      // Filter out Headmaster from the list as it's featured at the top
      const headmasterName = this.schoolData.headmaster
      const otherTeachers = this.schoolData.teachers.filter(t => !t.includes(headmasterName))
      
      if (!this.searchQuery) return otherTeachers
      const query = this.searchQuery.toLowerCase()
      return otherTeachers.filter(t => t.toLowerCase().includes(query))
    }
  },
  methods: {
    parseTeacher(teacherString) {
      const match = teacherString.match(/(.*)\s\((.*)\)/)
      if (match) {
        return { name: match[1], role: match[2] }
      }
      return { name: teacherString, role: this.$t('teachers.role_teacher') }
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
  font-size: 2.8rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-weight: 800;
}

/* Featured Headmaster */
.featured-headmaster {
  max-width: 900px;
  margin: 0 auto 4rem;
}

.headmaster-card {
  background: var(--primary-gradient);
  padding: 3rem;
  border-radius: 24px;
  display: flex;
  align-items: center;
  gap: 3rem;
  color: white;
  box-shadow: 0 20px 40px rgba(37, 99, 235, 0.25);
  position: relative;
  overflow: hidden;
}

.headmaster-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.headmaster-avatar {
  background: rgba(255, 255, 255, 0.2);
  width: 120px;
  height: 120px;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
  flex-shrink: 0;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.headmaster-info .badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  display: inline-block;
  backdrop-filter: blur(5px);
}

.headmaster-info h2 {
  font-size: 2.2rem;
  margin-bottom: 1rem;
  color: white;
  line-height: 1.2;
}

.headmaster-info p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  margin: 0;
  max-width: 500px;
}

.search-bar {
  max-width: 700px;
  margin: 0 auto 3rem;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 1.2rem 1.5rem;
  padding-left: 3.5rem;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  background: var(--surface);
  color: var(--text-primary);
  font-size: 1.1rem;
  box-shadow: var(--shadow-light);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
  transform: translateY(-2px);
}

.search-icon {
  position: absolute;
  left: 1.4rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary-color);
  font-size: 1.2rem;
}

.teachers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.teacher-card {
  background: var(--surface);
  padding: 1.8rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-light);
}

.teacher-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary-color);
  box-shadow: var(--shadow);
}

.avatar {
  background: var(--surface-2);
  width: 60px;
  height: 60px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  font-size: 1.5rem;
  transition: all 0.3s;
}

.teacher-card:hover .avatar {
  background: var(--primary-color);
  color: white;
  transform: scale(1.1);
}

.info h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-primary);
  font-weight: 700;
}

.role {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.3rem;
  display: block;
}

.fade-in {
  animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .headmaster-card {
    flex-direction: column;
    text-align: center;
    padding: 2rem;
    gap: 1.5rem;
  }
  
  .headmaster-info p {
    margin: 0 auto;
  }

  .header-section h1 {
    font-size: 2rem;
  }
}
</style>
