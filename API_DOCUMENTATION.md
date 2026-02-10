# API Documentation - SMK Pertiwi Chatbot

## Overview

The SMK Pertiwi Chatbot is a full-stack chatbot application powered by Google's Gemini AI. It consists of a **FastAPI backend** and a **Vue.js frontend**.

**Backend URL**: `http://localhost:8000`  
**Frontend URL**: `http://localhost:5174`

---

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Backend will be available at: `http://localhost:8000`  
Frontend will be available at: `http://localhost:5174`

---

## API Endpoints

### 1. Root Endpoint
**GET** `/`

Returns HTML page with API information.

**Response**: HTML page (200 OK)

---

### 2. Health Check
**GET** `/health`

Check if the backend server is running and healthy.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "app_name": "SMK Pertiwi Chatbot",
  "version": "1.0.0",
  "timestamp": "2024-02-07T12:00:00.000000"
}
```

---

### 3. Send Chat Message
**POST** `/api/chat`

Send a message to the AI chatbot and receive a response.

**Request Body**:
```json
{
  "message": "Jurusan apa saja di SMK Pertiwi?",
  "session_id": "session_1707329000_abc123xyz",
  "history": [
    {
      "role": "user",
      "content": "Halo"
    },
    {
      "role": "assistant",
      "content": "Halo! Saya Pertiwi Assistant..."
    }
  ]
}
```

**Parameters**:
- `message` (string, required): User's message
- `session_id` (string, optional): Session ID to track conversation. Auto-generated if not provided
- `history` (array, optional): Previous chat messages for context

**Response** (200 OK):
```json
{
  "success": true,
  "message": "SMK Pertiwi Kuningan memiliki 4 jurusan...",
  "timestamp": "2024-02-07T12:00:00.000000",
  "session_id": "session_1707329000_abc123xyz",
  "history": [
    {
      "role": "user",
      "message": "Jurusan apa saja di SMK Pertiwi?",
      "timestamp": "2024-02-07T12:00:00.000000"
    },
    {
      "role": "assistant",
      "message": "SMK Pertiwi Kuningan memiliki 4 jurusan...",
      "timestamp": "2024-02-07T12:00:00.000000"
    }
  ]
}
```

---

### 4. Get Session History
**GET** `/api/session/{session_id}`

Retrieve the complete chat history for a specific session.

**Path Parameters**:
- `session_id` (string, required): The session ID

**Response** (200 OK):
```json
{
  "session_id": "session_1707329000_abc123xyz",
  "history": [
    {
      "role": "user",
      "message": "Halo",
      "timestamp": "2024-02-07T12:00:00.000000"
    },
    {
      "role": "assistant",
      "message": "Halo! Saya Pertiwi Assistant...",
      "timestamp": "2024-02-07T12:00:00.000000"
    }
  ],
  "message_count": 2
}
```

**Error Response** (404 Not Found):
```json
{
  "success": false,
  "message": "Session tidak ditemukan",
  "timestamp": "2024-02-07T12:00:00.000000"
}
```

---

### 5. Delete Session
**DELETE** `/api/session/{session_id}`

Delete a chat session.

**Path Parameters**:
- `session_id` (string, required): The session ID

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Session berhasil dihapus"
}
```

**Error Response** (404 Not Found):
```json
{
  "success": false,
  "message": "Session tidak ditemukan",
  "timestamp": "2024-02-07T12:00:00.000000"
}
```

---

## Frontend Integration

### ChatAPI Service

The frontend uses a JavaScript API service (`src/services/api.js`) to communicate with the backend.

**Available Methods**:

```javascript
import ChatAPI from './services/api.js'

// Health check
await ChatAPI.healthCheck()

// Send message
const response = await ChatAPI.sendMessage(
  message,
  sessionId,
  history
)

// Get session history
await ChatAPI.getSessionHistory(sessionId)

// Delete session
await ChatAPI.deleteSession(sessionId)
```

### App Component Structure

The application uses a parent-child component structure:

- **App.vue** (Parent): Manages chat state and API communication
- **ChatWindow.vue** (Child): Displays messages and handles user interactions
- **InputArea.vue** (Helper): Input handling

---

## Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Gemini API
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=1000
TEMPERATURE=0.7

# Server
PORT=8000
FRONTEND_URL=http://localhost:5173

# App
APP_NAME=SMK Pertiwi Chatbot
```

### Frontend Requirements

- Node.js 16+
- npm or yarn

---

## System Information

### Tech Stack

**Backend**:
- FastAPI (Python)
- Google Generative AI (Gemini)
- Uvicorn (ASGI Server)
- Pydantic (Data Validation)

**Frontend**:
- Vue.js 3
- Vite (Build Tool)
- Font Awesome (Icons)

### Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## Troubleshooting

### Backend won't start

1. Check GEMINI_API_KEY is set in `.env`
2. Ensure port 8000 is not in use: `netstat -ano | findstr :8000`
3. Verify Python 3.8+ is installed: `python --version`

### Frontend won't load

1. Ensure port 5174 (or 5173) is free
2. Check npm dependencies: `npm install`
3. Clear cache: `npm cache clean --force`

### CORS Errors

Make sure backend has correct CORS origins configured in `backend/app/config.py`:

```python
origins: List[str] = Field(default_factory=lambda: [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
])
```

### API Integration Issues

1. Check backend is running: `curl http://localhost:8000/health`
2. Verify GEMINI_API_KEY is valid
3. Check browser console for CORS errors
4. Ensure frontend is calling correct API URL

---

## API Documentation Tools

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Example Usage

### JavaScript/Vue.js

```javascript
import ChatAPI from './services/api.js'

// Send message
try {
  const response = await ChatAPI.sendMessage(
    'Apa itu SMK Pertiwi?',
    null,  // sessionId
    null   // history
  )
  
  console.log('Response:', response.message)
  console.log('Session:', response.session_id)
} catch (error) {
  console.error('Chat failed:', error)
}
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jurusan apa saja di SMK Pertiwi?",
    "session_id": "session_1707329000_abc123xyz"
  }'

# Get session history
curl http://localhost:8000/api/session/session_1707329000_abc123xyz

# Delete session
curl -X DELETE http://localhost:8000/api/session/session_1707329000_abc123xyz
```

---

## License

© 2024 SMK Pertiwi Kuningan. All rights reserved.
