# Quick Reference - SMK Pertiwi Chatbot

## Quick Start (30 seconds)

### Terminal 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

### Open Browser
```
http://localhost:5174
```

---

## Common Commands

### Backend Commands

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --port 8000

# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Check health
curl http://localhost:8000/health
```

### Frontend Commands

```bash
# Install dependencies
cd frontend
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Clear node modules and reinstall
npm cache clean --force
rm -r node_modules package-lock.json
npm install
```

---

## Testing Endpoints

### Health Check
```bash
# Using curl
curl http://localhost:8000/health

# Using PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing | Select-Object -ExpandProperty Content

# In browser
http://localhost:8000/health
```

### Send Message
```bash
# Using curl (Windows)
curl -X POST http://localhost:8000/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Halo\"}"

# Using curl (Linux/Mac)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo"}'

# Using PowerShell
$body = @{ message = "Halo" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/chat" `
  -Method POST `
  -Headers @{'Content-Type'='application/json'} `
  -Body $body `
  -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Get Session History
```bash
curl http://localhost:8000/api/session/<SESSION_ID>
```

### Delete Session
```bash
curl -X DELETE http://localhost:8000/api/session/<SESSION_ID>
```

---

## API URLs

| Purpose | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend | http://localhost:8000 |
| Health Check | http://localhost:8000/health |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| API Info Page | http://localhost:8000/ |

---

## File Locations

### Configuration Files
- Backend config: `backend/app/config.py`
- Backend env: `backend/.env`
- Frontend config: `frontend/vite.config.js`
- Dependencies (backend): `backend/requirements.txt`
- Dependencies (frontend): `frontend/package.json`

### Source Code
- Backend main: `backend/app/main.py`
- Gemini service: `backend/app/services/gemini_service.py`
- Frontend app: `frontend/src/App.vue`
- Chat component: `frontend/src/components/ChatWindow.vue`
- API service: `frontend/src/services/api.js`

### Documentation
- API Docs: `API_DOCUMENTATION.md`
- Setup Guide: `SETUP_GUIDE.md`
- Implementation: `IMPLEMENTATION_SUMMARY.md`
- This file: `QUICK_REFERENCE.md`

---

## Environment Setup

### Setting .env Variables (Windows)
```powershell
# Create .env file
"GEMINI_API_KEY=your_key_here" | Set-Content backend\.env

# View .env
Get-Content backend\.env

# Edit with text editor
notepad backend\.env
```

### Setting .env Variables (Linux/Mac)
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > backend/.env

# View .env
cat backend/.env

# Edit with text editor
nano backend/.env
```

---

## Ports & Services

| Service | Port | Status Check |
|---------|------|--------------|
| Backend API | 8000 | `curl localhost:8000/health` |
| Frontend Dev | 5173-5174 | Open http://localhost:5174 |

### Change Ports

**Backend** (backend/.env):
```env
PORT=3000
```

**Frontend** (frontend/vite.config.js):
```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000
  }
})
```

---

## JavaScript/Vue Snippets

### Using ChatAPI Service
```javascript
import ChatAPI from './services/api.js'

// Health check
const health = await ChatAPI.healthCheck()

// Send message
const response = await ChatAPI.sendMessage('Hi', null, null)
console.log(response.message)

// Get history
const history = await ChatAPI.getSessionHistory(sessionId)

// Delete session
await ChatAPI.deleteSession(sessionId)
```

### Using in Vue Component
```vue
<script>
import ChatAPI from './services/api.js'

export default {
  methods: {
    async sendChat() {
      try {
        const res = await ChatAPI.sendMessage(this.message)
        this.response = res.message
      } catch (err) {
        console.error(err)
      }
    }
  }
}
</script>
```

---

## Troubleshooting

### Backend won't start
```bash
# Check port in use
netstat -ano | findstr :8000

# Kill process on Windows
taskkill /PID <PID_NUMBER> /F

# Kill process on Linux/Mac
kill <PID_NUMBER>

# Try different port
python -m uvicorn app.main:app --port 3000
```

### Frontend won't start
```bash
# Clear cache
npm cache clean --force

# Reinstall
cd frontend
rm -r node_modules package-lock.json
npm install
npm run dev
```

### API connection error
```
❌ Backend not responding

Check:
1. Backend is running: curl http://localhost:8000/health
2. Port not blocked: netstat -ano | findstr :8000
3. Firewall settings
4. GEMINI_API_KEY in .env
```

### CORS error
```
❌ No 'Access-Control-Allow-Origin' header

Check backend/app/config.py:
- Frontend URL in origins list
- Restart backend after changes
```

---

## Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Vue.js Docs**: https://vuejs.org/
- **Vite Docs**: https://vitejs.dev/
- **Gemini API**: https://ai.google.dev/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

## Git Commands

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Full chatbot implementation"

# Ignore node_modules and venv
echo "node_modules/" > .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
```

---

## Development Tips

1. **Frontend Hot Reload**: Changes auto-refresh in browser
2. **Backend Hot Reload**: Use `--reload` flag with uvicorn
3. **Browser DevTools**: F12 to debug frontend
4. **Backend Logs**: Terminal shows all API requests
5. **API Testing**: Visit http://localhost:8000/docs for interactive testing

---

## Production Deployment

### Backend
```bash
# Production server
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Or with uvicorn workers
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Build
npm run build

# Output in: frontend/dist/

# Serve with any HTTP server
python -m http.server 3000 --directory dist
```

---

## Performance Checklist

- [ ] API response time < 2 seconds
- [ ] Frontend loads in < 3 seconds
- [ ] No console errors
- [ ] All images optimized
- [ ] CSS minified
- [ ] JavaScript bundled

---

## Version Info

```bash
# Check Python version
python --version

# Check pip packages
pip list

# Check Node version
node --version

# Check npm version
npm --version

# Check Vue version
npm list vue
```

---

## Emergency Commands

### Stop All Services
```bash
# Stop backend (Ctrl+C in terminal)
# Stop frontend (Ctrl+C in terminal)
```

### Reset Everything
```bash
# Backend
cd backend
rm -r __pycache__ .venv
pip install -r requirements.txt

# Frontend
cd frontend
rm -r node_modules dist
npm install
```

### Test Everything
```bash
# 1. Backend health
curl http://localhost:8000/health

# 2. Frontend
open http://localhost:5174

# 3. Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'
```

---

## Quick Status Check

```bash
# Create check.sh (Linux/Mac)
#!/bin/bash
echo "🔍 Checking SMK Pertiwi Chatbot..."
echo ""
echo "Backend Health:"
curl -s http://localhost:8000/health | json_pp
echo ""
echo "Frontend Status:"
curl -s http://localhost:5174 > /dev/null && echo "✅ Running" || echo "❌ Not running"
echo ""
echo "✅ All checks passed!"
```

---

## Common Errors & Fixes

```
Error: "Cannot find module 'vue'"
Fix: npm install vue

Error: "GEMINI_API_KEY not found"
Fix: Check backend/.env file exists with valid key

Error: "Address already in use :8000"
Fix: Kill process on port 8000

Error: "CORS error"
Fix: Restart backend after config restart

Error: "Module not found: 'uvicorn'"
Fix: pip install uvicorn

Error: "Cannot GET /health"
Fix: Backend not running - check port 8000
```

---

## Last Updated
February 7, 2026

## Quick Navigation
- [Setup Guide](SETUP_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
