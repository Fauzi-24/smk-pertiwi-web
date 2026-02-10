# Setup & Configuration Guide - SMK Pertiwi Chatbot

## ✅ Checklist Status

- [x] API Service Created (`frontend/src/services/api.js`)
- [x] App Component Updated (Parent state management)
- [x] ChatWindow Component Updated (Message display & UI)
- [x] InputArea Components Integrated
- [x] Backend Endpoints Verified
- [x] CORS Middleware Configured
- [x] Session Management Implemented
- [x] Error Handling Added
- [x] API Documentation Generated

---

## Project Structure

```
smk-pertiwi-chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application & endpoints
│   │   ├── config.py               # Configuration settings
│   │   └── services/
│   │       └── gemini_service.py   # Gemini AI integration
│   ├── .env                        # Environment variables
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.vue                 # Main app (parent component)
│   │   ├── main.js                 # Vue app entry point
│   │   ├── services/
│   │   │   └── api.js              # API communication service
│   │   ├── components/
│   │   │   ├── ChatWindow.vue      # Chat display & controls
│   │   │   ├── InputArea.vue       # Message input (optional)
│   │   │   └── MassageBubble.vue   # Message bubble component
│   │   └── styles/
│   │       └── main.css
│   ├── package.json                # Node dependencies
│   └── vite.config.js              # Vite configuration
│
├── API_DOCUMENTATION.md            # Complete API reference
├── SETUP_GUIDE.md                  # This file
└── README.md                        # Project overview
```

---

## Installation Steps

### Step 1: Backend Setup

**1.1 Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- `fastapi>=0.104.1` - Web framework
- `uvicorn[standard]>=0.24.0` - ASGI server
- `google-generativeai>=0.3.0` - Gemini AI integration
- `python-dotenv>=1.0.0` - Environment variable management
- `pydantic-settings>=2.0.0` - Configuration management

**1.2 Configure Environment Variables**

Create `backend/.env`:

```env
# Required: Your Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Optional: API Configuration
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=1000
TEMPERATURE=0.7

# Server Configuration
PORT=8000
FRONTEND_URL=http://localhost:5173

# Application
APP_NAME=SMK Pertiwi Chatbot
```

**1.3 Start Backend Server**

```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend is running at**: `http://localhost:8000`

---

### Step 2: Frontend Setup

**2.1 Install Dependencies**

```bash
cd frontend
npm install
```

This installs:
- `vue@^3.3.4` - UI framework
- `vite@^5.0.0` - Build tool
- `@vitejs/plugin-vue@^4.6.2` - Vue plugin for Vite

**2.2 Start Development Server**

```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.4.21  ready in 405 ms

  ➜  Local:   http://localhost:5174/
  ➜  Network: use --host to expose
```

✅ **Frontend is running at**: `http://localhost:5174` (or 5173)

---

## API Testing

### Method 1: Browser Health Check

Open `http://localhost:8000/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "app_name": "SMK Pertiwi Chatbot",
  "version": "1.0.0",
  "timestamp": "2026-02-07T21:55:02.411973"
}
```

### Method 2: Swagger UI Documentation

Open `http://localhost:8000/docs`

This provides an interactive interface to:
- Test all API endpoints
- View request/response schemas
- Understand parameter requirements

### Method 3: ReDoc Documentation

Open `http://localhost:8000/redoc`

Alternative API documentation view with detailed descriptions.

### Method 4: Using the Frontend

1. Open `http://localhost:5174` in your browser
2. Type a message in the input field
3. Click send or press Enter
4. The frontend will communicate with the backend

---

## Code Architecture

### Frontend Data Flow

```
User Input
    ↓
ChatWindow Component
    ↓
emit('send-message', userMessage)
    ↓
App.vue Component
    ↓
ChatAPI.sendMessage()
    ↓
POST /api/chat
    ↓
Backend Response
    ↓
Add to messages array
    ↓
ChatWindow displays message
```

### Backend Architecture

```
POST /api/chat
    ↓
ChatRequest Validation (Pydantic)
    ↓
Create/Get Session ID
    ↓
Gemini AI Service
    ↓
Get Response from AI
    ↓
Store in Session History
    ↓
Return ChatResponse
```

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API Info Page |
| GET | `/health` | Health Check |
| POST | `/api/chat` | Send Message |
| GET | `/api/session/{session_id}` | Get History |
| DELETE | `/api/session/{session_id}` | Delete Session |

---

## Configuration Files

### backend/app/config.py

```python
class Settings(BaseSettings):
    # API Configuration
    gemini_api_key: Optional[SecretStr]
    gemini_model: str = "gemini-1.5-flash"
    max_tokens: int = 1000
    temperature: float = 0.7

    # Server Configuration
    port: int = 8000
    frontend_url: str = "http://localhost:5173"
    app_name: str = "SMK Pertiwi Chatbot"

    # CORS Origins
    origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
    ]
```

### frontend/vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
```

### frontend/package.json

```json
{
  "name": "frontend",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.6.2",
    "vite": "^5.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## Frontend Services

### ChatAPI Service (`src/services/api.js`)

The API service provides methods to communicate with the backend:

```javascript
import ChatAPI from './services/api.js'

// Health check
await ChatAPI.healthCheck()

// Send message to AI
const response = await ChatAPI.sendMessage(
  'Your message',
  sessionId,      // Optional
  chatHistory     // Optional
)

// Get chat history
await ChatAPI.getSessionHistory(sessionId)

// Delete chat session
await ChatAPI.deleteSession(sessionId)
```

---

## Component Structure

### App.vue (Parent Component)

**Responsibility**: State management and API coordination

**Data**:
- `messages` - Array of chat messages
- `isLoading` - Loading state during API calls
- `sessionId` - Current chat session ID
- `error` - Error messages

**Methods**:
- `initializeApp()` - Check backend health
- `handleSendMessage()` - Process user messages
- `handleClearChat()` - Clear conversation

### ChatWindow.vue (Child Component)

**Responsibility**: Display messages and UI controls

**Props**:
- `messages` - Chat messages array
- `isLoading` - Loading indicator state

**Emits**:
- `send-message` - Send user message to parent
- `clear-chat` - Clear conversation

**Features**:
- Message display with timestamps
- Typing indicator animation
- Quick question buttons
- Theme toggle (light/dark)
- Auto-scroll to latest message

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | Required | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | AI model to use |
| `MAX_TOKENS` | `1000` | Max response length |
| `TEMPERATURE` | `0.7` | Response creativity (0-1) |
| `PORT` | `8000` | Backend server port |
| `FRONTEND_URL` | `http://localhost:5173` | Frontend URL for CORS |
| `APP_NAME` | `SMK Pertiwi Chatbot` | Application name |

---

## Troubleshooting

### Port Already in Use

**Error**: `Address already in use :8000`

**Solution**:
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### GEMINI_API_KEY Not Found

**Error**: `HTTPException: 401 Unauthorized`

**Solution**:
1. Create `backend/.env` file
2. Add your Google Gemini API key
3. Restart backend server

### CORS Errors

**Error**: `No 'Access-Control-Allow-Origin' header`

**Solution**:
- Ensure frontend URL is in `origins` list in `backend/app/config.py`
- Restart backend server

### Frontend Not Loading

**Error**: `ERR_NAME_NOT_RESOLVED`

**Solution**:
```bash
cd frontend
npm cache clean --force
npm install
npm run dev
```

---

## Testing Endpoints

### Using JavaScript Fetch API

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)

// Send message
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Jurusan apa saja di SMK Pertiwi?'
  })
})
  .then(r => r.json())
  .then(console.log)
```

### Using PowerShell

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing | Select-Object -ExpandProperty Content

# Send message
$body = @{
  message = "Jurusan apa saja di SMK Pertiwi?"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/chat" `
  -Method POST `
  -Headers @{'Content-Type'='application/json'} `
  -Body $body `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## Performance Tips

1. **Message History**: Limited to 50 messages per session to optimize memory
2. **Temperature**: Adjust in `.env` (0 = deterministic, 1 = creative)
3. **Max Tokens**: Higher values = longer responses but slower API calls
4. **Caching**: Front-end stores theme preference in localStorage

---

## Browser Compatibility

- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

## Next Steps

1. ✅ Verify both servers are running
2. ✅ Open `http://localhost:5174` in your browser
3. ✅ Test sending a message
4. ✅ Check backend logs for any errors
5. ✅ Explore `/docs` for interactive API documentation

---

## Support

For issues or questions:
1. Check `API_DOCUMENTATION.md`
2. Review backend logs: Check terminal running `uvicorn`
3. Check frontend logs: Open browser DevTools (F12)
4. Verify `.env` file configuration
5. Ensure both servers are running

---

## Version Info

- **Python**: 3.8+
- **Node.js**: 14+
- **Vue.js**: 3.3+
- **Vite**: 5.0+
- **FastAPI**: 0.104+
- **Gemini AI**: Latest

---

Last Updated: February 7, 2026
