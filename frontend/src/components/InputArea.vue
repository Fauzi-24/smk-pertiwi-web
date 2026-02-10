<template>
    <div class="input-area">
        <!-- Quick Actions -->
        <div v-if="showQuickActions" class="quick-actions">
            <div class="quick-grid">
                <button 
                    v-for="(action, index) in quickActions" 
                    :key="index"
                    @click="handleQuickAction(action.command)"
                    :class="['quick-action-btn', action.type]"
                    :title="action.tooltip"
                >
                    <i :class="action.icon"></i>
                    <span class="action-label">{{ action.label }}</span>
                </button>
            </div>
        </div>
        
        <!-- Main Input -->
        <div class="main-input">
            <div class="input-wrapper">
                <textarea
                    ref="textInput"
                    v-model="inputText"
                    @keydown.enter.exact.prevent="handleSend"
                    @keydown.enter.shift.exact.prevent="inputText += '\n'"
                    :placeholder="placeholder"
                    :disabled="isLoading"
                    rows="1"
                    class="text-input"
                    @input="autoResize"
                ></textarea>
                
                <div class="input-controls">
                    <!-- Attachment Button -->
                    <button 
                        class="control-btn"
                        @click="toggleQuickActions"
                        :title="showQuickActions ? 'Sembunyikan aksi cepat' : 'Tampilkan aksi cepat'"
                    >
                        <i class="fas" :class="showQuickActions ? 'fa-times' : 'fa-bolt'"></i>
                    </button>
                    
                    <!-- Send Button -->
                    <button 
                        class="send-button"
                        @click="handleSend"
                        :disabled="!canSend"
                        :class="{ 'loading': isLoading }"
                        :title="isLoading ? 'Mengirim...' : 'Kirim pesan'"
                    >
                        <i v-if="!isLoading" class="fas fa-paper-plane"></i>
                        <i v-else class="fas fa-spinner fa-spin"></i>
                    </button>
                </div>
            </div>
            
            <!-- Character Counter -->
            <div class="input-info">
                <span class="char-counter" :class="{ 'warning': isNearLimit }">
                    {{ inputText.length }}/{{ maxChars }}
                </span>
                
                <div class="hint">
                    <i class="fas fa-lightbulb"></i>
                    Tekan Enter untuk kirim, Shift+Enter untuk baris baru
                </div>
            </div>
        </div>
        
        <!-- Emoji Picker (Optional) -->
        <div v-if="showEmojiPicker" class="emoji-picker">
            <div class="emoji-grid">
                <span 
                    v-for="emoji in commonEmojis" 
                    :key="emoji"
                    @click="insertEmoji(emoji)"
                    class="emoji-item"
                >
                    {{ emoji }}
                </span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'InputArea',
    props: {
        isLoading: {
            type: Boolean,
            default: false
        },
        placeholder: {
            type: String,
            default: 'Tulis pesan...'
        },
        maxChars: {
            type: Number,
            default: 2000
        }
    },
    data() {
        return {
            inputText: '',
            showQuickActions: false,
            showEmojiPicker: false,
            quickActions: [
                {
                    icon: 'fas fa-question-circle',
                    label: 'Tanya Jurusan',
                    command: 'jurusan',
                    type: 'info',
                    tooltip: 'Tanya tentang jurusan sekolah'
                },
                {
                    icon: 'fas fa-calendar-alt',
                    label: 'Jadwal',
                    command: 'jadwal',
                    type: 'schedule',
                    tooltip: 'Tanya jadwal sekolah'
                },
                {
                    icon: 'fas fa-file-alt',
                    label: 'Pendaftaran',
                    command: 'pendaftaran',
                    type: 'register',
                    tooltip: 'Info pendaftaran siswa baru'
                },
                {
                    icon: 'fas fa-users',
                    label: 'Guru & Staf',
                    command: 'guru',
                    type: 'people',
                    tooltip: 'Informasi guru dan staf'
                },
                {
                    icon: 'fas fa-trophy',
                    label: 'Prestasi',
                    command: 'prestasi',
                    type: 'achievement',
                    tooltip: 'Prestasi sekolah'
                },
                {
                    icon: 'fas fa-map-marker-alt',
                    label: 'Lokasi',
                    command: 'lokasi',
                    type: 'location',
                    tooltip: 'Lokasi SMK Pertiwi'
                }
            ],
            commonEmojis: ['😊', '👍', '👏', '🎓', '🏫', '📚', '💻', '🎨', '💰', '📝', '❓', '💡']
        }
    },
    computed: {
        canSend() {
            return this.inputText.trim().length > 0 && !this.isLoading && this.inputText.length <= this.maxChars
        },
        isNearLimit() {
            return this.inputText.length > this.maxChars * 0.9
        }
    },
    methods: {
        handleSend() {
            if (this.canSend) {
                this.$emit('send', this.inputText.trim())
                this.inputText = ''
                this.autoResize()
                this.showQuickActions = false
                this.showEmojiPicker = false
            }
        },
        
        handleQuickAction(command) {
            const questions = {
                'jurusan': 'Jurusan apa saja yang ada di SMK Pertiwi Kuningan?',
                'jadwal': 'Bagaimana jadwal sekolah di SMK Pertiwi?',
                'pendaftaran': 'Bagaimana cara mendaftar sebagai siswa baru di SMK Pertiwi?',
                'guru': 'Siapa saja guru dan staf pengajar di SMK Pertiwi?',
                'prestasi': 'Apa saja prestasi yang pernah diraih SMK Pertiwi Kuningan?',
                'lokasi': 'Dimana alamat lengkap SMK Pertiwi Kuningan?'
            }
            
            this.inputText = questions[command] || `Tentang ${command} di SMK Pertiwi Kuningan`
            this.$nextTick(() => {
                this.autoResize()
                this.$refs.textInput.focus()
            })
        },
        
        toggleQuickActions() {
            this.showQuickActions = !this.showQuickActions
            if (this.showQuickActions) {
                this.showEmojiPicker = false
            }
        },
        
        toggleEmojiPicker() {
            this.showEmojiPicker = !this.showEmojiPicker
            if (this.showEmojiPicker) {
                this.showQuickActions = false
            }
        },
        
        insertEmoji(emoji) {
            this.inputText += emoji
            this.$nextTick(() => {
                this.autoResize()
                this.$refs.textInput.focus()
            })
        },
        
        autoResize() {
            const textarea = this.$refs.textInput
            if (textarea) {
                textarea.style.height = 'auto'
                const newHeight = Math.min(textarea.scrollHeight, 150)
                textarea.style.height = newHeight + 'px'
            }
        },
        
        focus() {
            if (this.$refs.textInput) {
                this.$refs.textInput.focus()
            }
        }
    },
    mounted() {
        // Auto focus on mount
        this.$nextTick(() => {
            if (this.$refs.textInput) {
                this.$refs.textInput.focus()
            }
        })
    },
    watch: {
        inputText() {
            this.autoResize()
        }
    }
}
</script>

<style scoped>
.input-area {
    background: var(--white);
    border-top: 1px solid var(--gray-light);
    padding: 1rem;
}

/* Quick Actions */
.quick-actions {
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease-out;
}

.quick-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}

@media (min-width: 640px) {
    .quick-grid {
        grid-template-columns: repeat(6, 1fr);
    }
}

.quick-action-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    border: 1px solid var(--gray-light);
    border-radius: var(--radius-md);
    background: var(--background);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
}

.quick-action-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

.quick-action-btn.info {
    border-color: var(--primary-color);
    background: var(--primary-light);
    color: var(--primary-dark);
}

.quick-action-btn.schedule {
    border-color: #4CAF50;
    background: #E8F5E9;
    color: #2E7D32;
}

.quick-action-btn.register {
    border-color: #FF9800;
    background: #FFF3E0;
    color: #EF6C00;
}

.quick-action-btn.people {
    border-color: #9C27B0;
    background: #F3E5F5;
    color: #7B1FA2;
}

.quick-action-btn.achievement {
    border-color: #F44336;
    background: #FFEBEE;
    color: #D32F2F;
}

.quick-action-btn.location {
    border-color: #2196F3;
    background: #E3F2FD;
    color: #1565C0;
}

.quick-action-btn i {
    font-size: 1.25rem;
}

.action-label {
    font-size: 0.8rem;
    font-weight: 500;
    text-align: center;
}

/* Main Input */
.main-input {
    position: relative;
}

.input-wrapper {
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
}

.text-input {
    flex: 1;
    padding: 1rem 1.25rem;
    border: 2px solid var(--gray-light);
    border-radius: var(--radius-lg);
    background: var(--background);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1rem;
    resize: none;
    min-height: 56px;
    max-height: 150px;
    line-height: 1.5;
    transition: border-color 0.2s;
}

.text-input:focus {
    outline: none;
    border-color: var(--primary-color);
}

.text-input:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.input-controls {
    display: flex;
    gap: 0.5rem;
    align-items: flex-end;
    margin-bottom: 0.5rem;
}

.control-btn {
    width: 44px;
    height: 44px;
    border: 1px solid var(--gray-light);
    background: var(--background);
    color: var(--text-secondary);
    border-radius: var(--radius-md);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.control-btn:hover {
    background: var(--primary-light);
    color: var(--primary-color);
    border-color: var(--primary-color);
}

.send-button {
    width: 56px;
    height: 56px;
    background: var(--primary-color);
    border: none;
    border-radius: var(--radius-lg);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    transition: all 0.2s;
}

.send-button:hover:not(:disabled) {
    background: var(--primary-dark);
    transform: scale(1.05);
}

.send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.send-button.loading {
    background: var(--text-secondary);
}

/* Input Info */
.input-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
    font-size: 0.85rem;
}

.char-counter {
    color: var(--text-secondary);
    font-family: monospace;
}

.char-counter.warning {
    color: #f44336;
    font-weight: bold;
}

.hint {
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hint i {
    color: #FFC107;
}

/* Emoji Picker */
.emoji-picker {
    position: absolute;
    bottom: 100%;
    left: 0;
    right: 0;
    background: var(--white);
    border: 1px solid var(--gray-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--shadow-hover);
    z-index: 10;
    animation: fadeIn 0.2s ease-out;
}

.emoji-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.5rem;
}

.emoji-item {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    transition: background 0.2s;
}

.emoji-item:hover {
    background: var(--primary-light);
}

/* Responsive */
@media (max-width: 768px) {
    .input-area {
        padding: 0.75rem;
    }
    
    .quick-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .text-input {
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
    }
    
    .control-btn {
        width: 40px;
        height: 40px;
    }
    
    .send-button {
        width: 48px;
        height: 48px;
        font-size: 1.1rem;
    }
    
    .emoji-grid {
        grid-template-columns: repeat(4, 1fr);
    }
    
    .input-info {
        flex-direction: column;
        gap: 0.5rem;
        align-items: flex-start;
    }
}
</style>