<template>
  <div class="share-buttons">
    <button @click="share('facebook')" class="share-btn facebook" title="Share ke Facebook">
      <i class="fab fa-facebook-f"></i>
    </button>
    <button @click="share('twitter')" class="share-btn twitter" title="Share ke Twitter">
      <i class="fab fa-twitter"></i>
    </button>
    <button @click="share('whatsapp')" class="share-btn whatsapp" title="Share ke WhatsApp">
      <i class="fab fa-whatsapp"></i>
    </button>
    <button @click="copyLink" class="share-btn copy" :title="copied ? 'Tersalin!' : 'Salin Link'">
      <i :class="copied ? 'fas fa-check' : 'fas fa-link'"></i>
    </button>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ShareButtons',
  props: {
    url: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: 'SMK Pertiwi Kuningan'
    },
    description: {
      type: String,
      default: 'Website resmi SMK Pertiwi Kuningan dengan 7 jurusan unggulan'
    }
  },
  setup(props) {
    const copied = ref(false)
    
    const shareUrl = props.url || window.location.href
    
    const share = (platform) => {
      const text = encodeURIComponent(`${props.title} - ${props.description}`)
      const url = encodeURIComponent(shareUrl)
      
      let shareLink = ''
      
      switch (platform) {
        case 'facebook':
          shareLink = `https://www.facebook.com/sharer/sharer.php?u=${url}`
          break
        case 'twitter':
          shareLink = `https://twitter.com/intent/tweet?text=${text}&url=${url}`
          break
        case 'whatsapp':
          shareLink = `https://wa.me/?text=${text}%20${url}`
          break
      }
      
      if (shareLink) {
        window.open(shareLink, '_blank', 'width=600,height=400')
      }
    }
    
    const copyLink = async () => {
      try {
        await navigator.clipboard.writeText(shareUrl)
        copied.value = true
        setTimeout(() => {
          copied.value = false
        }, 2000)
      } catch (err) {
        // Fallback untuk browser yang tidak support clipboard API
        const textarea = document.createElement('textarea')
        textarea.value = shareUrl
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand('copy')
        document.body.removeChild(textarea)
        copied.value = true
        setTimeout(() => {
          copied.value = false
        }, 2000)
      }
    }
    
    return {
      copied,
      share,
      copyLink
    }
  }
}
</script>

<style scoped>
.share-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.share-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: white;
  transition: all 0.3s ease;
}

.share-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.share-btn.facebook {
  background: #1877F2;
}

.share-btn.twitter {
  background: #1DA1F2;
}

.share-btn.whatsapp {
  background: #25D366;
}

.share-btn.copy {
  background: var(--text-secondary);
}

.share-btn.copy:hover {
  background: var(--primary-color);
}
</style>
