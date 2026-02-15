<template>
  <div class="chat-widget">
    <!-- Floating Toggle Button -->
    <button class="chat-toggle-btn" @click="toggleChat" :class="{ 'open': isOpen }">
      <i class="fas" :class="isOpen ? 'fa-times' : 'fa-comment-dots'"></i>
    </button>

    <!-- Chat Container -->
    <div class="chat-container" :class="{ 'open': isOpen }">
      <ChatWindow 
        :messages="activeMessages"
        :conversationTitle="activeTitle"
        :isLoading="isLoading"
        :backendStatus="backendStatus"
        :backendMessage="backendMessage"
        :draft="activeDraft"
        :uploadState="uploadState"
        :attachments="activeAttachments"
        :attachmentsLoading="attachmentsLoading"
        @send-message="handleSendMessage"
        @draft-change="handleDraftChange"
        @retry-connection="handleRetryBackend"
        @upload-file="handleUploadFile"
        @clear-upload="clearUploadState"
        @remove-attachment="removeAttachment"
        @clear-chat="handleClearChat"
        @go-to-info="handleGoToInfo"
        @toggle-theme="setTheme"
        @export-chat="exportActiveConversation"
        @regenerate-response="regenerateLastResponse"
        @feedback="openFeedback"
        @toggle-history="toggleSidebar"
        @toggle-pin-message="togglePinMessage"
        @edit-message="editMessage"
      />

      <ChatSidebar
        :open="showSidebar"
        :conversations="sortedConversations"
        :activeId="activeConversationId"
        @close="showSidebar = false"
        @select="selectConversation"
        @new="startNewConversation"
        @delete="requestDeleteConversation"
        @pin="togglePinConversation"
        @clear-all="requestClearAllConversations"
        @rename="renameConversation"
        @open-admin="openAdminPanel"
      />

      <!-- Dialogs -->
      <ConfirmDialog
        :open="confirmState.open"
        :title="confirmState.title"
        :message="confirmState.message"
        :confirmLabel="confirmState.confirmLabel"
        :cancelLabel="confirmState.cancelLabel"
        @confirm="handleConfirm"
        @cancel="closeConfirm"
      />

      <FeedbackDialog
        :open="feedbackState.open"
        :question="feedbackState.question"
        :answer="feedbackState.answer"
        :loading="feedbackState.loading"
        @submit="submitFeedback"
        @cancel="closeFeedback"
      />

      <AdminLoginDialog
        :open="adminLoginState.open"
        :adminKey="adminState.key"
        :loading="adminLoginState.loading"
        :error="adminLoginState.error"
        @cancel="closeAdminLogin"
        @submit="submitAdminLogin"
        @update-key="updateAdminKey"
      />

      <AdminPanel
        :open="adminState.open"
        :items="adminState.items"
        :loading="adminState.loading"
        :error="adminState.error"
        @close="closeAdminPanel"
        @refresh="loadAdminFeedback"
        @approve="approveAdminFeedback"
        @reject="rejectAdminFeedback"
        @logout="logoutAdmin"
        @export="handleAdminExport"
      />
    </div>
  </div>
</template>

<script>
import ChatWindow from './ChatWindow.vue'
import ChatSidebar from './ChatSidebar.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import FeedbackDialog from './FeedbackDialog.vue'
import AdminPanel from './AdminPanel.vue'
import AdminLoginDialog from './AdminLoginDialog.vue'
import ChatAPI from '../services/api.js'

export default {
  name: 'ChatWidget',
  components: {
    ChatWindow,
    ChatSidebar,
    ConfirmDialog,
    FeedbackDialog,
    AdminPanel,
    AdminLoginDialog
  },
  props: {
    alwaysOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isOpen: false,
      conversations: [],
      activeConversationId: null,
      isLoading: false,
      error: null,
      chatStorageKey: 'prism_conversations_v1',
      showSidebar: false,
      drafts: {},
      draftStorageKey: 'prism_drafts_v1',
      confirmState: {
        open: false,
        title: '',
        message: '',
        confirmLabel: 'Hapus',
        cancelLabel: 'Batal',
        action: null,
        payload: null
      },
      feedbackState: {
        open: false,
        question: '',
        answer: '',
        messageIndex: null,
        loading: false
      },
      adminState: {
        open: false,
        key: '',
        items: [],
        loading: false,
        error: '',
        loggedIn: false
      },
      adminLoginState: {
        open: false,
        loading: false,
        error: ''
      },
      backendStatus: 'checking',
      backendMessage: '',
      uploadState: {
        status: 'idle',
        fileName: '',
        message: '',
        previewUrl: '',
        isImage: false
      },
      attachmentsByConversation: {},
      attachmentsLoading: false,
      healthTimer: null
    }
  },
  computed: {
    activeConversation() {
      return this.conversations.find(item => item.id === this.activeConversationId) || null
    },
    activeMessages() {
      return this.activeConversation ? this.activeConversation.messages : []
    },
    activeTitle() {
      return this.activeConversation ? this.activeConversation.title : ''
    },
    activeDraft() {
      if (!this.activeConversationId) return ''
      return this.drafts[this.activeConversationId] || ''
    },
    activeAttachments() {
      if (!this.activeConversationId) return []
      return this.attachmentsByConversation[this.activeConversationId] || []
    },
    sortedConversations() {
      return [...this.conversations].sort((a, b) => {
        if (Boolean(a.pinned) !== Boolean(b.pinned)) {
          return a.pinned ? -1 : 1
        }
        const aTime = new Date(a.updatedAt || a.createdAt || 0).getTime()
        const bTime = new Date(b.updatedAt || b.createdAt || 0).getTime()
        return bTime - aTime
      })
    }
  },
  mounted() {
    this.loadConversations()
    this.loadDrafts()
    this.loadAdminKey()
    this.initializeApp()
    this.applyTheme()
    this.startHealthPolling()
    if (this.alwaysOpen) {
      this.isOpen = true
    }
  },
  watch: {
    activeConversationId(newId) {
      if (newId) {
        this.loadAttachments()
      }
    }
  },
  beforeUnmount() {
    this.stopHealthPolling()
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
    },
    handleGoToInfo(payload) {
      if (payload && payload.tab) {
         if (payload.tab === 'info') this.$router.push('/profil')
         else if (payload.tab === 'jurusan') this.$router.push('/jurusan')
         else this.$router.push('/' + payload.tab)
      } else {
         this.$router.push('/profil')
      }
      // Mobile: close chat on nav
      if (window.innerWidth < 768) {
        this.isOpen = false
      }
    },
    async initializeApp() {
      await this.checkBackendHealth()
    },
    startHealthPolling() {
      if (this.healthTimer) return
      this.healthTimer = setInterval(() => {
        this.checkBackendHealth(true)
      }, 30000)
    },
    stopHealthPolling() {
      if (this.healthTimer) {
        clearInterval(this.healthTimer)
        this.healthTimer = null
      }
    },
    async checkBackendHealth(silent = false) {
      if (!silent) {
        this.setBackendStatus('checking', 'Menghubungkan ke server...')
      }
      try {
        const health = await ChatAPI.healthCheck()
        console.log('✅ Backend is healthy:', health)
        this.setBackendStatus('online')
      } catch (error) {
        console.error('❌ Backend health check failed:', error)
        this.error = 'Backend tidak tersedia. Pastikan server berjalan di port 8000'
        this.setBackendStatus('offline', this.error)
      }
    },
    setBackendStatus(status, message = '') {
        this.backendStatus = status
        this.backendMessage = message || ''
    },
    handleRetryBackend() {
      this.checkBackendHealth()
    },
    applyTheme() {
      const savedTheme = localStorage.getItem('pertiwi_theme') || 'light'
      this.setTheme(savedTheme)
    },
    setTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark')
        document.documentElement.style.setProperty('--background', '#0F172A')
        document.documentElement.style.setProperty('--background-dark', '#0B1220')
        document.documentElement.style.setProperty('--white', '#111827')
        document.documentElement.style.setProperty('--surface', '#111827')
        document.documentElement.style.setProperty('--surface-2', '#1F2937')
        document.documentElement.style.setProperty('--text-primary', '#F9FAFB')
        document.documentElement.style.setProperty('--text-secondary', '#CBD5E1')
        document.documentElement.style.setProperty('--gray-light', '#334155')
        document.documentElement.style.setProperty('--gray-medium', '#475569')
        document.documentElement.style.setProperty('--gray-dark', '#94A3B8')
        document.documentElement.style.setProperty('--ai-msg-bg', '#111827')
        document.documentElement.style.setProperty('--ai-msg-text', '#F9FAFB')
        document.documentElement.style.setProperty('--user-msg-bg', '#2563EB')
        document.documentElement.style.setProperty('--user-msg-text', '#FFFFFF')
        document.documentElement.style.setProperty('--card-bg', '#111827')
        document.documentElement.style.setProperty('--border-color', '#334155')
        document.documentElement.style.setProperty('--disabled-bg', '#334155')
        document.documentElement.style.setProperty('--shadow', '0 4px 12px rgba(0, 0, 0, 0.35)')
        document.documentElement.style.setProperty('--shadow-light', '0 2px 6px rgba(0, 0, 0, 0.3)')
        document.documentElement.style.setProperty('--shadow-hover', '0 8px 20px rgba(0, 0, 0, 0.4)')
      } else {
        document.documentElement.classList.remove('dark')
        document.documentElement.style.setProperty('--background', '#FFFFFF')
        document.documentElement.style.setProperty('--background-dark', '#F9FAFB')
        document.documentElement.style.setProperty('--white', '#FFFFFF')
        document.documentElement.style.setProperty('--surface', '#FFFFFF')
        document.documentElement.style.setProperty('--surface-2', '#F9FAFB')
        document.documentElement.style.setProperty('--text-primary', '#111827')
        document.documentElement.style.setProperty('--text-secondary', '#6B7280')
        document.documentElement.style.setProperty('--gray-light', '#E5E7EB')
        document.documentElement.style.setProperty('--gray-medium', '#D1D5DB')
        document.documentElement.style.setProperty('--gray-dark', '#6B7280')
        document.documentElement.style.setProperty('--ai-msg-bg', '#FFFFFF')
        document.documentElement.style.setProperty('--ai-msg-text', '#0F172A')
        document.documentElement.style.setProperty('--user-msg-bg', '#2563EB')
        document.documentElement.style.setProperty('--user-msg-text', '#FFFFFF')
        document.documentElement.style.setProperty('--card-bg', '#FFFFFF')
        document.documentElement.style.setProperty('--border-color', '#E2E8F0')
        document.documentElement.style.setProperty('--border-rgb', '226, 232, 240')
        document.documentElement.style.setProperty('--surface-rgb', '255, 255, 255')
        document.documentElement.style.setProperty('--disabled-bg', '#E2E8F0')
        document.documentElement.style.setProperty('--shadow', '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)')
        document.documentElement.style.setProperty('--shadow-light', '0 1px 2px 0 rgba(0, 0, 0, 0.05)')
        document.documentElement.style.setProperty('--shadow-hover', '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)')
      }
      localStorage.setItem('pertiwi_theme', theme)
    },
    greetingMessage() {
      return {
        sender: 'ai',
        text: 'Halo, saya PRISM (Pertiwi Responsive Intelligent Smart Model). Siap bantu tanya sekolah, jurusan, maupun info lain seputar SMK Pertiwi.',
        timestamp: new Date()
      }
    },
    createConversation() {
      const id = `chat_${Date.now()}`
      const now = new Date()
      const conversation = {
        id,
        title: 'Obrolan Baru',
        sessionId: null,
        pinned: false,
        messages: [this.greetingMessage()],
        createdAt: now.toISOString(),
        updatedAt: now.toISOString()
      }
      this.conversations.unshift(conversation)
      this.activeConversationId = id
      this.saveConversations()
      return conversation
    },
    saveConversations() {
      try {
        const payload = this.conversations.map(item => ({
          ...item,
          messages: (item.messages || []).slice(-200).map(message => ({
            sender: message.sender,
            text: message.text,
            source: message.source || null,
            pinned: Boolean(message.pinned),
            attachment: message.attachment || null,
            timestamp: message.timestamp ? new Date(message.timestamp).toISOString() : null
          }))
        }))
        localStorage.setItem(this.chatStorageKey, JSON.stringify(payload))
      } catch (error) {
        console.warn('Failed to save conversations:', error)
      }
    },
    loadConversations() {
      try {
        const raw = localStorage.getItem(this.chatStorageKey)
        if (!raw) {
          this.createConversation()
          return
        }
        const saved = JSON.parse(raw)
        if (Array.isArray(saved) && saved.length > 0) {
          this.conversations = saved.map(item => ({
            ...item,
            pinned: Boolean(item.pinned),
            messages: (item.messages || []).map(message => ({
              sender: message.sender,
              text: message.text,
              source: message.source || null,
              pinned: Boolean(message.pinned),
              attachment: message.attachment || null,
              timestamp: message.timestamp ? new Date(message.timestamp) : new Date()
            }))
          }))
          this.activeConversationId = this.conversations[0].id
          return
        }
        this.createConversation()
      } catch (error) {
        console.warn('Failed to load conversations:', error)
        this.createConversation()
      }
    },
    requestDeleteConversation(id) {
      if (!id) return
      this.openConfirm({
        title: 'Hapus obrolan?',
        message: 'Obrolan ini akan dihapus dari perangkatmu.',
        confirmLabel: 'Hapus',
        action: 'delete-conversation',
        payload: id
      })
    },
    requestClearAllConversations() {
      this.openConfirm({
        title: 'Hapus semua obrolan?',
        message: 'Semua obrolan akan dihapus dari perangkatmu. Aksi ini tidak bisa dibatalkan.',
        confirmLabel: 'Hapus Semua',
        action: 'clear-all'
      })
    },
    deleteConversation(id) {
      const index = this.conversations.findIndex(item => item.id === id)
      if (index === -1) return
      const [removed] = this.conversations.splice(index, 1)
      if (removed && removed.sessionId) {
        ChatAPI.deleteSession(removed.sessionId).catch(() => {})
        ChatAPI.clearFiles(removed.sessionId, removed.id).catch(() => {})
      }
      if (this.activeConversationId === id) {
        if (this.conversations.length) {
          this.activeConversationId = this.conversations[0].id
        } else {
          this.createConversation()
        }
      }
      this.removeDraft(id)
      this.removeAttachments(id)
      this.saveConversations()
    },
    clearAllConversations() {
      const items = [...this.conversations]
      items.forEach(item => {
        if (item.sessionId) {
          ChatAPI.deleteSession(item.sessionId).catch(() => {})
        }
        ChatAPI.clearFiles(item.sessionId || null, item.id).catch(() => {})
      })
      this.conversations = []
      this.activeConversationId = null
      this.createConversation()
      this.clearDrafts()
      this.attachmentsByConversation = {}
      this.saveConversations()
    },
    loadDrafts() {
      try {
        const raw = localStorage.getItem(this.draftStorageKey)
        if (raw) {
          const parsed = JSON.parse(raw)
          if (parsed && typeof parsed === 'object') {
            this.drafts = parsed
          }
        }
      } catch (error) {
        console.warn('Failed to load drafts:', error)
      }
    },
    saveDrafts() {
      try {
        localStorage.setItem(this.draftStorageKey, JSON.stringify(this.drafts || {}))
      } catch (error) {
        console.warn('Failed to save drafts:', error)
      }
    },
    handleDraftChange(value) {
      const conversationId = this.activeConversationId
      if (!conversationId) return
      if (!value) {
        this.removeDraft(conversationId)
        return
      }
      this.drafts = {
        ...this.drafts,
        [conversationId]: value
      }
      this.saveDrafts()
    },
    removeDraft(conversationId) {
      if (!conversationId || !this.drafts[conversationId]) return
      const { [conversationId]: _, ...rest } = this.drafts
      this.drafts = rest
      this.saveDrafts()
    },
    removeAttachments(conversationId) {
      if (!conversationId) return
      const { [conversationId]: _, ...rest } = this.attachmentsByConversation
      this.attachmentsByConversation = rest
    },
    clearDrafts() {
      this.drafts = {}
      this.saveDrafts()
    },
    async loadAttachments() {
      const conversation = this.activeConversation
      if (!conversation) return
      this.attachmentsLoading = true
      try {
        const response = await ChatAPI.listFiles(conversation.sessionId, conversation.id)
        this.attachmentsByConversation = {
          ...this.attachmentsByConversation,
          [conversation.id]: response.items || []
        }
      } catch (_) {
        this.attachmentsByConversation = {
          ...this.attachmentsByConversation,
          [conversation.id]: []
        }
      } finally {
        this.attachmentsLoading = false
      }
    },
    async removeAttachment(fileId) {
      const conversation = this.activeConversation
      if (!conversation || !fileId) return
      try {
        await ChatAPI.deleteFile(fileId, conversation.sessionId, conversation.id)
      } catch (error) {
        console.error('Delete attachment failed:', error)
      } finally {
        this.loadAttachments()
      }
    },
    setUploadState(next) {
      this.uploadState = {
        status: next.status || 'idle',
        fileName: next.fileName || '',
        message: next.message || '',
        previewUrl: next.previewUrl || '',
        isImage: Boolean(next.isImage)
      }
    },
    clearUploadState() {
      this.releaseUploadPreview()
      this.setUploadState({ status: 'idle' })
    },
    releaseUploadPreview() {
      if (this.uploadState.previewUrl) {
        URL.revokeObjectURL(this.uploadState.previewUrl)
      }
    },
    async handleUploadFile(file) {
      if (!file) return
      const conversation = this.activeConversation || this.createConversation()
      this.releaseUploadPreview()
      const isImage = file.type.startsWith('image/')
      const previewUrl = isImage ? URL.createObjectURL(file) : ''
      this.setUploadState({
        status: 'uploading',
        fileName: file.name,
        message: 'Mengunggah file...',
        previewUrl,
        isImage
      })
      try {
        const response = await ChatAPI.uploadFile(file, conversation.sessionId, conversation.id)
        if (response.session_id && !conversation.sessionId) {
          conversation.sessionId = response.session_id
        }
        conversation.messages.push({
          sender: 'user',
          text: `Mengirim lampiran: ${file.name}`,
          timestamp: new Date(),
          attachment: {
            filename: file.name,
            contentType: file.type || '',
            size: file.size || 0
          }
        })
        conversation.messages.push({
          sender: 'ai',
          text: `File "${file.name}" berhasil diunggah. Kamu bisa tanya isi dokumen.`,
          timestamp: new Date(),
          source: response.source || 'file'
        })
        conversation.updatedAt = new Date().toISOString()
        this.saveConversations()
        this.loadAttachments()
        this.clearUploadState()
      } catch (error) {
        this.setUploadState({
          status: 'error',
          fileName: file.name,
          message: error.message || 'Upload gagal. Coba lagi.',
          previewUrl,
          isImage
        })
        conversation.messages.push({
          sender: 'ai',
          text: `Upload file gagal: ${error.message || 'Coba lagi atau gunakan PDF/JPG/PNG di bawah 4MB.'}`,
          timestamp: new Date()
        })
        conversation.updatedAt = new Date().toISOString()
        this.saveConversations()
      }
    },
    openConfirm({ title, message, confirmLabel, cancelLabel, action, payload }) {
      this.confirmState = {
        open: true,
        title: title || 'Konfirmasi',
        message: message || 'Anda yakin?',
        confirmLabel: confirmLabel || 'Ya',
        cancelLabel: cancelLabel || 'Batal',
        action: action || null,
        payload: payload || null
      }
    },
    closeConfirm() {
      this.confirmState = {
        open: false,
        title: '',
        message: '',
        confirmLabel: 'Hapus',
        cancelLabel: 'Batal',
        action: null,
        payload: null
      }
    },
    handleConfirm() {
      const { action, payload } = this.confirmState
      this.closeConfirm()
      if (action === 'delete-conversation') {
        this.deleteConversation(payload)
      } else if (action === 'clear-all') {
        this.clearAllConversations()
      }
    },
    openFeedback(payload) {
      const conversation = this.activeConversation
      if (!conversation || !payload) return
      const index = payload.index
      if (index === null || index === undefined) return
      const messages = conversation.messages || []
      const aiMessage = messages[index]
      if (!aiMessage || aiMessage.sender !== 'ai') return
      let question = ''
      for (let i = index - 1; i >= 0; i -= 1) {
        if (messages[i].sender === 'user') {
          question = messages[i].text || ''
          break
        }
      }
      this.feedbackState = {
        open: true,
        question,
        answer: aiMessage.text || '',
        messageIndex: index,
        loading: false
      }
    },
    closeFeedback() {
      this.feedbackState = {
        open: false,
        question: '',
        answer: '',
        messageIndex: null,
        loading: false
      }
    },
    async submitFeedback(payload) {
      if (!payload || !payload.correction) return
      const conversation = this.activeConversation
      if (!conversation) return
      this.feedbackState.loading = true
      try {
        await ChatAPI.sendFeedback({
          question: this.feedbackState.question,
          answer: this.feedbackState.answer,
          correction: payload.correction,
          source: payload.source,
          session_id: conversation.sessionId,
          conversation_id: conversation.id
        })
        conversation.messages.push({
          sender: 'ai',
          text: 'Terima kasih! Koreksi kamu sudah dikirim dan akan direview admin.',
          timestamp: new Date()
        })
        conversation.updatedAt = new Date().toISOString()
        this.saveConversations()
        this.closeFeedback()
      } catch (error) {
        console.error('Feedback submit failed:', error)
        this.feedbackState.loading = false
      }
    },
    loadAdminKey() {
      try {
        const stored = localStorage.getItem('prism_admin_key')
        if (stored) {
          this.adminState.key = stored
        }
      } catch (_) {}
    },
    updateAdminKey(value) {
      if (value !== this.adminState.key) {
        this.adminState.loggedIn = false
      }
      this.adminState.key = value
    },
    saveAdminKey() {
      try {
        localStorage.setItem('prism_admin_key', this.adminState.key || '')
      } catch (_) {}
    },
    openAdminLogin() {
      this.adminLoginState = {
        open: true,
        loading: false,
        error: ''
      }
    },
    closeAdminLogin() {
      this.adminLoginState = {
        open: false,
        loading: false,
        error: ''
      }
    },
    async submitAdminLogin() {
      if (!this.adminState.key) {
        this.adminLoginState.error = 'Masukkan ADMIN_KEY terlebih dahulu.'
        return
      }
      this.adminLoginState.loading = true
      this.adminLoginState.error = ''
      try {
        const response = await ChatAPI.adminListFeedback(this.adminState.key)
        this.adminState.items = response.items || []
        this.adminState.loggedIn = true
        this.adminState.error = ''
        this.adminState.open = true
        this.saveAdminKey()
        this.closeAdminLogin()
      } catch (error) {
        this.adminLoginState.error = error.message || 'Admin key tidak valid.'
        this.adminLoginState.loading = false
      }
    },
    logoutAdmin() {
      this.adminState.loggedIn = false
      this.adminState.key = ''
      this.adminState.items = []
      this.adminState.error = ''
      this.adminState.open = false
      this.adminLoginState = {
        open: false,
        loading: false,
        error: ''
      }
      try {
        localStorage.removeItem('prism_admin_key')
      } catch (_) {}
    },
    openAdminPanel() {
      this.showSidebar = false
      if (this.adminState.loggedIn) {
        this.adminState.open = true
        this.loadAdminFeedback()
        return
      }
      this.openAdminLogin()
    },
    closeAdminPanel() {
      this.adminState.open = false
    },
    async loadAdminFeedback() {
      if (!this.adminState.loggedIn) {
        this.adminState.error = 'Silakan login admin terlebih dahulu.'
        return
      }
      if (!this.adminState.key) {
        this.adminState.error = 'Masukkan ADMIN_KEY terlebih dahulu.'
        return
      }
      this.adminState.loading = true
      this.adminState.error = ''
      try {
        const response = await ChatAPI.adminListFeedback(this.adminState.key)
        this.adminState.items = response.items || []
      } catch (error) {
        this.adminState.error = error.message || 'Gagal mengambil data admin.'
      } finally {
        this.adminState.loading = false
      }
    },
    async approveAdminFeedback(id) {
      if (!id) return
      this.adminState.loading = true
      this.adminState.error = ''
      try {
        await ChatAPI.adminApproveFeedback(id, this.adminState.key)
        await this.loadAdminFeedback()
      } catch (error) {
        this.adminState.error = error.message || 'Gagal menyetujui.'
        this.adminState.loading = false
      }
    },
    async rejectAdminFeedback(id) {
      if (!id) return
      this.adminState.loading = true
      this.adminState.error = ''
      try {
        await ChatAPI.adminRejectFeedback(id, this.adminState.key)
        await this.loadAdminFeedback()
      } catch (error) {
        this.adminState.error = error.message || 'Gagal menolak.'
        this.adminState.loading = false
      }
    },
    togglePinConversation(id) {
      const conversation = this.conversations.find(item => item.id === id)
      if (!conversation) return
      conversation.pinned = !conversation.pinned
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
    },
    renameConversation({ id, title }) {
      const conversation = this.conversations.find(item => item.id === id)
      if (!conversation || !title) return
      conversation.title = title
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
    },
    selectConversation(id) {
      this.activeConversationId = id
      this.showSidebar = false
      this.saveConversations()
    },
    startNewConversation() {
      this.createConversation()
      this.showSidebar = false
    },
    handleClearChat() {
      if (!this.activeConversationId) return
      const conversation = this.activeConversation
      if (!conversation) return
      if (conversation.messages.length <= 1) return
      this.openConfirm({
        title: 'Bersihkan chat?',
        message: 'Pesan akan dihapus dari obrolan ini.',
        confirmLabel: 'Bersihkan',
        action: 'clear-chat'
      })
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar
    },
    togglePinMessage(payload) {
      const conversation = this.activeConversation
      if (!conversation || !payload) return
      const index = payload.index
      if (index === null || index === undefined) return
      const message = conversation.messages[index]
      if (!message) return
      message.pinned = !message.pinned
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
    },
    editMessage(payload) {
      const conversation = this.activeConversation
      if (!conversation || !payload) return
      const index = payload.index
      if (index === null || index === undefined) return
      const message = conversation.messages[index]
      if (!message || message.sender !== 'user') return
      const text = message.text || ''
      conversation.messages = conversation.messages.slice(0, index)
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
      this.handleDraftChange(text)
    },
    buildGlobalMemory(activeId) {
      const others = this.conversations
        .filter(item => item.id !== activeId)
        .sort((a, b) => new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0))
      const memory = []
      for (const convo of others) {
        const recentUsers = (convo.messages || [])
          .filter(message => message.sender === 'user')
          .slice(-2)
        for (const msg of recentUsers) {
          if (msg && msg.text) {
            memory.push(`User pernah menanyakan: ${msg.text}`)
          }
        }
        if (memory.length >= 12) break
      }
      return memory.slice(0, 12)
    },
    async handleSendMessage(userMessage) {
      if (!userMessage.trim()) return
      const conversation = this.activeConversation || this.createConversation()
      this.handleDraftChange('')
      conversation.messages.push({
        sender: 'user',
        text: userMessage,
        timestamp: new Date()
      })
      if (conversation.title === 'Obrolan Baru') {
        conversation.title = userMessage.slice(0, 42)
      }
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
      this.isLoading = true
      const aiMessageIndex = conversation.messages.push({
        sender: 'ai',
        text: '',
        timestamp: new Date(),
        source: null,
        isStreaming: true
      }) - 1
      const aiMessage = conversation.messages[aiMessageIndex]
      try {
        const historyPayload = conversation.messages.slice(0, -1).map(message => ({
          role: message.sender === 'user' ? 'user' : 'model',
          parts: [message.text]
        }))
        const memory = this.buildGlobalMemory(conversation.id)
        await ChatAPI.sendMessageStream(
          userMessage,
          conversation.sessionId,
          historyPayload,
          memory,
          conversation.id,
          (chunk) => {
            aiMessage.text += chunk
          },
          (meta) => {
             if (meta.session_id) {
               conversation.sessionId = meta.session_id
             }
          },
          (sourceData) => {
             aiMessage.source = sourceData.label
             if (sourceData.details) {
               aiMessage.sourceDetails = sourceData.details
             }
          }
        )
        this.setBackendStatus('online')
        conversation.updatedAt = new Date().toISOString()
        aiMessage.isStreaming = false
        this.saveConversations()
      } catch (error) {
        console.error('Failed to send message:', error)
        aiMessage.isStreaming = false
        if (!aiMessage.text) {
          let friendly = 'Maaf, terjadi kesalahan teknis. Silakan coba kembali.'
          if (error.message && error.message.includes('Quota')) {
             friendly = 'Maaf, kuota AI sedang penuh.'
          }
           aiMessage.text = friendly
        } else {
           aiMessage.text += '\n\n[Terputus: terjadi kesalahan teknis]'
        }
        conversation.updatedAt = new Date().toISOString()
        this.saveConversations()
      } finally {
        this.isLoading = false
      }
    },
    async regenerateLastResponse() {
      if (this.isLoading) return
      const conversation = this.activeConversation
      if (!conversation) return
      const messages = conversation.messages || []
      const lastUserIndex = [...messages].reverse().findIndex(item => item.sender === 'user')
      if (lastUserIndex === -1) return
      const actualIndex = messages.length - 1 - lastUserIndex
      const lastUserMessage = messages[actualIndex]
      if (!lastUserMessage || !lastUserMessage.text) return
      conversation.messages = messages.slice(0, actualIndex + 1)
      conversation.updatedAt = new Date().toISOString()
      this.saveConversations()
      this.isLoading = true
      const aiMessageIndex = conversation.messages.push({
        sender: 'ai',
        text: '',
        timestamp: new Date(),
        source: null,
        isStreaming: true
      }) - 1
      const aiMessage = conversation.messages[aiMessageIndex]
      try {
        const historyPayload = conversation.messages.slice(0, -1).map(message => ({
          role: message.sender === 'user' ? 'user' : 'model',
          parts: [message.text]
        }))
        const memory = this.buildGlobalMemory(conversation.id)
        await ChatAPI.sendMessageStream(
          lastUserMessage.text,
          conversation.sessionId,
          historyPayload,
          memory,
          conversation.id,
          (chunk) => {
            aiMessage.text += chunk
          },
          (meta) => {
             if (meta.session_id) {
               conversation.sessionId = meta.session_id
             }
          },
          (sourceData) => {
             aiMessage.source = sourceData.label
          }
        )
        this.setBackendStatus('online')
        conversation.updatedAt = new Date().toISOString()
        aiMessage.isStreaming = false
        this.saveConversations()
      } catch (error) {
        console.error('Failed to regenerate:', error)
        aiMessage.isStreaming = false
        if (!aiMessage.text) {
            aiMessage.text = 'Maaf, gagal membuat jawaban baru.'
        }
        conversation.updatedAt = new Date().toISOString()
        this.saveConversations()
      } finally {
        this.isLoading = false
      }
    },
    exportActiveConversation() {
      const conversation = this.activeConversation
      if (!conversation) return
      const lines = []
      const title = conversation.title || 'Obrolan'
      lines.push(`Judul: ${title}`)
      lines.push(`Dibuat: ${conversation.createdAt || '-'}`)
      lines.push(`Terakhir: ${conversation.updatedAt || '-'}`)
      lines.push('')
      for (const message of conversation.messages || []) {
        const role = message.sender === 'user' ? 'User' : 'Prism'
        const time = message.timestamp ? new Date(message.timestamp).toLocaleString('id-ID') : ''
        lines.push(`[${role}] ${time}`.trim())
        lines.push(message.text || '')
        lines.push('')
      }
      const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = `${title.replace(/[^a-z0-9]+/gi, '_').toLowerCase() || 'obrolan'}.txt`
      document.body.appendChild(anchor)
      anchor.click()
      document.body.removeChild(anchor)
      URL.revokeObjectURL(url)
    },
    async handleAdminExport(dataset) {
      try {
        const blob = await ChatAPI.adminExport(dataset, this.adminState.key)
        const url = URL.createObjectURL(blob)
        const anchor = document.createElement('a')
        anchor.href = url
        anchor.download = `admin_${dataset || 'data'}.csv`
        document.body.appendChild(anchor)
        anchor.click()
        document.body.removeChild(anchor)
        URL.revokeObjectURL(url)
      } catch (error) {
        console.error('Export failed:', error)
        this.adminState.error = error.message || 'Gagal export data.'
      }
    }
  }
}
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 9999;
}

.chat-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--primary-color, #2563EB);
  color: white;
  border: none;
  font-size: 1.5rem;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.chat-toggle-btn.open {
  transform: rotate(90deg);
  background: #DC2626;
}

.chat-container {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 400px;
  height: 600px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 120px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  overflow: hidden;
  transform: translateY(20px);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.chat-container.open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

/* Override ChatWindow styles to fit widget */
:deep(.chat-app) {
  height: 100%;
  max-width: 100%;
}

:deep(.app-header) {
  padding: 0.8rem 1rem;
}

:deep(.logo img) {
  height: 32px;
}

:deep(.school-info h1) {
  font-size: 1.1rem;
}

:deep(.school-info .subtitle) {
  font-size: 0.8rem;
}

/* Mobile Responsive */
@media (max-width: 480px) {
  .chat-widget {
    bottom: 20px;
    right: 20px;
  }
  
  .chat-container {
    right: 0;
    left: 0;
    bottom: 0;
    top: 0;
    width: 100%;
    height: 100vh;
    max-width: 100%;
    max-height: 100%;
    border-radius: 0;
    z-index: 9998;
  }
  
  .chat-toggle-btn.open {
    display: none; /* Hide toggle when full screen open */
  }
}
</style>
