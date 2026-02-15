<template>
  <div class="not-found-page">
    <div class="error-container">
      <div class="error-code">404</div>
      <h1>Halaman Tidak Ditemukan</h1>
      <p>Maaf, halaman yang Anda cari tidak ada atau telah dipindahkan.</p>
      
      <div class="suggestions">
        <h3>Mungkin Anda mencari:</h3>
        <div class="suggestion-links">
          <router-link to="/" class="suggestion-btn">
            <i class="fas fa-home"></i>
            Beranda
          </router-link>
          <router-link to="/ppdb" class="suggestion-btn">
            <i class="fas fa-user-graduate"></i>
            PPDB
          </router-link>
          <router-link to="/galeri" class="suggestion-btn">
            <i class="fas fa-images"></i>
            Galeri
          </router-link>
          <router-link to="/chat" class="suggestion-btn">
            <i class="fas fa-robot"></i>
            AI Chat
          </router-link>
        </div>
      </div>

      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Cari halaman..."
          @keyup.enter="searchPage"
        >
        <button @click="searchPage">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'NotFound',
  setup() {
    const searchQuery = ref('')
    const router = useRouter()

    const searchPage = () => {
      if (searchQuery.value.trim()) {
        // Simple search logic - redirect to chat
        router.push(`/chat?q=${encodeURIComponent(searchQuery.value)}`)
      }
    }

    return {
      searchQuery,
      searchPage
    }
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--background) 0%, var(--surface-2) 100%);
  padding: 2rem;
}

.error-container {
  text-align: center;
  max-width: 600px;
}

.error-code {
  font-size: 10rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

h1 {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
}

.suggestions {
  margin-bottom: 3rem;
}

.suggestions h3 {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.suggestion-links {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.suggestion-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.suggestion-btn:hover {
  border-color: var(--primary-color);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.suggestion-btn i {
  font-size: 2rem;
  color: var(--primary-color);
}

.search-box {
  display: flex;
  gap: 0.5rem;
  max-width: 400px;
  margin: 0 auto;
}

.search-box input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--surface);
  color: var(--text-primary);
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.search-box button {
  padding: 0.75rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.search-box button:hover {
  background: var(--primary-dark);
}

@media (max-width: 768px) {
  .error-code {
    font-size: 6rem;
  }
  
  .suggestion-links {
    grid-template-columns: 1fr;
  }
}
</style>
