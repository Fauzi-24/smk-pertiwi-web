<template>
  <div class="chat-app">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="logo-container">
          <div class="school-info">
            <h1>Prism</h1>
            <p class="subtitle">SMK Pertiwi Kuningan</p>
            <p v-if="conversationTitle" class="conversation-title">{{ conversationTitle }}</p>
          </div>
        </div>
        <div class="header-actions">
          <button class="icon-btn" @click="$emit('toggle-history')" title="Riwayat Obrolan">
            <i class="fas fa-comments"></i>
          </button>
          <button class="icon-btn" @click="$emit('export-chat')" title="Unduh Obrolan">
            <i class="fas fa-download"></i>
          </button>
          <button class="icon-btn info-btn" @click="$emit('go-to-info')" title="Informasi Sekolah">
            <i class="fas fa-circle-info"></i>
          </button>
          <button class="icon-btn" @click="toggleTheme" :title="isDark ? 'Mode Terang' : 'Mode Gelap'">
            <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
          <button class="icon-btn" @click="$emit('clear-chat')" title="Hapus Percakapan">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </header>

    <div
      v-if="backendStatus && backendStatus !== 'online'"
      :class="['connection-banner', backendStatus]"
    >
      <div class="banner-info">
        <i class="fas fa-triangle-exclamation"></i>
        <span>
          {{ backendMessage || (backendStatus === 'checking' ? 'Menghubungkan ke server...' : 'Server belum tersambung.') }}
        </span>
      </div>
      <button
        v-if="backendStatus === 'offline'"
        class="banner-btn"
        type="button"
        @click="$emit('retry-connection')"
      >
        Coba lagi
      </button>
    </div>

    <!-- Main Chat Area -->
    <main class="chat-main" ref="chatMain" @scroll="handleScroll">
      <div class="chat-search">
        <i class="fas fa-magnifying-glass"></i>
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Cari di chat ini..."
          @input="resetSearch"
        />
        <span v-if="searchIndices.length" class="search-count">
          {{ searchPointer + 1 }}/{{ searchIndices.length }}
        </span>
        <button
          class="search-btn"
          type="button"
          :disabled="!searchIndices.length"
          @click="prevSearch"
        >
          <i class="fas fa-chevron-up"></i>
        </button>
        <button
          class="search-btn"
          type="button"
          :disabled="!searchIndices.length"
          @click="nextSearch"
        >
          <i class="fas fa-chevron-down"></i>
        </button>
      </div>

      <div v-if="attachmentsLoading || (attachments && attachments.length)" class="attachments-panel">
        <div class="attachments-header">
          <i class="fas fa-paperclip"></i>
          Lampiran Aktif
          <span class="attachments-count">{{ attachments.length }}</span>
        </div>
        <div v-if="attachmentsLoading" class="attachment-loading">Memuat lampiran...</div>
        <div v-else class="attachments-list">
          <div v-for="item in attachments" :key="item.id" class="attachment-item">
            <div>
              <div class="attachment-name">{{ item.filename }}</div>
              <div class="attachment-summary">Lampiran siap digunakan.</div>
            </div>
            <button class="attachment-remove" type="button" @click="$emit('remove-attachment', item.id)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
      <!-- Welcome Message -->
      <div v-if="messages.length === 0" class="welcome-section">
        <div class="welcome-card">
          <div class="welcome-icon">
            <i class="fas fa-robot"></i>
          </div>
          <h2>Halo! Saya PRISM</h2>
          <p>Pertiwi Responsive Intelligent Smart Model untuk SMK Pertiwi Kuningan</p>
          <div class="features">
            <div class="feature" role="button" tabindex="0" @click="$emit('go-to-info', { tab: 'info' })">
              <i class="fas fa-school"></i>
              <span>Informasi Sekolah</span>
            </div>
            <div class="feature" role="button" tabindex="0" @click="$emit('go-to-info', { tab: 'jurusan' })">
              <i class="fas fa-book"></i>
              <span>Jurusan & Kurikulum</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="pinnedMessages.length" class="pinned-section">
        <div class="pinned-header">
          <i class="fas fa-thumbtack"></i>
          Disematkan
        </div>
        <div class="pinned-list">
          <div v-for="item in pinnedMessages" :key="item.index" class="pinned-item">
            <div class="pinned-text">{{ item.text }}</div>
            <div class="pinned-actions">
              <button class="pinned-btn" type="button" @click="scrollToMessage(item.index)">
                Lihat
              </button>
              <button class="pinned-btn ghost" type="button" @click="togglePin(item.index)">
                Lepas
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Prompts -->
      <div v-if="showQuickPrompts" class="quick-prompts">
        <button class="prompt-refresh" type="button" @click="refreshQuickPrompts">
          <i class="fas fa-rotate"></i>
          Acak Prompt
        </button>
        <button
          v-for="prompt in quickPrompts"
          :key="prompt"
          class="prompt-chip"
          type="button"
          @click="sendQuickPrompt(prompt)"
        >
          {{ prompt }}
        </button>
      </div>

      <!-- Chat Messages -->
      <div class="messages-container">
        <div
          v-for="(message, index) in parsedMessages"
          :key="index"
          :data-message-index="index"
          :class="['message-wrapper', message.sender, { pinned: message.pinned, matched: searchMatchSet.has(index), active: activeMatchIndex === index }]"
        >
          <div class="message-sender">
            <i v-if="message.sender === 'user'" class="fas fa-user"></i>
            <i v-else class="fas fa-robot"></i>
            <span>{{ message.sender === 'user' ? 'Anda' : 'Prism' }}</span>
          </div>
          <div class="message-bubble">
            <div v-if="message.attachment" class="message-attachment">
              <div class="attachment-icon">
                <i class="fas fa-paperclip"></i>
              </div>
              <div class="attachment-details">
                <div class="attachment-title">{{ message.attachment.filename }}</div>
                <div class="attachment-meta">{{ formatAttachmentMeta(message.attachment) }}</div>
              </div>
            </div>
            <p>{{ message.body }}</p>
            <div v-if="message.sender === 'ai' && showSource(message.source)" class="message-source">
              {{ formatSource(message.source) }}
            </div>
            <div v-if="message.sender === 'ai' && message.sources.length" class="message-sources">
              <div class="sources-title">Sumber Internet</div>
              <div class="sources-list">
                <template v-for="(source, sIndex) in message.sources" :key="`${index}-${sIndex}`">
                  <a
                    v-if="source.url"
                    class="source-item"
                    :href="source.url"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {{ source.label }}
                  </a>
                  <span v-else class="source-item">{{ source.label }}</span>
                </template>
              </div>
            </div>
            <div class="message-actions">
              <button
                class="message-action-btn copy-btn"
                type="button"
                :class="{ copied: copiedIndex === index }"
                :title="copiedIndex === index ? 'Tersalin' : 'Salin pesan'"
                @click="copyMessage(message.text, index)"
              >
                <i class="fas fa-copy"></i>
              </button>
              <button
                v-if="message.sender === 'ai' && index === lastAiIndex && !isLoading"
                class="message-action-btn regen-btn"
                type="button"
                title="Regenerate jawaban"
                @click="$emit('regenerate-response')"
              >
                <i class="fas fa-rotate-right"></i>
              </button>
              <button
                v-if="message.sender === 'user' && index === lastUserIndex && !isLoading"
                class="message-action-btn edit-btn"
                type="button"
                title="Edit pesan terakhir"
                @click="$emit('edit-message', { index })"
              >
                <i class="fas fa-pen-to-square"></i>
              </button>
              <button
                v-if="message.sender === 'ai'"
                class="message-action-btn pin-btn"
                type="button"
                :class="{ active: message.pinned }"
                :title="message.pinned ? 'Lepas sematan' : 'Sematkan jawaban'"
                @click="togglePin(index)"
              >
                <i class="fas fa-thumbtack"></i>
              </button>
              <button
                v-if="message.sender === 'ai'"
                class="message-action-btn feedback-btn"
                type="button"
                title="Perbaiki jawaban"
                @click="$emit('feedback', { index })"
              >
                <i class="fas fa-flag"></i>
              </button>
              <button
                v-if="message.sender === 'ai' && speechSupported.synthesis"
                class="message-action-btn speak-btn"
                type="button"
                :class="{ active: speakingIndex === index }"
                :title="speakingIndex === index ? 'Hentikan suara' : 'Dengarkan jawaban'"
                @click="toggleSpeak(message.text, index)"
              >
                <i :class="speakingIndex === index ? 'fas fa-stop' : 'fas fa-volume-up'"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isLoading" class="typing-indicator">
          <div class="typing-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
          <span>Sedang mengetik...</span>
        </div>
      </div>

      <button
        v-if="showScrollToBottom"
        class="scroll-to-bottom"
        type="button"
        title="Scroll ke bawah"
        @click="scrollToBottom"
      >
        <i class="fas fa-arrow-down"></i>
      </button>
    </main>

    <!-- Input Area -->
    <footer class="chat-footer">
      <div v-if="uploadState && uploadState.status !== 'idle'" :class="['upload-state', uploadState.status]">
        <div class="upload-info">
          <div v-if="uploadState.isImage && uploadState.previewUrl" class="upload-thumb">
            <img :src="uploadState.previewUrl" alt="Lampiran" />
          </div>
          <i v-else class="fas fa-paperclip"></i>
          <div>
            <div class="upload-name">{{ uploadState.fileName || 'Lampiran' }}</div>
            <div class="upload-message">{{ uploadState.message }}</div>
          </div>
        </div>
        <button class="upload-clear" type="button" @click="$emit('clear-upload')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>
      <div v-if="localUploadError" class="upload-error">{{ localUploadError }}</div>
      <div class="input-wrapper">
        <textarea
          v-model="inputMessage" 
          @keydown.enter.exact.prevent="handleSendMessage"
          @input="handleInput"
          :disabled="isLoading" 
          placeholder="Tanyakan apa saja ke PRISM..." 
          class="message-input" 
          ref="messageInput"
          rows="1"
        ></textarea>
        <div class="input-actions">
          <input
            ref="fileInput"
            class="file-input"
            type="file"
            accept=".pdf,image/*"
            @change="handleFileSelect"
          />
          <button
            class="attach-btn"
            type="button"
            :disabled="isLoading || (uploadState && uploadState.status === 'uploading')"
            title="Lampirkan file PDF/JPG"
            @click="openFilePicker"
          >
            <i class="fas fa-paperclip"></i>
          </button>
          <button
            class="copy-input-btn"
            type="button"
            :disabled="!inputMessage.trim()"
            :class="{ copied: copiedInput }"
            :title="copiedInput ? 'Tersalin' : 'Salin teks input'"
            @click="copyInput"
          >
            <i class="fas fa-copy"></i>
          </button>
          <button
            v-if="speechSupported.recognition"
            class="voice-btn"
            type="button"
            :class="{ listening: isListening }"
            :title="isListening ? 'Hentikan rekam' : 'Mulai rekam suara'"
            @click="toggleListening"
          >
            <i :class="isListening ? 'fas fa-stop' : 'fas fa-microphone'"></i>
          </button>
          <button 
            @click="handleSendMessage" 
            :disabled="!inputMessage.trim() || isLoading" 
            class="send-btn"
            type="button"
          >
            <i v-if="!isLoading" class="fas fa-paper-plane"></i>
            <i v-else class="fas fa-spinner fa-spin"></i>
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'ChatWindow',
  props: {
    messages: { type: Array, default: () => [] },
    isLoading: { type: Boolean, default: false },
    conversationTitle: { type: String, default: '' },
    backendStatus: { type: String, default: 'checking' },
    backendMessage: { type: String, default: '' },
    draft: { type: String, default: '' },
    uploadState: { type: Object, default: () => ({ status: 'idle', fileName: '', message: '' }) },
    attachments: { type: Array, default: () => [] },
    attachmentsLoading: { type: Boolean, default: false }
  },
  emits: [
    'send-message',
    'clear-chat',
    'go-to-info',
    'toggle-theme',
    'toggle-history',
    'export-chat',
    'regenerate-response',
    'feedback',
    'draft-change',
    'toggle-pin-message',
    'retry-connection',
    'edit-message',
    'upload-file',
    'clear-upload',
    'remove-attachment'
  ],
  data() {
    return {
      inputMessage: '',
      isDark: false,
      copiedIndex: null,
      copyTimer: null,
      copiedInput: false,
      inputCopyTimer: null,
      showScrollToBottom: false,
      isListening: false,
      dictationBase: '',
      recognition: null,
      speechSupported: {
        recognition: false,
        synthesis: false
      },
      speakingIndex: null,
      availableVoices: [],
      selectedVoice: null,
      localUploadError: '',
      searchTerm: '',
      searchPointer: 0,
      allPrompts: [
        'Apa keunggulan SMK Pertiwi Kuningan?',
        'Jurusan apa saja yang tersedia?',
        'RPL fokus belajar apa?',
        'Siapa kepala sekolah?',
        'Jadwal pelajaran sekolah',
        'Daftar guru RPL',
        'Siapa guru TKJ?',
        'Apa itu jurusan TKR?',
        'Mapel TSM apa saja?',
        'Alamat SMK Pertiwi Kuningan?'
      ],
      quickPrompts: []
    }
  },
  computed: {
    showQuickPrompts() {
      return this.messages.length <= 1 && !this.isLoading
    },
    parsedMessages() {
      return (this.messages || []).map((message) => {
        const parsed = this.parseMessageText(message.text || '')
        return {
          ...message,
          body: parsed.body,
          sources: parsed.sources,
          attachment: message.attachment || null
        }
      })
    },
    searchIndices() {
      const term = (this.searchTerm || '').trim().toLowerCase()
      if (!term) return []
      const indices = []
      for (let i = 0; i < this.messages.length; i += 1) {
        const text = (this.messages[i].text || '').toLowerCase()
        if (text.includes(term)) {
          indices.push(i)
        }
      }
      return indices
    },
    searchMatchSet() {
      return new Set(this.searchIndices)
    },
    activeMatchIndex() {
      if (!this.searchIndices.length) return -1
      return this.searchIndices[this.searchPointer] ?? -1
    },
    pinnedMessages() {
      return this.messages
        .map((message, index) => ({ ...message, index }))
        .filter(message => message.pinned)
    },
    lastUserIndex() {
      for (let i = this.messages.length - 1; i >= 0; i -= 1) {
        if (this.messages[i].sender === 'user') {
          return i
        }
      }
      return -1
    },
    lastAiIndex() {
      for (let i = this.messages.length - 1; i >= 0; i -= 1) {
        if (this.messages[i].sender === 'ai') {
          return i
        }
      }
      return -1
    }
  },
  created() {
    this.refreshQuickPrompts()
  },
  mounted() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const synth = typeof window !== 'undefined' ? window.speechSynthesis : null
    const savedTheme = localStorage.getItem('pertiwi_theme')
    if (savedTheme === 'dark') {
      this.isDark = true
    }
    this.speechSupported = {
      recognition: Boolean(SpeechRecognition),
      synthesis: Boolean(synth)
    }
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition()
      recognition.lang = 'id-ID'
      recognition.interimResults = true
      recognition.maxAlternatives = 1

      recognition.onresult = (event) => {
        let transcript = ''
        for (let i = event.resultIndex; i < event.results.length; i += 1) {
          transcript += event.results[i][0].transcript
        }
        transcript = transcript.trim()
        if (!transcript) return
        const base = this.dictationBase ? `${this.dictationBase} ` : ''
        this.inputMessage = `${base}${transcript}`.trim()
        this.$nextTick(() => this.autoResize())
      }

      recognition.onerror = () => {
        this.isListening = false
      }
      recognition.onend = () => {
        this.isListening = false
      }

      this.recognition = recognition
    }
    if (synth) {
      this.loadVoices()
      if (typeof synth.onvoiceschanged !== 'undefined') {
        synth.onvoiceschanged = () => this.loadVoices()
      }
    }
    this.autoResize()
    this.scrollToBottom()
  },
  watch: {
    messages() {
      this.$nextTick(() => {
        if (!this.showScrollToBottom) {
          this.scrollToBottom()
        } else {
          this.handleScroll()
        }
      })
      if (this.searchPointer >= this.searchIndices.length) {
        this.searchPointer = 0
      }
    },
    searchIndices(newList) {
      if (!newList.length) {
        this.searchPointer = 0
      } else if (this.searchPointer >= newList.length) {
        this.searchPointer = 0
      }
    },
    draft: {
      immediate: true,
      handler(value) {
        const next = typeof value === 'string' ? value : ''
        if (next !== this.inputMessage) {
          this.inputMessage = next
          this.$nextTick(() => this.autoResize())
        }
      }
    },
    inputMessage(value) {
      this.$emit('draft-change', value)
    }
  },
  methods: {
    handleSendMessage() {
      if (!this.inputMessage.trim() || this.isLoading) return
      const userMessage = this.inputMessage.trim()
      this.inputMessage = ''
      this.dictationBase = ''
      if (this.isListening && this.recognition) {
        this.recognition.stop()
      }
      this.$emit('send-message', userMessage)
      this.$nextTick(() => {
        this.autoResize()
      })
    },
    toggleTheme() {
      this.isDark = !this.isDark
      const newTheme = this.isDark ? 'dark' : 'light'
      this.$emit('toggle-theme', newTheme)
    },
    sendQuickPrompt(prompt) {
      if (!prompt || this.isLoading) return
      this.$emit('send-message', prompt)
    },
    resetSearch() {
      this.searchPointer = 0
      if (this.activeMatchIndex !== -1) {
        this.scrollToMessage(this.activeMatchIndex)
      }
    },
    nextSearch() {
      if (!this.searchIndices.length) return
      this.searchPointer = (this.searchPointer + 1) % this.searchIndices.length
      this.scrollToMessage(this.activeMatchIndex)
    },
    prevSearch() {
      if (!this.searchIndices.length) return
      this.searchPointer = (this.searchPointer - 1 + this.searchIndices.length) % this.searchIndices.length
      this.scrollToMessage(this.activeMatchIndex)
    },
    openFilePicker() {
      const input = this.$refs.fileInput
      if (input) {
        input.click()
      }
    },
    handleFileSelect(event) {
      const file = event.target.files && event.target.files[0]
      if (!file) return
      const maxSize = 4 * 1024 * 1024
      if (file.size > maxSize) {
        this.localUploadError = 'Ukuran file maksimal 4MB.'
        this.resetFileInput()
        return
      }
      this.localUploadError = ''
      this.$emit('upload-file', file)
      this.resetFileInput()
    },
    resetFileInput() {
      const input = this.$refs.fileInput
      if (input) {
        input.value = ''
      }
    },
    parseMessageText(text) {
      if (!text) {
        return { body: '', sources: [] }
      }
      const match = text.match(/(?:^|\n)Sumber:\s*/i)
      if (!match || match.index === undefined) {
        return { body: text, sources: [] }
      }
      const splitIndex = match.index
      const markerLength = match[0].length
      const body = text.slice(0, splitIndex).trim()
      const rawSources = text.slice(splitIndex + markerLength).trim()
      const lines = rawSources.split(/\n+/).map(line => line.trim()).filter(Boolean)
      const sources = []
      for (const line of lines) {
        const cleaned = line.replace(/^[-*\d.)\s]+/, '').trim()
        if (!cleaned) continue
        const urlMatch = cleaned.match(/https?:\/\/\S+/)
        const url = urlMatch ? urlMatch[0] : ''
        const label = url ? cleaned.replace(url, '').replace(/[:\-]\s*$/, '').trim() : cleaned
        if (url) {
          sources.push({ label: label || url, url })
        } else {
          sources.push({ label: cleaned, url: '' })
        }
      }
      return { body: body || text, sources }
    },
    formatAttachmentMeta(attachment) {
      if (!attachment) return ''
      const size = attachment.size ? this.formatBytes(attachment.size) : ''
      const type = attachment.contentType ? attachment.contentType.split('/').pop() : ''
      if (size && type) return `${type.toUpperCase()} · ${size}`
      if (size) return size
      if (type) return type.toUpperCase()
      return 'Lampiran'
    },
    formatBytes(bytes) {
      if (!bytes || Number.isNaN(bytes)) return ''
      const units = ['B', 'KB', 'MB', 'GB']
      let value = bytes
      let idx = 0
      while (value >= 1024 && idx < units.length - 1) {
        value /= 1024
        idx += 1
      }
      return `${value.toFixed(value >= 10 || idx === 0 ? 0 : 1)} ${units[idx]}`
    },
    handleInput() {
      this.autoResize()
    },
    togglePin(index) {
      this.$emit('toggle-pin-message', { index })
    },
    scrollToMessage(index) {
      const target = this.$el.querySelector(`[data-message-index="${index}"]`)
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    },
    toggleListening() {
      if (!this.recognition) {
        return
      }
      if (this.isListening) {
        this.recognition.stop()
        this.isListening = false
        return
      }
      this.dictationBase = this.inputMessage.trim()
      this.isListening = true
      try {
        this.recognition.start()
      } catch (error) {
        this.isListening = false
      }
    },
    toggleSpeak(text, index) {
      if (!this.speechSupported.synthesis || !text) return
      const synth = window.speechSynthesis
      if (this.speakingIndex === index) {
        synth.cancel()
        this.speakingIndex = null
        return
      }
      synth.cancel()
      const utterance = new SpeechSynthesisUtterance(this.cleanTtsText(text))
      utterance.lang = 'id-ID'
      if (this.selectedVoice) {
        utterance.voice = this.selectedVoice
      }
      utterance.rate = 1
      utterance.pitch = 1
      utterance.volume = 1
      utterance.onend = () => {
        if (this.speakingIndex === index) {
          this.speakingIndex = null
        }
      }
      utterance.onerror = () => {
        if (this.speakingIndex === index) {
          this.speakingIndex = null
        }
      }
      this.speakingIndex = index
      synth.speak(utterance)
    },
    loadVoices() {
      const synth = window.speechSynthesis
      if (!synth) return
      const voices = synth.getVoices() || []
      if (!voices.length) return
      this.availableVoices = voices
      if (!this.selectedVoice) {
        this.selectedVoice = this.pickBestVoice(voices)
      }
    },
    pickBestVoice(voices) {
      const prefer = (voice) => {
        const name = (voice.name || '').toLowerCase()
        return name.includes('google') || name.includes('microsoft')
      }
      const idVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('id'))
      if (idVoices.length) {
        return idVoices.find(prefer) || idVoices[0]
      }
      const enVoices = voices.filter(v => (v.lang || '').toLowerCase().startsWith('en'))
      return enVoices.find(prefer) || voices[0]
    },
    cleanTtsText(text) {
      if (!text) return ''
      return text
        .replace(/\n+/g, '. ')
        .replace(/[-•]\s+/g, '')
        .replace(/\s+/g, ' ')
        .trim()
    },
    refreshQuickPrompts() {
      const prompts = [...this.allPrompts]
      for (let i = prompts.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[prompts[i], prompts[j]] = [prompts[j], prompts[i]]
      }
      this.quickPrompts = prompts.slice(0, 6)
    },
    formatSource(source) {
      const map = {
        schoolData: 'Data Resmi',
        rag: 'Data Resmi',
        web: 'Internet'
      }
      return map[source] || 'Sumber'
    },
    showSource(source) {
      if (!source) return false
      return ['web', 'schoolData', 'rag'].includes(source)
    },
    async copyMessage(text, index) {
      if (!text) return
      try {
        const ok = await this.copyText(text)
        if (!ok) return
        this.copiedIndex = index
        if (this.copyTimer) {
          clearTimeout(this.copyTimer)
        }
        this.copyTimer = setTimeout(() => {
          this.copiedIndex = null
          this.copyTimer = null
        }, 1500)
      } catch (error) {
        console.error('Copy failed:', error)
      }
    },
    async copyInput() {
      const text = this.inputMessage.trim()
      if (!text) return
      try {
        const ok = await this.copyText(text)
        if (!ok) return
        this.copiedInput = true
        if (this.inputCopyTimer) {
          clearTimeout(this.inputCopyTimer)
        }
        this.inputCopyTimer = setTimeout(() => {
          this.copiedInput = false
          this.inputCopyTimer = null
        }, 1500)
      } catch (error) {
        console.error('Copy failed:', error)
      }
    },
    async copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text)
        return true
      }
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.focus()
      textarea.select()
      const success = document.execCommand('copy')
      document.body.removeChild(textarea)
      return success
    },
    autoResize() {
      const input = this.$refs.messageInput
      if (!input) return
      input.style.height = 'auto'
      const maxHeight = 160
      const newHeight = Math.min(input.scrollHeight, maxHeight)
      input.style.height = `${newHeight}px`
      input.style.overflowY = input.scrollHeight > maxHeight ? 'auto' : 'hidden'
    },
    handleScroll() {
      const container = this.$refs.chatMain
      if (!container) return
      const threshold = 24
      const atBottom = container.scrollHeight - container.scrollTop - container.clientHeight <= threshold
      this.showScrollToBottom = !atBottom
    },
    scrollToBottom() {
      const container = this.$refs.chatMain
      if (container) {
        this.$nextTick(() => {
          container.scrollTop = container.scrollHeight
          this.showScrollToBottom = false
        })
      }
    }
  }
}
</script>

<style scoped>
/* Chat App Container */
.chat-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--background);
  color: var(--text-primary);
  overflow: hidden;
}

/* Header */
.app-header {
  background: var(--surface);
  border-bottom: none;
  padding: 1rem 1.5rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-light);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  width: 48px;
  height: 48px;
  background: var(--surface-2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--primary-color);
  flex-shrink: 0;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
}

.school-info h1 {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary); /* Ensure this is dark in light mode */
}

/* Force dark text for header in light mode */
:global(html:not(.dark)) .chat-app .school-info h1 {
  color: #0f172a !important; /* Slate-900 */
}

.subtitle {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin: 0.125rem 0 0;
  font-weight: 500;
}

/* Force dark text for subtitle in light mode */
:global(html:not(.dark)) .chat-app .subtitle {
  color: #334155 !important; /* Slate-700 */
}

.conversation-title {
  font-size: 0.7rem;
  color: var(--primary-color);
  margin: 0.2rem 0 0;
  font-weight: 600;
  max-width: 240px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.header-actions {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  width: 36px;
  height: 36px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 0.9rem;
}

.icon-btn:hover {
  background: var(--primary-light);
  color: var(--text-primary);
}

.info-btn {
  color: var(--primary-color);
  font-weight: 600;
}

.info-btn:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}


.connection-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.6rem 1.2rem;
  background: #e0f2fe;
  color: #0369a1;
  border-bottom: 1px solid rgba(14, 116, 144, 0.2);
  font-size: 0.85rem;
  font-weight: 600;
}

.banner-info {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
}

.banner-btn {
  border: 1px solid rgba(14, 116, 144, 0.35);
  background: rgba(255, 255, 255, 0.7);
  color: inherit;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  cursor: pointer;
}

.banner-btn:hover {
  border-color: currentColor;
}

.connection-banner.offline {
  background: #fee2e2;
  color: #991b1b;
  border-bottom-color: rgba(185, 28, 28, 0.2);
}

.connection-banner.checking {
  background: #fef9c3;
  color: #92400e;
  border-bottom-color: rgba(180, 83, 9, 0.25);
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  background: var(--background);
  position: relative;
}

.chat-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.5rem 0.8rem;
  margin-bottom: 0.9rem;
  box-shadow: var(--shadow-light);
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.chat-search input {
  border: none;
  background: transparent;
  outline: none;
  flex: 1;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.search-count {
  font-weight: 600;
  color: var(--text-secondary);
}

.search-btn {
  border: 1px solid var(--border-color);
  background: var(--surface-2);
  color: var(--text-secondary);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.search-btn:hover:not(:disabled) {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.attachments-panel {
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.85rem;
  box-shadow: var(--shadow-light);
  margin-bottom: 1rem;
}

.attachments-header {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  margin-bottom: 0.6rem;
}

.attachments-count {
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  font-size: 0.7rem;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.attachment-loading {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.attachment-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  background: var(--surface-2);
  border-radius: 10px;
  padding: 0.6rem 0.8rem;
  border: 1px dashed var(--border-color);
}

.attachment-name {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.attachment-summary {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.2rem;
}

.attachment-remove {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.attachment-remove:hover {
  color: #ef4444;
}

/* Welcome Section */
.welcome-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 2rem;
}

.welcome-card {
  background: var(--surface);
  padding: 2.5rem;
  border-radius: 12px;
  text-align: center;
  max-width: 480px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.welcome-icon {
  font-size: 4rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.welcome-card h2 {
  margin: 0 0 0.75rem;
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.welcome-card p {
  color: var(--text-secondary);
  margin: 0 0 2rem;
  font-size: 0.95rem;
}

.pinned-section {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.9rem 1rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-light);
}

.pinned-header {
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.pinned-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.pinned-item {
  background: var(--surface-2);
  border-radius: 10px;
  padding: 0.65rem 0.85rem;
  border: 1px dashed var(--border-color);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.pinned-text {
  flex: 1;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pinned-actions {
  display: flex;
  gap: 0.4rem;
  flex-shrink: 0;
}

.pinned-btn {
  border: 1px solid var(--border-color);
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 8px;
  font-size: 0.75rem;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
}

.pinned-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.pinned-btn.ghost {
  background: transparent;
}

.features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-top: 2rem;
}

.feature {
  padding: 1.25rem;
  background: var(--surface-2);
  border-radius: 10px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: var(--transition);
}

.feature:hover {
  background: var(--primary-light);
}

.feature i {
  font-size: 1.5rem;
  color: var(--primary-color);
  display: block;
  margin-bottom: 0.75rem;
}

.feature span {
  font-size: 0.85rem;
  color: var(--text-primary);
  font-weight: 500;
  display: block;
}

/* Messages Container */
.messages-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-bottom: 2.5rem;
}

.quick-prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.prompt-refresh {
  padding: 0.5rem 0.9rem;
  border-radius: 999px;
  border: 1px dashed var(--border-color);
  background: transparent;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.75rem;
  cursor: pointer;
  transition: var(--transition);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.prompt-refresh:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.prompt-chip {
  padding: 0.5rem 0.9rem;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--surface-2);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: var(--transition);
}

.prompt-chip:hover {
  background: var(--primary-light);
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: min(720px, 78%);
  animation: slideInUp 0.3s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-wrapper.user {
  align-self: flex-end;
}

.message-wrapper.ai {
  align-self: flex-start;
}

.message-wrapper.pinned .message-bubble {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-light);
}

.message-wrapper.matched .message-bubble {
  border-color: #f59e0b;
}

.message-wrapper.active .message-bubble {
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.35);
}

.message-sender {
  display: none;
}

.message-sender i {
  font-size: 0.75rem;
}

.message-bubble {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.6;
  position: relative;
}

.message-attachment {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px dashed var(--border-color);
  border-radius: 10px;
  padding: 0.5rem 0.7rem;
  margin-bottom: 0.6rem;
}

.message-wrapper.user .message-attachment {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.35);
}

.attachment-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--surface);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
}

.message-wrapper.user .attachment-icon {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.35);
  color: var(--user-msg-text);
}

.attachment-details {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.attachment-title {
  font-weight: 600;
  font-size: 0.85rem;
  color: inherit;
}

.attachment-meta {
  font-size: 0.7rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.message-wrapper.user .message-bubble {
  background: var(--user-msg-bg);
  color: var(--user-msg-text);
  border-radius: 12px;
  font-weight: 500;
  padding: 0.875rem 1.25rem;
}

.message-wrapper.ai .message-bubble {
  background: var(--ai-msg-bg);
  color: var(--ai-msg-text); /* Use variable but ensure it is dark */
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
  font-weight: 500; /* Increase weight */
}

/* Force dark text if variables fail in light mode context (fallback) */
:global(html:not(.dark)) .chat-app .message-wrapper.ai .message-bubble {
    color: #0f172a !important; /* Slate-900 */
    background: #ffffff !important;
}

.message-bubble p {
  margin: 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

.message-source {
  margin-top: 0.45rem;
  font-size: 0.7rem;
  color: var(--text-secondary);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.message-sources {
  margin-top: 0.6rem;
  background: var(--surface);
  border: 1px dashed var(--border-color);
  border-radius: 10px;
  padding: 0.55rem 0.75rem;
}

.sources-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.35rem;
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.source-item {
  font-size: 0.78rem;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.source-item:hover {
  text-decoration: underline;
}

.message-actions {
  position: static;
  margin-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.4rem;
}

.message-action-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--surface);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  cursor: pointer;
  opacity: 0.65;
  transition: var(--transition);
}

.message-wrapper.user .message-action-btn {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.35);
  color: var(--user-msg-text);
}

.message-action-btn:hover {
  opacity: 1;
  transform: translateY(-1px);
}

.message-action-btn.copied,
.message-action-btn.active {
  color: var(--accent-color);
  border-color: var(--accent-color);
  opacity: 1;
}

.regen-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.pin-btn:hover {
  color: #f59e0b;
  border-color: #f59e0b;
}

.pin-btn.active {
  color: #f59e0b;
  border-color: #f59e0b;
  opacity: 1;
}

.feedback-btn:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.edit-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.875rem 1.25rem;
  background: var(--ai-msg-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  width: fit-content;
  animation: slideInUp 0.3s ease-out;
}

.typing-dots {
  display: flex;
  gap: 0.3rem;
}

.dot {
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: typingBounce 1.4s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% { opacity: 0.5; transform: translateY(0); }
  30% { opacity: 1; transform: translateY(-8px); }
}

/* Footer & Input */
.chat-footer {
  padding: 1rem 1.5rem;
  border-top: none;
  background: var(--surface);
  flex-shrink: 0;
  box-shadow: var(--shadow-light);
}

.upload-state {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.6rem 0.8rem;
  margin-bottom: 0.6rem;
}

.upload-state.uploading {
  border-color: var(--primary-color);
}

.upload-state.error {
  border-color: #ef4444;
  color: #ef4444;
}

.upload-info {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.upload-info i {
  color: var(--primary-color);
}

.upload-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-name {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.upload-message {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.upload-clear {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.upload-clear:hover {
  color: #ef4444;
}

.upload-error {
  margin-bottom: 0.6rem;
  color: #ef4444;
  font-size: 0.8rem;
  font-weight: 600;
}

.input-wrapper {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.input-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.file-input {
  display: none;
}

.attach-btn {
  width: 40px;
  height: 40px;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 0.95rem;
  flex-shrink: 0;
}

.attach-btn:hover:not(:disabled) {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.attach-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message-input {
  flex: 1;
  padding: 0.875rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  color: var(--text-primary);
  transition: var(--transition);
  background: var(--surface);
  resize: none;
  min-height: 44px;
  max-height: 160px;
  line-height: 1.5;
}

.message-input::placeholder {
  color: var(--text-secondary);
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.message-input:disabled {
  opacity: 0.6;
  background: var(--disabled-bg);
}

.copy-input-btn {
  width: 40px;
  height: 40px;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 0.95rem;
  flex-shrink: 0;
}

.copy-input-btn:hover:not(:disabled) {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.copy-input-btn.copied {
  color: var(--accent-color);
  border-color: var(--accent-color);
}

.copy-input-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.voice-btn {
  width: 40px;
  height: 40px;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 0.95rem;
  flex-shrink: 0;
}

.voice-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.voice-btn.listening {
  color: var(--accent-color);
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);
}

.send-btn {
  width: 40px;
  height: 40px;
  background: var(--user-msg-bg);
  border: none;
  border-radius: 8px;
  color: var(--user-msg-text);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 1rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-light);
}

.send-btn:hover:not(:disabled) {
  background: var(--primary-dark);
}

.send-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.scroll-to-bottom {
  position: sticky;
  bottom: 1.25rem;
  align-self: flex-end;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--surface);
  color: var(--text-secondary);
  box-shadow: var(--shadow-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  margin-left: auto;
  z-index: 2;
}

.scroll-to-bottom:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

/* Scrollbar */
.messages-container::-webkit-scrollbar,
.chat-main::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track,
.chat-main::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb,
.chat-main::-webkit-scrollbar-thumb {
  background: var(--gray-medium);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover,
.chat-main::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}

@media (max-width: 480px) {
  .app-header {
    padding: 0.8rem 1rem;
  }

  .header-actions {
    gap: 0.4rem;
    flex-wrap: wrap;
  }

  .icon-btn {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }

  .chat-main {
    padding: 1rem;
  }

  .message-input {
    padding: 0.8rem 0.9rem;
  }

  .send-btn {
    width: 36px;
    height: 36px;
  }

  .scroll-to-bottom {
    width: 36px;
    height: 36px;
    bottom: 1rem;
  }
}
</style>
