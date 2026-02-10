<template>
    <div :class="['message-bubble-container', sender]">
        <div class="avatar">
            <i v-if="sender === 'user'" class="fas fa-user"></i>
            <i v-else class="fas fa-robot"></i>
        </div>
        <div class="bubble-content">
            <div class="message-header">
                <span class="sender-name">{{ sender === 'user' ? 'Anda' : 'Pertiwi Assistant' }}</span>
                <span class="message-time">{{ formatTime(time) }}</span>
            </div>
            <div :class="['bubble', sender]">
                <div class="message-text">
                    <p v-for="(line, index) in text.split('\n')" :key="index">
                        {{ line }}
                    </p>
                </div>
                <div v-if="sender === 'ai'" class="ai-actions">
                    <button class="action-btn" @click="copyToClipboard" title="Salin teks">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button class="action-btn" @click="speakText" title="Dengarkan">
                        <i class="fas fa-volume-up"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MessageBubble',
    props: {
        sender: {
            type: String,
            required: true,
            validator: value => ['user', 'ai'].includes(value)
        },
        text: {
            type: String,
            required: true
        },
        time: {
            type: [Date, String],
            required: true
        }
    },
    methods: {
        formatTime(timestamp) {
            const date = typeof timestamp === 'string' ? new Date(timestamp) : timestamp
            return date.toLocaleTimeString('id-ID', {
                hour: '2-digit',
                minute: '2-digit'
            })
        },
        
        copyToClipboard() {
            navigator.clipboard.writeText(this.text).then(() => {
                // Optional: Show toast notification
                console.log('Teks berhasil disalin!')
            }).catch(err => {
                console.error('Gagal menyalin teks:', err)
            })
        },
        
        speakText() {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(this.text)
                utterance.lang = 'id-ID'
                utterance.rate = 1.0
                utterance.pitch = 1.0
                window.speechSynthesis.speak(utterance)
            } else {
                alert('Browser tidak mendukung text-to-speech')
            }
        }
    }
}
</script>

<style scoped>
.message-bubble-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    animation: fadeIn 0.3s ease-out;
}

.message-bubble-container.user {
    flex-direction: row-reverse;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.message-bubble-container.user .avatar {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    color: white;
}

.message-bubble-container.ai .avatar {
    background: var(--gray-light);
    color: var(--text-primary);
}

.bubble-content {
    flex: 1;
    max-width: calc(100% - 60px);
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.sender-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-primary);
}

.message-time {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.bubble {
    padding: 1rem 1.25rem;
    border-radius: var(--radius-lg);
    position: relative;
    transition: transform 0.2s;
}

.bubble:hover {
    transform: translateY(-2px);
}

.bubble.user {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border-bottom-right-radius: var(--radius-sm);
    margin-left: auto;
}

.bubble.ai {
    background: var(--white);
    color: var(--text-primary);
    border: 1px solid var(--gray-light);
    border-bottom-left-radius: var(--radius-sm);
    box-shadow: var(--shadow);
}

.message-text {
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}

.message-text p {
    margin: 0 0 0.5rem 0;
}

.message-text p:last-child {
    margin-bottom: 0;
}

.ai-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.bubble.user .ai-actions {
    display: none;
}

.action-btn {
    background: none;
    border: 1px solid var(--gray-light);
    color: var(--text-secondary);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    font-size: 0.9rem;
}

.action-btn:hover {
    background: var(--primary-light);
    color: var(--primary-color);
    border-color: var(--primary-color);
}

/* Responsive */
@media (max-width: 768px) {
    .message-bubble-container {
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .avatar {
        width: 36px;
        height: 36px;
        font-size: 0.9rem;
    }
    
    .bubble {
        padding: 0.75rem 1rem;
    }
    
    .sender-name {
        font-size: 0.85rem;
    }
    
    .message-time {
        font-size: 0.7rem;
    }
}
</style>