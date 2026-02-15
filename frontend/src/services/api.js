// API Service untuk SMK Pertiwi Chatbot

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

// Types/Interfaces
export const ChatAPI = {
  /**
   * Health check endpoint
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  /**
   * Send chat message to AI
   * @param {string} message - User message
   * @param {string|null} sessionId - Optional session ID for conversation tracking
   * @param {Array|null} history - Optional chat history
   * @returns {Promise<Object>} Chat response with session_id and message
   */
  async sendMessage(message, sessionId = null, history = null, memory = null, conversationId = null) {
    try {
      const payload = {
        message,
        session_id: sessionId,
        history: history,
        memory: memory,
        conversation_id: conversationId
      };

      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        // Handle rate limit / quota exceeded gracefully
        if (response.status === 429) {
          const err = new Error('Kuota AI sementara penuh, silakan coba lagi dalam 1-2 menit.');
          err.code = 'RATE_LIMIT';
          throw err;
        }

        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) {
          // fallback to default message
        }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }

      return await response.json();
    } catch (error) {
      console.error('Chat message failed:', error);
      throw error;
    }
  },

  /**
   * Send chat message to AI with streaming response
   * @param {string} message - User message
   * @param {string|null} sessionId - Optional session ID
   * @param {Array|null} history - Optional chat history
   * @param {Array|null} memory - Optional memory context
   * @param {string|null} conversationId - Optional conversation ID
   * @param {Function} onChunk - Callback for each text chunk
   * @param {Function} onMeta - Callback for metadata (session_id, etc)
   * @param {Function} onSource - Callback for source info
   * @returns {Promise<void>}
   */
  async sendMessageStream(message, sessionId = null, history = null, memory = null, conversationId = null, onChunk, onMeta, onSource) {
    try {
      const payload = {
        message,
        session_id: sessionId,
        history: history,
        memory: memory,
        conversation_id: conversationId
      };

      const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Kuota AI sementara penuh. Coba lagi nanti.');
        }
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (_) { }
        throw new Error(errorMessage);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      try {
        let buffer = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split('\n');
          // Keep the last partial line, if it's empty it means the previous line was complete
          buffer = parts.pop() || '';

          for (const line of parts) {
            if (!line.trim()) continue;
            try {
              const data = JSON.parse(line);
              if (data.type === 'chunk') {
                if (onChunk) onChunk(data.content);
              } else if (data.type === 'meta') {
                if (onMeta) onMeta(data);
              } else if (data.type === 'source') {
                if (onSource) onSource(data);
              } else if (data.type === 'error') {
                throw new Error(data.content);
              }
            } catch (e) {
              console.warn('Failed to parse stream line:', line, e);
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      console.error('Stream chat failed:', error);
      throw error;
    }
  },

  /**
   * Get session history
   * @param {string} sessionId - Session ID
   * @returns {Promise<Object>} Session history
   */
  async getSessionHistory(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Get session history failed:', error);
      throw error;
    }
  },

  /**
   * Delete session
   * @param {string} sessionId - Session ID
   * @returns {Promise<Object>} Deletion response
   */
  async deleteSession(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Delete session failed:', error);
      throw error;
    }
  }
  ,
  /**
   * Submit feedback/correction
   * @param {Object} payload
   */
  async sendFeedback(payload) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }

      return await response.json();
    } catch (error) {
      console.error('Send feedback failed:', error);
      throw error;
    }
  }
  ,
  async adminListFeedback(adminKey) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/feedback`, {
        headers: {
          'X-Admin-Key': adminKey || ''
        }
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Admin list feedback failed:', error);
      throw error;
    }
  },
  async adminApproveFeedback(id, adminKey) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/feedback/${id}/approve`, {
        method: 'POST',
        headers: {
          'X-Admin-Key': adminKey || ''
        }
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Admin approve feedback failed:', error);
      throw error;
    }
  },
  async adminRejectFeedback(id, adminKey) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/feedback/${id}/reject`, {
        method: 'POST',
        headers: {
          'X-Admin-Key': adminKey || ''
        }
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Admin reject feedback failed:', error);
      throw error;
    }
  },
  async adminExport(dataset, adminKey) {
    try {
      const url = `${API_BASE_URL}/api/admin/export?dataset=${encodeURIComponent(dataset || 'pending')}`;
      const response = await fetch(url, {
        headers: {
          'X-Admin-Key': adminKey || ''
        }
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.blob();
    } catch (error) {
      console.error('Admin export failed:', error);
      throw error;
    }
  },
  async uploadFile(file, sessionId = null, conversationId = null) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (sessionId) {
        formData.append('session_id', sessionId);
      }
      if (conversationId) {
        formData.append('conversation_id', conversationId);
      }

      const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }

      return await response.json();
    } catch (error) {
      console.error('Upload file failed:', error);
      throw error;
    }
  },
  async listFiles(sessionId = null, conversationId = null) {
    try {
      const params = new URLSearchParams();
      if (sessionId) params.append('session_id', sessionId);
      if (conversationId) params.append('conversation_id', conversationId);
      const response = await fetch(`${API_BASE_URL}/api/files?${params.toString()}`);
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('List files failed:', error);
      throw error;
    }
  },
  async deleteFile(fileId, sessionId = null, conversationId = null) {
    try {
      const params = new URLSearchParams();
      if (sessionId) params.append('session_id', sessionId);
      if (conversationId) params.append('conversation_id', conversationId);
      const response = await fetch(`${API_BASE_URL}/api/files/${fileId}?${params.toString()}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Delete file failed:', error);
      throw error;
    }
  },
  async clearFiles(sessionId = null, conversationId = null) {
    try {
      const params = new URLSearchParams();
      if (sessionId) params.append('session_id', sessionId);
      if (conversationId) params.append('conversation_id', conversationId);
      const response = await fetch(`${API_BASE_URL}/api/files?${params.toString()}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Clear files failed:', error);
      throw error;
    }
  },

  /**
   * Register new student via PPDB
   * @param {Object} data - Registration data
   * @returns {Promise<Object>} Registration response
   */
  async registerPPDB(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ppdb/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (_) { }
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }

      return await response.json();
    } catch (error) {
      console.error('PPDB registration failed:', error);
      throw error;
    }
  },

  async adminLogin(key) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ admin_key: key })
      });
      if (!response.ok) throw new Error('Login failed');
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async getPPDBData(token) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/ppdb?token=${token}`);
      if (!response.ok) throw new Error('Failed to fetch data');
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async getDashboardStats(token) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/stats?key=${token}`);
      if (!response.ok) throw new Error('Failed to fetch stats');
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async deletePPDBData(id, token) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/ppdb/${id}?token=${token}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to delete data');
      return await response.json();
      return await response.json();
    } catch (error) {
      throw error;
    }
  },

  async updatePPDBStatus(id, status, token) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/ppdb/${id}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status, token })
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (_) { }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('Update PPDB status failed:', error);
      throw error;
    }
  },

  /**
   * Register new PPDB student
   * @param {Object} payload - Student registration data
   * @returns {Promise<Object>} Registration response
   */
  async registerPPDB(payload) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ppdb/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('PPDB registration failed:', error);
      throw error;
    }
  }
};

export default ChatAPI;
