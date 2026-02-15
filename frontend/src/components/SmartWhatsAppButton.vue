<template>
  <a 
    :href="whatsappLink" 
    target="_blank"
    class="whatsapp-float"
    :title="whatsappTitle"
    aria-label="Chat WhatsApp"
  >
    <i class="fab fa-whatsapp"></i>
  </a>
</template>

<script>
export default {
  name: 'SmartWhatsAppButton',
  computed: {
    currentPage() {
      return this.$route.name || ''
    },
    whatsappNumber() {
      return '6281234567890' // Replace with real number
    },
    whatsappMessage() {
      const messages = {
        '/ppdb': 'Halo SMK Pertiwi Kuningan! Saya tertarik untuk mendaftar PPDB. Mohon informasinya.',
        '/jurusan': 'Halo, saya ingin mengetahui lebih detail tentang jurusan yang tersedia di SMK Pertiwi Kuningan.',
        '/berita': 'Halo, saya ingin bertanya tentang informasi terbaru dari SMK Pertiwi Kuningan.',
        '/alumni': 'Halo, saya alumni SMK Pertiwi Kuningan dan ingin update data/informasi.',
        '/kontak': 'Halo SMK Pertiwi Kuningan, saya ingin bertanya...',
        '/guru': 'Halo, saya ingin mengetahui informasi tentang tenaga pengajar di SMK Pertiwi Kuningan.',
        default: 'Halo SMK Pertiwi Kuningan! Saya ingin bertanya tentang sekolah.'
      }
      
      const currentPath = this.$route.path
      return messages[currentPath] || messages.default
    },
    whatsappLink() {
      const encodedMessage = encodeURIComponent(this.whatsappMessage)
      return `https://wa.me/${this.whatsappNumber}?text=${encodedMessage}`
    },
    whatsappTitle() {
      return 'Chat dengan admin SMK Pertiwi via WhatsApp'
    }
  }
}
</script>

<style scoped>
.whatsapp-float {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 998;
  text-decoration: none;
}

.whatsapp-float:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 10px 32px rgba(37, 211, 102, 0.6);
}

.whatsapp-float i {
  font-size: 2rem;
}

/* Animation pulse */
@keyframes pulse {
  0% {
    box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4);
  }
  50% {
    box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4), 0 0 0 15px rgba(37, 211, 102, 0.1);
  }
  100% {
    box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4);
  }
}

.whatsapp-float {
  animation: pulse 2s infinite;
}

/* Mobile */
@media (max-width: 768px) {
  .whatsapp-float {
    bottom: 20px;
    right: 20px;
    width: 55px;
    height: 55px;
    font-size: 1.75rem;
  }
}
</style>
