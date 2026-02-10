# Pertiwi Assistant - Chatbot SMK Pertiwi Kuningan

Chatbot AI full-stack untuk SMK Pertiwi Kuningan yang menggunakan Google Gemini API. Aplikasi yang dipbangun dengan Vue.js 3 (frontend) dan FastAPI (backend) dengan integrasi sempurna dan desain modern.

---

## Fitur Utama

- **Chat AI Cerdas** - Powered by Google Generative AI (Gemini)
- **Interface Modern** - Vue.js 3 dengan Vite build tool
- **Session Management** - Riwayat percakapan yang persisten per sesi
- **Tema Terang/Gelap** - Dark mode support dengan localStorage persistence
- **Typing Indicator** - Animasi saat AI sedang merespon
- **Quick Questions** - Tombol preset untuk pertanyaan umum
- **Mobile Friendly** - Responsive design untuk desktop, tablet, dan mobile
- **Real-time Chat** - Messaging langsung dengan AI
- **CORS Integration** - Frontend-backend integration yang seamless
- **Error Handling** - Graceful error messages dan recovery
- **API Documentation** - Swagger UI dan ReDoc di backend

---

## Mulai Cepat (30 Detik)

### Prerequisite
- Python 3.8+ (dengan pip)
- Node.js 14+ (dengan npm)
- Google Gemini API Key

### 1. Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Buat .env file dengan API key
# backend/.env:
# GEMINI_API_KEY=your_api_key_here

# Jalankan backend
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2. Setup Frontend (Terminal Baru)

```bash
cd frontend

# Install dependencies
npm install

# Jalankan dev server
npm run dev
```

**Expected Output:**
```
VITE v5.4.21  ready in 405 ms
 Local:   http://localhost:5174/
```

### 3. Akses Aplikasi

Buka browser ke: **http://localhost:5174** ---

## Struktur Proyek

```
smk-pertiwi-chatbot/
|-- backend/                           # FastAPI Backend
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py                   # Main FastAPI application
|   |   |-- config.py                 # Configuration & environment
|   |   `-- services/
|   |       `-- gemini_service.py     # Gemini AI integration
|   |
|   |-- .env                          # Environment variables (not included)
|   |-- requirements.txt              # Python dependencies
|   `-- __pycache__/
|
|-- frontend/                          # Vue.js Frontend
|   |-- src/
|   |   |-- App.vue                   # Main app component
|   |   |-- main.js                   # App entry point
|   |   |-- services/
|   |   |   `-- api.js                # API wrapper service
|   |   |-- components/
|   |   |   |-- ChatWindow.vue        # Chat display component
|   |   |   |-- InputArea.vue         # Input component
|   |   |   `-- MessageBubble.vue     # Message bubble component
|   |   |-- assets/                   # Images and static files
|   |   `-- styles/
|   |       `-- main.css              # Global styles
|   |
|   |-- public/
|   |   `-- index.html
|   |
|   |-- package.json                  # Node.js dependencies
|   |-- vite.config.js                # Vite configuration
|   `-- node_modules/
|
|-- API_DOCUMENTATION.md              # Complete API reference
|-- SETUP_GUIDE.md                    # Detailed setup instructions
|-- IMPLEMENTATION_SUMMARY.md         # Implementation details
|-- QUICK_REFERENCE.md                # Quick command reference
|-- README.md                         # This file
`-- .gitignore                        # Git ignore patterns
```
---

## Architecture

### Technology Stack

**Backend:**
- **FastAPI** - Modern, fast Python web framework
- **Uvicorn** - ASGI server
- **Google Generative AI** - Gemini AI integration
- **Pydantic** - Data validation and settings management
- **python-dotenv** - Environment variable management

**Frontend:**
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation build tool
- **Fetch API** - Native HTTP client
- **CSS 3** - Modern styling with variables

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API info page |
| GET | `/health` | Health check |
| POST | `/api/chat` | Send message to AI |
| GET | `/api/session/{id}` | Get chat history |
| DELETE | `/api/session/{id}` | Delete session |

---

## Documentation

Lengkapi pengetahuan Anda dengan dokumentasi berikut:

1. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation and configuration guide
3. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
4. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands and quick tips

---

## Configuration

### Backend .env

Create `backend/.env`:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Optional: Model Configuration
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=1000
TEMPERATURE=0.7

# Optional: Server Configuration
PORT=8000
FRONTEND_URL=http://localhost:5173
APP_NAME=SMK Pertiwi Chatbot
```

### Frontend Environment

Frontend automatically configured to connect to backend on `http://localhost:8000`

---

## Deploy ke Render

Saya tambahkan `render.yaml` di root project supaya kamu bisa deploy cepat (backend + frontend).

Langkah singkat:
1. Buat Blueprint baru di Render dan pilih repo ini.
2. Render akan membaca `render.yaml` dan membuat 2 service: backend + frontend.
3. Atur env vars wajib di dashboard Render untuk backend.

Env vars backend:
1. `GEMINI_API_KEY`
2. `ADMIN_KEY` (jika pakai admin panel)
3. `SERPAPI_API_KEY` (jika web search diaktifkan)
4. Update `CORS_ORIGINS` ke domain frontend Render kamu.

Env vars frontend:
1. Update `VITE_API_URL` ke URL backend Render kamu.

Catatan:
1. Backend sudah bind ke `$PORT` sesuai kebutuhan Render.
2. Jika kamu tidak memakai web search, ubah `ENABLE_WEB_SEARCH` menjadi `false`.

---

## Testing API

### Health Check
```bash
# Via curl
curl http://localhost:8000/health

# Via browser
http://localhost:8000/health
```

### Interactive API Docs
```
http://localhost:8000/docs           # Swagger UI
http://localhost:8000/redoc          # ReDoc
```

### Send Message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Jurusan apa saja di SMK Pertiwi?"}'
```

---

## Component System

### App.vue (Parent Component)
- State management
- API communication
- Session management
- Message history
- Error handling

### ChatWindow.vue (Child Component)
- Message display
- User interface
- Quick actions
- Theme toggle
- Auto-scroll

### API Service (api.js)
- HTTP wrapper
- Error handling
- Request/response mapping
- Base URL configuration

---

## Features in Detail

### Session Management
Each conversation is assigned a unique `session_id` which allows:
- Persistent chat history
- Multi-session support
- Session cleanup
- Conversation context

### Theme System
- Light Mode (default)
- Dark Mode
- LocalStorage persistence
- Smooth transitions

### Error Handling
- Network error recovery
- Graceful error messages
- Validation errors
- Timeout handling

### Message Formatting
- User/AI differentiation
- Timestamps
- Markdown support ready
- Code block support ready

---

## Browser Support

- Chrome/Chromium (v90+)
- Firefox (v88+)
- Safari (v14+)
- Edge (v90+)
- Mobile browsers

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Change port in .env
PORT=3000

# Or kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**GEMINI_API_KEY not found:**
- Create `backend/.env` file
- Add your Gemini API key
- Restart backend

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Port in use:**
```bash
# Vite will auto-increment port (5174, 5175, etc)
```

**Dependencies error:**
```bash
npm cache clean --force
npm install
```

**Build error:**
```bash
npm run build
npm run preview
```

### CORS Errors

**Error:** `No 'Access-Control-Allow-Origin' header`

**Solution:**
- Check `backend/app/config.py` has frontend URL in `origins`
- Restart backend server

---

## API Usage Examples

### JavaScript/Vue
```javascript
import ChatAPI from './services/api.js'

// Send message
const response = await ChatAPI.sendMessage('Hello')
console.log(response.message)

// Get history
const history = await ChatAPI.getSessionHistory(sessionId)

// Delete session
await ChatAPI.deleteSession(sessionId)
```

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'Hello'}
)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## Learning Resources

- [Vue.js Documentation](https://vuejs.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vite Documentation](https://vitejs.dev/)
- [Google Generative AI](https://ai.google.dev/)

---

## Security Notes

1. **API Key Management** - Never commit `.env` file
   - Use environment variables in production
   - Rotate keys regularly

2. **CORS Configuration** - Only allow trusted origins
   - Update for production domains

3. **Session Management** - Use database in production
   - Implement session expiration
   - Add rate limiting

---

## Performance Tips

1. Response time optimizations
2. Message history limiting (50 per session)
3. Chunk large conversations
4. Use appropriate temperature settings
5. Monitor API usage

---

## Deployment

### Backend (Production)
```bash
# Using gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Using uvicorn with workers
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Frontend (Production)
```bash
# Build
npm run build

# Output in: dist/ folder
# Serve with any HTTP server
```

---

## Development Workflow

1. **Backend Changes** - Edit `backend/app/main.py` or services
   - Auto-reload enabled with `--reload` flag
   - Test with `/docs` endpoint

2. **Frontend Changes** - Edit `.vue` or `.js` files
   - Vite provide hot module replacement
   - Changes reflect immediately

3. **Component Testing** - Use browser DevTools (F12)
   - Check Network tab for API calls
   - Inspect Vue component tree

---

## Contributing

To contribute to this project:

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## License

 2024 SMK Pertiwi Kuningan. All rights reserved.

---

## Support

For issues or questions:

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
4. Check browser console for errors (F12)
5. Check backend logs in terminal

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Google Gemini API key obtained
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] `.env` file created with API key
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5174
- [ ] Able to send messages in chat
- [ ] Responses from AI appearing

---

## Project Status

 **Complete** All components fully implemented and tested:
- API Service 
- Components 
- Backend Endpoints 
- Error Handling 
- Documentation
---

## Next Steps

1. Open http://localhost:5174 in your browser
2. Try sending a message
3. Test different features
4. Explore API documentation at /docs
5. Customize for your needs

---

## Quick Links

- [Frontend](http://localhost:5174)
- [Backend](http://localhost:8000)
- [API Docs](http://localhost:8000/docs)
- [Configuration](backend/.env)

---

**Version**: 1.0.0
**Last Updated**: February 7, 2026
**Status**:  Production Ready

---

Made with  for SMK Pertiwi Kuningan
