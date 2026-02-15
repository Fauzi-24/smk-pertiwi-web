<template>
  <div class="admin-login-container">
    <div class="login-card">
      <div class="logo-section">
        <i class="fas fa-user-shield"></i>
        <h2>Admin Portal</h2>
        <p>SMK Pertiwi Kuningan</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="adminKey">Admin Key</label>
          <div class="input-wrapper">
            <i class="fas fa-key"></i>
            <input 
              type="password" 
              id="adminKey" 
              v-model="adminKey" 
              placeholder="Masukkan Kunci Admin"
              required
            >
          </div>
        </div>

        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>

        <button type="submit" :disabled="loading" class="login-btn">
          <span v-if="loading"><i class="fas fa-spinner fa-spin"></i> Memproses...</span>
          <span v-else>Masuk <i class="fas fa-arrow-right"></i></span>
        </button>
      </form>

      <div class="back-link">
        <router-link to="/"><i class="fas fa-home"></i> Kembali ke Beranda</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ChatAPI } from '../services/api'

export default {
  name: 'AdminLogin',
  data() {
    return {
      adminKey: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await ChatAPI.adminLogin(this.adminKey)
        if (response.success) {
          localStorage.setItem('admin_token', response.token) // In real app use httpOnly cookie
          
          if (window.$toast) {
            window.$toast('Login Berhasil!', 'success')
          }
          
          this.$router.push('/admin/dashboard')
        }
      } catch (err) {
        this.error = 'Kunci Admin Salah atau Terjadi Kesalahan.'
        if (window.$toast) {
          window.$toast('Login Gagal', 'error')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.admin-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background);
  padding: 1rem;
}

.login-card {
  background: var(--surface);
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--border-color);
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-section i {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.logo-section h2 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.logo-section p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.input-wrapper i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--surface-2);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.login-btn {
  width: 100%;
  padding: 0.85rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  background: rgba(220, 38, 38, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.back-link {
  text-align: center;
  margin-top: 1.5rem;
}

.back-link a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

.back-link a:hover {
  color: var(--primary-color);
}
</style>
