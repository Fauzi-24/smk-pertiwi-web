# 🎓 SMK Pertiwi Kuningan - Website Resmi

Website modern untuk SMK Pertiwi Kuningan dengan AI Chatbot "Prism" menggunakan Google Gemini AI.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Vue 3](https://img.shields.io/badge/Vue.js-3.x-4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)

## ✨ Features

### 🤖 AI Chatbot "Prism"
- Powered by Google Gemini 2.5 Flash
- Streaming responses
- Context-aware conversations
- Support PDF & image attachments
- Indonesian language optimized

### 📱 PWA Support
- Install to home screen
- Offline capability
- Service worker caching
- Custom app icon & theme

### 🎨 Modern UI/UX
- Glassmorphism effects
- Smooth page transitions
- Dark mode support
- Responsive design
- Loading skeletons

### 📊 User Features
- **Gallery**: Photo showcase dengan category filters & lightbox
- **PPDB Online**: 4-step registration wizard
- **Social Sharing**: Facebook, Twitter, WhatsApp, Copy Link
- **WhatsApp Integration**: Floating contact button
- **7 Jurusan**: RPL, TKJ, TKR, TSM, TO, LP, BDP

### 🔍 SEO Optimized
- Meta tags (Open Graph, Twitter Card)
- Sitemap.xml
- Robots.txt
- Canonical URLs
- Rich social previews

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ dan npm
- **Python** 3.9+
- **Google Gemini API Key** ([Get here](https://makersuite.google.com/app/apikey))

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/smk-pertiwi-chatbot.git
cd smk-pertiwi-chatbot
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
COR S_ORIGINS=http://localhost:5173
```

Start server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit: `http://localhost:5173`

---

## 📂 Project Structure

```
smk-pertiwi-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── routers/             # API endpoints
│   │   │   ├── chat.py          # Chat API
│   │   │   └── ppdb.py          # PPDB API
│   │   ├── services/
│   │   │   └── gemini_service.py # Gemini AI integration
│   │   └── models/              # Database models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.vue   # Main chat interface
│   │   │   ├── LazyImage.vue    # Lazy loading images
│   │   │   ├── ShareButtons.vue # Social  sharing
│   │   │   ├── SkeletonCard.vue # Loading states
│   │   │   └── VoiceInput.vue   # Speech-to-text
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Galeri.vue       # Photo gallery
│   │   │   ├── PPDBForm.vue     # Registration form
│   │   │   └── ...
│   │   ├── data/
│   │   │   ├── schoolData.js    # School info
│   │   │   └── galleryData.js   # Gallery items
│   │   └── router/index.js
│   ├── public/
│   │   ├── manifest.json        # PWA manifest
│   │   ├── service-worker.js    # Offline support
│   │   ├── sitemap.xml          # SEO sitemap
│   │   └── robots.txt
│   └── package.json
│
└── README.md
```

---

## 🛠️ Development

### Build for Production
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
pip install -r requirements.txt
```

### Environment Variables

**Backend (.env):**
```env
GEMINI_API_KEY=your_api_key
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

**Frontend:**
Hard-coded API URL in `src/services/api.js`:
```javascript
const API_URL = import.meta.env.DEV 
  ? 'http://localhost:8000' 
  : 'https://api.yourdomain.com'
```

---

## 🌐 Deployment

### Frontend (Vercel - Recommended)
1. Push code to GitHub
2. Import project di [Vercel](https://vercel.com)
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Deploy!

Update API URL setelah backend deployed.

### Backend (Railway - Recommended)
1. Push code to GitHub
2. Import project di [Railway](https://railway.app)
3. Add environment variables (GEMINI_API_KEY)
4. Deploy otomatis!

Atau gunakan:
- **Heroku** (backend)
- **Netlify** (frontend)
- **DigitalOcean** (VPS)

---

## 📋 Features Checklist

- [x] PWA installable
- [x] SEO optimized
- [x] AI Chatbot with Gemini
- [x] Gallery with lightbox
- [x] PPDB Online form
- [x] Social sharing
- [x] WhatsApp integration
- [x] Page transitions
- [x] Loading states
- [x] Responsive design
- [ ] Voice input integrated (component ready)
- [ ] Event calendar (optional)
- [ ] Alumni section (optional)

---

## 🎯 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue.js 3, Vue Router, Vite |
| Backend | FastAPI, Uvicorn |
| AI | Google Gemini 2.5 Flash |
| Styling | Vanilla CSS, Glassmorphism |
| Icons | Font Awesome 6 |
| PWA | Service Worker, Manifest |

---

## 📸 Screenshots

```
TODO: Add screenshots of:
- Homepage
- AI Chat interface
- Gallery page
- PPDB form
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Developer

**Fathurrachman Fauzi**
- Website: [smkpertiwi.sch.id](https://smkpertiwi.sch.id)
- Email: info@smkpertiwi.sch.id

---

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language model
- **Vue.js Team** for amazing framework
- **FastAPI** for modern Python API
- **SMK Pertiwi Kuningan** for opportunity

---

## 📞 Support

Need help? Contact us:
- 📧 Email: info@smkpertiwi.sch.id
- 📱 WhatsApp: [Click here](https://wa.me/628123456789)
- 💬 AI Chat: Built-in on website!

---

**Made with ❤️ by Fathurrachman Fauzi**
