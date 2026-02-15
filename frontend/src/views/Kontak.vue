<template>
  <div class="page-container">
    <div class="header-section">
      <h1>{{ $t('contact.title') }}</h1>
      <p>{{ $t('contact.subtitle') }}</p>
    </div>

    <div class="contact-grid">
      <div class="contact-info">
        <div class="info-card">
          <i class="fas fa-map-marker-alt"></i>
          <h3>{{ $t('contact.address') }}</h3>
          <p>{{ schoolData.address }}</p>
        </div>
        <div class="info-card">
          <i class="fas fa-phone"></i>
          <h3>{{ $t('contact.phone') }}</h3>
          <p>(0232) 123456</p>
        </div>
        <div class="info-card">
          <i class="fas fa-envelope"></i>
          <h3>{{ $t('contact.email') }}</h3>
          <p>info@smkpertiwi.sch.id</p>
        </div>
      </div>

      <div class="contact-form-card">
        <h2>{{ $t('contact.form.title') }}</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>{{ $t('contact.form.name') }}</label>
            <input type="text" v-model="form.name" required :placeholder="$t('contact.form.placeholder_name')">
          </div>
          <div class="form-group">
            <label>{{ $t('contact.form.email_label') }}</label>
            <input type="email" v-model="form.email" required :placeholder="$t('contact.form.placeholder_email')">
          </div>
          <div class="form-group">
            <label>{{ $t('contact.form.message') }}</label>
            <textarea v-model="form.message" rows="5" required :placeholder="$t('contact.form.placeholder_message')"></textarea>
          </div>
          <button type="submit" class="btn-submit">{{ $t('contact.form.submit') }}</button>
        </form>
      </div>
    </div>

    <!-- WhatsApp Floating Button -->
    <a 
      href="https://wa.me/6281234567890?text=Halo%20SMK%20Pertiwi%20Kuningan,%20saya%20ingin%20bertanya%20tentang..." 
      target="_blank"
      class="whatsapp-float"
      title="Chat WhatsApp"
    >
      <i class="fab fa-whatsapp"></i>
    </a>
  </div>
</template>

<script>
import schoolData from '../data/schoolData'

export default {
  name: 'Kontak',
  data() {
    return {
      schoolData,
      form: {
        name: '',
        email: '',
        message: ''
      }
    }
  },
  methods: {
    submitForm() {
      // TODO: Implement contact form submission logic
      alert(`Terima kasih ${this.form.name}, pesan Anda telah kami terima!`)
      this.form = { name: '', email: '', message: '' }
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

.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .contact-grid {
    grid-template-columns: 1fr 1.5fr;
  }
}

.info-card {
  background: var(--surface);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  text-align: center;
  border: 1px solid var(--border-color);
}

.info-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.contact-form-card {
  background: var(--surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  background: var(--background);
  color: var(--text-primary);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-submit {
  width: 100%;
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-submit:hover {
  background: var(--primary-dark);
}

.whatsapp-float {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: #25D366;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
  z-index: 1000;
  transition: all 0.3s ease;
  text-decoration: none;
}

.whatsapp-float:hover {
  transform: scale(1.1) translateY(-5px);
  box-shadow: 0 8px 30px rgba(37, 211, 102, 0.6);
}

.whatsapp-float i {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
</style>
