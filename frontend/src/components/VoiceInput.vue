<template>
  <div class="voice-input-container">
    <button 
      @click="toggleRecording" 
      :class="['voice-btn', { recording: isRecording }]"
      :title="isRecording ? 'Stop Recording' : 'Voice Input'"
    >
      <i :class="isRecording ? 'fas fa-stop' : 'fas fa-microphone'"></i>
    </button>
    <div v-if="isRecording" class="recording-indicator">
      <span class="pulse"></span>
      <span class="text">Recording...</span>
    </div>
    <div v-if="transcript" class="transcript">
      {{ transcript }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'VoiceInput',
  emits: ['transcript'],
  setup(props, { emit }) {
    const isRecording = ref(false)
    const transcript = ref('')
    let recognition = null

    // Check browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

    if (SpeechRecognition) {
      recognition = new SpeechRecognition()
      recognition.lang = 'id-ID' // Indonesian
      recognition.continuous = false
      recognition.interimResults = false

      recognition.onresult = (event) => {
        const text = event.results[0][0].transcript
        transcript.value = text
        emit('transcript', text)
        isRecording.value = false
      }

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        isRecording.value = false
      }

      recognition.onend = () => {
        isRecording.value = false
      }
    }

    const toggleRecording = () => {
      if (!recognition) {
        alert('Browser Anda tidak support voice input. Gunakan Chrome/Edge.')
        return
      }

      if (isRecording.value) {
        recognition.stop()
        isRecording.value = false
      } else {
        transcript.value = ''
        recognition.start()
        isRecording.value = true
      }
    }

    return {
      isRecording,
      transcript,
      toggleRecording
    }
  }
}
</script>

<style scoped>
.voice-input-container {
  display: inline-flex;
  align-items: center;
  gap: 1rem;
}

.voice-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--primary-color);
  background: var(--surface);
  color: var(--primary-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.voice-btn:hover {
  background: var(--primary-color);
  color: white;
  transform: scale(1.05);
}

.voice-btn.recording {
  background: #ef4444;
  border-color: #ef4444;
  color: white;
  animation: recordingPulse 1.5s infinite;
}

@keyframes recordingPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}

.recording-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ef4444;
  font-weight: 600;
}

.pulse {
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

.transcript {
  padding: 0.75rem 1rem;
  background: var(--surface-2);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--text-primary);
  max-width: 300px;
}
</style>
