<template>
  <div class="page-container">
    <div class="header-section">
      <h1>Pertanyaan Umum (FAQ)</h1>
      <p>Temukan jawaban atas pertanyaan yang sering diajukan</p>
    </div>

    <!-- Category Filter -->
    <div class="category-filter">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="['cat-btn', { active: selectedCategory === cat }]"
        @click="selectedCategory = cat"
      >
        {{ cat }}
      </button>
    </div>

    <!-- FAQ List -->
    <div class="faq-list">
      <div
        v-for="faq in filteredFAQs"
        :key="faq.id"
        class="faq-item"
        @click="toggleFAQ(faq.id)"
      >
        <div class="faq-question">
          <span class="category-badge">{{ faq.category }}</span>
          <h3>{{ faq.question }}</h3>
          <i :class="['fas', openFAQs.includes(faq.id) ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
        </div>
        <transition name="slide">
          <div v-if="openFAQs.includes(faq.id)" class="faq-answer">
            <p>{{ faq.answer }}</p>
          </div>
        </transition>
      </div>
    </div>

    <!-- Contact CTA -->
    <div class="faq-cta">
      <h3>Belum menemukan jawaban yang Anda cari?</h3>
      <p>Hubungi kami atau gunakan AI Chatbot untuk pertanyaan lebih spesifik</p>
      <div class="cta-buttons">
        <router-link to="/kontak" class="btn-contact">
          <i class="fas fa-envelope"></i>
          Hubungi Kami
        </router-link>
        <router-link to="/chat" class="btn-chat">
          <i class="fas fa-robot"></i>
          Tanya AI
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { faqData, faqCategories } from '../data/faqData'

export default {
  name: 'FAQ',
  setup() {
    const selectedCategory = ref('Semua')
    const openFAQs = ref([])
    const categories = faqCategories

    const filteredFAQs = computed(() => {
      if (selectedCategory.value === 'Semua') {
        return faqData
      }
      return faqData.filter(faq => faq.category === selectedCategory.value)
    })

    const toggleFAQ = (id) => {
      const index = openFAQs.value.indexOf(id)
      if (index > -1) {
        openFAQs.value.splice(index, 1)
      } else {
        openFAQs.value.push(id)
      }
    }

    return {
      categories,
      selectedCategory,
      filteredFAQs,
      openFAQs,
      toggleFAQ
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 80px 2rem 4rem;
  min-height: 100vh;
  background: var(--background);
  max-width: 900px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.category-filter {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 3rem;
}

.cat-btn {
  padding: 0.75rem 1.5rem;
  background: var(--surface);
  border: 2px solid var(--border-color);
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.cat-btn:hover,
.cat-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.faq-item:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.faq-question {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.category-badge {
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.faq-question h3 {
  flex: 1;
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.faq-question i {
  color: var(--primary-color);
  transition: transform 0.3s;
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.faq-answer p {
  margin: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.faq-cta {
  margin-top: 4rem;
  text-align: center;
  padding: 3rem;
  background: var(--surface);
  border-radius: 16px;
  border: 2px dashed var(--border-color);
}

.faq-cta h3 {
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.faq-cta p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-contact,
.btn-chat {
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-contact {
  background: var(--primary-color);
  color: white;
}

.btn-contact:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-chat {
  background: var(--surface-2);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.btn-chat:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}
</style>
