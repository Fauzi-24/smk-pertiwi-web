<template>
  <div v-if="open" class="sidebar-overlay" @click.self="$emit('close')">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>Riwayat Obrolan</h2>
        <button class="icon-btn" type="button" title="Tutup" @click="$emit('close')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <div class="sidebar-actions">
        <button class="new-chat-btn" type="button" @click="$emit('new')">
          <i class="fas fa-plus"></i>
          Obrolan Baru
        </button>
        <button class="clear-chat-btn" type="button" @click="$emit('clear-all')">
          <i class="fas fa-trash"></i>
          Hapus Semua
        </button>
        <button class="admin-btn" type="button" @click.stop="$emit('open-admin')">
          <i class="fas fa-shield-halved"></i>
          Admin Review
        </button>
      </div>

      <div class="search-box">
        <i class="fas fa-magnifying-glass"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari obrolan..."
          @input="filterChats"
        />
      </div>

      <div class="chat-list">
        <div
          v-for="chat in filteredConversations"
          :key="chat.id"
          :class="['chat-item', { active: chat.id === activeId }]"
        >
          <button class="chat-item-main" type="button" @click="$emit('select', chat.id)">
            <div v-if="editingId !== chat.id" class="chat-title">
              {{ chat.title || 'Obrolan Baru' }}
            </div>
            <input
              v-else
              v-model="draftTitle"
              class="chat-title-input"
              type="text"
              @keydown.enter.prevent="commitRename(chat.id)"
              @keydown.esc.prevent="cancelRename"
              @blur="commitRename(chat.id)"
            />
            <div class="chat-meta">{{ formatTime(chat.updatedAt || chat.createdAt) }}</div>
          </button>
          <button class="chat-delete" type="button" title="Hapus" @click="$emit('delete', chat.id)">
            <i class="fas fa-trash"></i>
          </button>
          <button class="chat-edit" type="button" title="Ubah judul" @click.stop="startRename(chat)">
            <i class="fas fa-pen"></i>
          </button>
          <button class="chat-pin" type="button" :title="chat.pinned ? 'Lepas pin' : 'Pin obrolan'" @click.stop="$emit('pin', chat.id)">
            <i :class="chat.pinned ? 'fas fa-star' : 'far fa-star'"></i>
          </button>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
export default {
  name: 'ChatSidebar',
  props: {
    open: { type: Boolean, default: false },
    conversations: { type: Array, default: () => [] },
    activeId: { type: String, default: null }
  },
  emits: ['close', 'select', 'new', 'delete', 'rename', 'pin', 'clear-all', 'open-admin'],
  data() {
    return {
      searchQuery: '',
      filteredConversations: [],
      editingId: null,
      draftTitle: ''
    }
  },
  watch: {
    conversations: {
      immediate: true,
      handler() {
        this.filterChats()
      }
    },
    open(isOpen) {
      if (!isOpen) {
        this.searchQuery = ''
        this.filterChats()
        this.cancelRename()
      }
    }
  },
  methods: {
    filterChats() {
      const query = (this.searchQuery || '').trim().toLowerCase()
      if (!query) {
        this.filteredConversations = [...this.conversations]
        return
      }
      this.filteredConversations = this.conversations.filter(item => {
        const title = (item.title || '').toLowerCase()
        return title.includes(query)
      })
    },
    startRename(chat) {
      if (!chat) return
      this.editingId = chat.id
      this.draftTitle = chat.title || 'Obrolan Baru'
      this.$nextTick(() => {
        const input = this.$el.querySelector('.chat-title-input')
        if (input) {
          input.focus()
          input.select()
        }
      })
    },
    cancelRename() {
      this.editingId = null
      this.draftTitle = ''
    },
    commitRename(id) {
      if (!id || this.editingId !== id) return
      const title = (this.draftTitle || '').trim()
      if (title) {
        this.$emit('rename', { id, title })
      }
      this.cancelRename()
    },
    formatTime(value) {
      if (!value) return ''
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return ''
      return date.toLocaleString('id-ID', {
        day: '2-digit',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  display: flex;
  justify-content: flex-start;
  z-index: 50;
}

.sidebar {
  width: min(320px, 90vw);
  height: 100%;
  background: var(--surface);
  border-right: 1px solid var(--border-color);
  padding: 1rem;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-header h2 {
  font-size: 1.05rem;
  margin: 0;
  color: var(--text-primary);
}

.icon-btn {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.icon-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.new-chat-btn {
  width: 100%;
  border: none;
  background: var(--primary-gradient);
  color: #fff;
  padding: 0.7rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: var(--shadow-light);
}

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.clear-chat-btn {
  width: 100%;
  border: 1px solid var(--border-color);
  background: transparent;
  color: var(--text-secondary);
  padding: 0.6rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.clear-chat-btn:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.admin-btn {
  width: 100%;
  border: 1px solid var(--border-color);
  background: var(--surface-2);
  color: var(--text-secondary);
  padding: 0.6rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.admin-btn:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--surface-2);
  color: var(--text-secondary);
}

.search-box input {
  border: none;
  background: transparent;
  outline: none;
  color: var(--text-primary);
  font-size: 0.85rem;
  width: 100%;
}

.chat-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  overflow-y: auto;
  padding-right: 4px;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.6rem;
}

.chat-item.active {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-light);
}

.chat-item-main {
  flex: 1;
  border: none;
  background: transparent;
  text-align: left;
  cursor: pointer;
  color: var(--text-primary);
}

.chat-title {
  font-weight: 600;
  font-size: 0.9rem;
}

.chat-title-input {
  width: 100%;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 0.35rem 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  background: var(--surface);
  color: var(--text-primary);
}

.chat-meta {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.2rem;
}

.chat-delete {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.3rem;
}

.chat-delete:hover {
  color: #ef4444;
}

.chat-edit {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.3rem;
}

.chat-edit:hover {
  color: var(--primary-color);
}

.chat-pin {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.3rem;
}

.chat-pin:hover {
  color: #f59e0b;
}

@media (max-width: 640px) {
  .sidebar {
    width: 100%;
    border-right: none;
  }
}
</style>
