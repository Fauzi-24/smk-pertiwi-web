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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
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
        } catch (_) {}
        const err = new Error(errorMessage);
        err.code = `HTTP_${response.status}`;
        throw err;
      }
      return await response.json();
    } catch (error) {
      console.error('Clear files failed:', error);
      throw error;
    }
  }
};

export default ChatAPI;
