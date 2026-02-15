<template>
  <div class="progress-container" :class="{ 'active': isLoading }">
    <div class="progress-bar" :style="{ width: progress + '%' }"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'ProgressBar',
  setup() {
    const isLoading = ref(false)
    const progress = ref(0)
    let interval = null

    const start = () => {
      isLoading.value = true
      progress.value = 0
      clearInterval(interval)
      interval = setInterval(() => {
        if (progress.value < 90) {
          progress.value += Math.random() * 10
        }
      }, 200)
    }

    const finish = () => {
      progress.value = 100
      clearInterval(interval)
      setTimeout(() => {
        isLoading.value = false
        setTimeout(() => {
          progress.value = 0
        }, 300)
      }, 300)
    }

    const handleStart = () => start()
    const handleStop = () => finish()

    onMounted(() => {
      window.addEventListener('start-loading', handleStart)
      window.addEventListener('stop-loading', handleStop)
    })

    onUnmounted(() => {
      window.removeEventListener('start-loading', handleStart)
      window.removeEventListener('stop-loading', handleStop)
    })

    return { isLoading, progress }
  }
}
</script>

<style scoped>
.progress-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 10000;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}

.progress-container.active {
  opacity: 1;
}

.progress-bar {
  height: 100%;
  background: #2563eb; /* Primary blue */
  background: linear-gradient(90deg, #2563eb, #10b981); /* Blue to Green */
  width: 0;
  transition: width 0.2s ease;
  box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
}
</style>
