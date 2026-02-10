from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import uvicorn
from datetime import datetime
import json
import os
import time
import hashlib
import re
import csv
import io

from .config import settings
from .services.gemini_service import chatbot

# Model data
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List] = None
    memory: Optional[List[str]] = None
    conversation_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    correction: str
    source: Optional[str] = None
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    session_id: Optional[str] = None
    history: Optional[List] = None
    source: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    timestamp: str

# Inisialisasi FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Chatbot AI untuk SMK Pertiwi Kuningan",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat sessions (in production, use database)
chat_sessions = {}
file_contexts = {}
file_contexts_by_convo = {}
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEEDBACK_QUEUE_PATH = os.path.join(APP_DIR, "data", "feedback_queue.json")
FEEDBACK_APPROVED_PATH = os.path.join(APP_DIR, "data", "feedback_approved.json")
FILE_CONTEXTS_PATH = os.path.join(APP_DIR, "data", "file_contexts.json")
MAX_UPLOAD_BYTES = 4 * 1024 * 1024
MAX_FILE_CONTEXT_CHARS = 6000
FILE_CONTEXT_LIMIT = 5

rate_limits = {}

def _load_file_contexts():
    if not os.path.exists(FILE_CONTEXTS_PATH):
        return {}, {}
    try:
        with open(FILE_CONTEXTS_PATH, "r", encoding="utf-8") as file:
            payload = json.load(file)
        by_session = payload.get("by_session", {}) if isinstance(payload, dict) else {}
        by_convo = payload.get("by_conversation", {}) if isinstance(payload, dict) else {}
        return by_session, by_convo
    except Exception:
        return {}, {}

def _save_file_contexts():
    try:
        os.makedirs(os.path.dirname(FILE_CONTEXTS_PATH), exist_ok=True)
        payload = {
            "by_session": file_contexts,
            "by_conversation": file_contexts_by_convo
        }
        with open(FILE_CONTEXTS_PATH, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
    except Exception:
        pass

file_contexts, file_contexts_by_convo = _load_file_contexts()
ADMIN_AUDIT_LOG_PATH = os.path.join(APP_DIR, "data", "admin_audit_log.json")

def _load_json_list(path: str):
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def _save_json_list(path: str, items: list):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _require_admin(request: Request):
    admin_key = settings.admin_key.get_secret_value() if settings.admin_key else None
    if not admin_key:
        return
    header_key = request.headers.get("x-admin-key")
    if header_key != admin_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

def _check_rate_limit(request: Request):
    if not request:
        return
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = getattr(settings, "rate_limit_window", 60)
    limit = getattr(settings, "rate_limit_per_min", 30)
    min_interval = getattr(settings, "min_request_interval", 1.2)

    entries = rate_limits.get(ip, [])
    entries = [ts for ts in entries if now - ts < window]
    if entries and (now - entries[-1]) < min_interval:
        raise HTTPException(status_code=429, detail="Terlalu cepat. Tunggu sebentar lalu coba lagi.")
    if len(entries) >= limit:
        raise HTTPException(status_code=429, detail="Terlalu banyak permintaan. Coba lagi nanti.")
    entries.append(now)
    rate_limits[ip] = entries

def _normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", (text or "").lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def _load_blocklist():
    raw = getattr(settings, "moderation_blocklist", None) or ""
    if not raw:
        raw = os.getenv("MODERATION_BLOCKLIST", "")
    if not raw:
        return []
    parts = re.split(r"[,\n;|]+", raw)
    return [part.strip().lower() for part in parts if part.strip()]

def _is_blocked_message(text: str) -> bool:
    if not getattr(settings, "moderation_enabled", True):
        return False
    normalized = _normalize_text(text)
    if not normalized:
        return False
    blocklist = _load_blocklist()
    for term in blocklist:
        if " " in term:
            if term in normalized:
                return True
        else:
            if re.search(rf"\b{re.escape(term)}\b", normalized):
                return True
    return False

def _list_file_entries(session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    items = []
    if session_id:
        items = file_contexts.get(session_id) or []
    if not items and conversation_id:
        items = file_contexts_by_convo.get(conversation_id) or []
    output = []
    for item in items:
        content = item.get("content") or ""
        summary = item.get("summary")
        if not summary and content:
            summary = content[:240].rstrip() + ("..." if len(content) > 240 else "")
        output.append({
            "id": item.get("id"),
            "filename": item.get("filename"),
            "content_type": item.get("content_type"),
            "summary": summary or "",
            "created_at": item.get("created_at")
        })
    return output

def _remove_file_entry(file_id: str, session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    removed = False
    if session_id and session_id in file_contexts:
        before = len(file_contexts[session_id])
        file_contexts[session_id] = [item for item in file_contexts[session_id] if item.get("id") != file_id]
        removed = removed or (len(file_contexts[session_id]) != before)
        if not file_contexts[session_id]:
            file_contexts.pop(session_id, None)

    if conversation_id and conversation_id in file_contexts_by_convo:
        before = len(file_contexts_by_convo[conversation_id])
        file_contexts_by_convo[conversation_id] = [item for item in file_contexts_by_convo[conversation_id] if item.get("id") != file_id]
        removed = removed or (len(file_contexts_by_convo[conversation_id]) != before)
        if not file_contexts_by_convo[conversation_id]:
            file_contexts_by_convo.pop(conversation_id, None)

    if not session_id and not conversation_id:
        for key in list(file_contexts.keys()):
            before = len(file_contexts[key])
            file_contexts[key] = [item for item in file_contexts[key] if item.get("id") != file_id]
            if len(file_contexts[key]) != before:
                removed = True
            if not file_contexts[key]:
                file_contexts.pop(key, None)
        for key in list(file_contexts_by_convo.keys()):
            before = len(file_contexts_by_convo[key])
            file_contexts_by_convo[key] = [item for item in file_contexts_by_convo[key] if item.get("id") != file_id]
            if len(file_contexts_by_convo[key]) != before:
                removed = True
            if not file_contexts_by_convo[key]:
                file_contexts_by_convo.pop(key, None)

    if removed:
        _save_file_contexts()
    return removed

def _clear_files(conversation_id: Optional[str] = None, session_id: Optional[str] = None):
    removed = False
    if session_id and session_id in file_contexts:
        file_contexts.pop(session_id, None)
        removed = True
    if conversation_id and conversation_id in file_contexts_by_convo:
        file_contexts_by_convo.pop(conversation_id, None)
        removed = True
    if removed:
        _save_file_contexts()
    return removed

def _get_file_context_text(session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    items = []
    if session_id:
        items = file_contexts.get(session_id) or []
    if not items and conversation_id:
        items = file_contexts_by_convo.get(conversation_id) or []
    if not items:
        return None
    parts = []
    for item in items[-FILE_CONTEXT_LIMIT:]:
        title = item.get("filename") or "Dokumen"
        content = item.get("content") or ""
        if content:
            parts.append(f"[{title}]\n{content}")
    return "\n\n".join(parts) if parts else None

def _admin_fingerprint(request: Request):
    header_key = request.headers.get("x-admin-key") if request else None
    if not header_key:
        return "public"
    return hashlib.sha256(header_key.encode("utf-8")).hexdigest()[:12]

def _log_admin_action(action: str, feedback_id: str, request: Request, item: dict | None = None):
    entry = {
        "id": uuid4().hex,
        "action": action,
        "feedback_id": feedback_id,
        "admin_id": _admin_fingerprint(request),
        "timestamp": datetime.now().isoformat(),
        "ip": request.client.host if request and request.client else None
    }
    if item:
        entry["question"] = item.get("question")
        entry["conversation_id"] = item.get("conversation_id")
        entry["session_id"] = item.get("session_id")
    logs = _load_json_list(ADMIN_AUDIT_LOG_PATH)
    logs.append(entry)
    _save_json_list(ADMIN_AUDIT_LOG_PATH, logs)

def _csv_response(filename: str, rows: list, fieldnames: list):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, "") for key in fieldnames})
    output.seek(0)
    response = StreamingResponse(output, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

@app.get("/", response_class=HTMLResponse)
async def root():
    """Halaman utama API"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.app_name}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #E3F2FD;
                color: #333;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(33, 150, 243, 0.1);
            }}
            h1 {{
                color: #2196F3;
                border-bottom: 3px solid #2196F3;
                padding-bottom: 10px;
            }}
            .endpoint {{
                background: #F5F5F5;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #2196F3;
            }}
            code {{
                background: #E3F2FD;
                padding: 2px 6px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 {settings.app_name} API</h1>
            <p>Selamat datang di API Chatbot SMK Pertiwi Kuningan.</p>
            
            <h2>📡 Endpoints</h2>
            
            <div class="endpoint">
                <strong>GET</strong> <code>/health</code><br>
                Cek status server
            </div>
            
            <div class="endpoint">
                <strong>POST</strong> <code>/api/chat</code><br>
                Kirim pesan ke chatbot
            </div>
            
            <div class="endpoint">
                <strong>GET</strong> <code>/api/session/{'{session_id}'}</code><br>
                Dapatkan riwayat chat
            </div>
            
            <div class="endpoint">
                <strong>DELETE</strong> <code>/api/session/{'{session_id}'}</code><br>
                Hapus sesi chat
            </div>
            
            <h2>📚 Dokumentasi</h2>
            <p>
                <a href="/docs">Swagger UI</a> | 
                <a href="/redoc">ReDoc</a>
            </p>
            
            <h2>🏫 Tentang</h2>
            <p>API ini menggunakan Gemini AI untuk membantu komunitas SMK Pertiwi Kuningan.</p>
            <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
                © 2024 SMK Pertiwi Kuningan. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint untuk mengecek kesehatan server"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(payload: ChatRequest, request: Request):
    """Endpoint utama untuk chat dengan AI"""
    try:
        _check_rate_limit(request)
        # Validasi input
        if not payload.message.strip():
            raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")

        if _is_blocked_message(payload.message):
            return {
                "success": True,
                "message": "Maaf, saya tidak bisa membantu dengan bahasa tersebut. Silakan gunakan bahasa yang sopan.",
                "timestamp": datetime.now().isoformat(),
                "session_id": payload.session_id,
                "history": [],
                "source": "moderation"
            }
        
        # Gunakan session_id atau buat baru
        session_id = payload.session_id or f"session_{datetime.now().timestamp()}"
        
        # Dapatkan atau inisialisasi riwayat sesi
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Dapatkan respons dari chatbot
        history_for_context = payload.history or chat_sessions.get(session_id, [])
        file_context_text = _get_file_context_text(session_id, payload.conversation_id)

        if history_for_context or payload.memory:
            result = chatbot.get_response_with_history(
                payload.message,
                history_for_context,
                payload.memory,
                file_context=file_context_text
            )
        else:
            result = chatbot.get_response(payload.message, file_context=file_context_text)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        
        # Update riwayat sesi
        chat_sessions[session_id].append({
            "role": "user",
            "message": payload.message,
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id].append({
            "role": "assistant",
            "message": result["message"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Batasi riwayat maksimal 50 pesan per sesi
        if len(chat_sessions[session_id]) > 50:
            chat_sessions[session_id] = chat_sessions[session_id][-50:]
        
        return {
            "success": True,
            "message": result["message"],
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "history": chat_sessions[session_id][-10:] if len(chat_sessions[session_id]) > 10 else chat_sessions[session_id],
            "source": result.get("source")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/session/{session_id}")
async def get_session_history(session_id: str):
    """Dapatkan riwayat chat berdasarkan session_id"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session tidak ditemukan")
    
    return {
        "session_id": session_id,
        "history": chat_sessions[session_id],
        "message_count": len(chat_sessions[session_id])
    }

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Hapus sesi chat"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        file_contexts.pop(session_id, None)
        _save_file_contexts()
        return {"success": True, "message": "Session berhasil dihapus"}
    
    raise HTTPException(status_code=404, detail="Session tidak ditemukan")

@app.get("/api/rag")
async def get_rag_data():
    """Ambil data RAG sekolah yang dihasilkan dari schoolData.js"""
    rag_path = chatbot.rag_path
    if not rag_path or not os.path.exists(rag_path):
        raise HTTPException(status_code=404, detail="RAG data tidak ditemukan")

    try:
        with open(rag_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membaca RAG: {str(e)}")

@app.post("/api/feedback")
async def submit_feedback(payload: FeedbackRequest, request: Request):
    _check_rate_limit(request)
    if not payload.correction or not payload.correction.strip():
        raise HTTPException(status_code=400, detail="Koreksi tidak boleh kosong")

    entry = {
        "id": uuid4().hex,
        "question": payload.question,
        "answer": payload.answer,
        "correction": payload.correction.strip(),
        "source": payload.source,
        "session_id": payload.session_id,
        "conversation_id": payload.conversation_id,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    queue = _load_json_list(FEEDBACK_QUEUE_PATH)
    queue.append(entry)
    _save_json_list(FEEDBACK_QUEUE_PATH, queue)
    return {"success": True, "message": "Masukan diterima dan akan direview admin."}

@app.get("/api/admin/feedback")
async def list_feedback(request: Request):
    _require_admin(request)
    queue = _load_json_list(FEEDBACK_QUEUE_PATH)
    return {"success": True, "items": queue}

@app.post("/api/admin/feedback/{feedback_id}/approve")
async def approve_feedback(feedback_id: str, request: Request):
    _require_admin(request)
    queue = _load_json_list(FEEDBACK_QUEUE_PATH)
    approved = _load_json_list(FEEDBACK_APPROVED_PATH)

    item = next((entry for entry in queue if entry.get("id") == feedback_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan")

    queue = [entry for entry in queue if entry.get("id") != feedback_id]
    item["status"] = "approved"
    item["approved_at"] = datetime.now().isoformat()
    approved.append(item)
    _save_json_list(FEEDBACK_QUEUE_PATH, queue)
    _save_json_list(FEEDBACK_APPROVED_PATH, approved)
    _log_admin_action("approve", feedback_id, request, item)
    chatbot._refresh_school_data()
    return {"success": True, "message": "Feedback disetujui."}

@app.post("/api/admin/feedback/{feedback_id}/reject")
async def reject_feedback(feedback_id: str, request: Request):
    _require_admin(request)
    queue = _load_json_list(FEEDBACK_QUEUE_PATH)
    item = next((entry for entry in queue if entry.get("id") == feedback_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan")
    queue = [entry for entry in queue if entry.get("id") != feedback_id]
    _save_json_list(FEEDBACK_QUEUE_PATH, queue)
    _log_admin_action("reject", feedback_id, request, item)
    return {"success": True, "message": "Feedback ditolak."}

@app.get("/api/admin/export")
async def export_admin_data(request: Request, dataset: str = "pending"):
    _require_admin(request)
    dataset = (dataset or "pending").lower()
    if dataset == "pending":
        rows = _load_json_list(FEEDBACK_QUEUE_PATH)
        fields = ["id", "question", "answer", "correction", "source", "session_id", "conversation_id", "status", "created_at"]
        return _csv_response("feedback_pending.csv", rows, fields)
    if dataset == "approved":
        rows = _load_json_list(FEEDBACK_APPROVED_PATH)
        fields = ["id", "question", "answer", "correction", "source", "session_id", "conversation_id", "status", "created_at", "approved_at"]
        return _csv_response("feedback_approved.csv", rows, fields)
    if dataset == "audit":
        rows = _load_json_list(ADMIN_AUDIT_LOG_PATH)
        fields = ["id", "action", "feedback_id", "admin_id", "timestamp", "ip", "question", "conversation_id", "session_id"]
        return _csv_response("admin_audit_log.csv", rows, fields)
    raise HTTPException(status_code=400, detail="Dataset tidak valid")

@app.post("/api/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    conversation_id: Optional[str] = Form(None)
):
    _check_rate_limit(request)
    if not file:
        raise HTTPException(status_code=400, detail="File tidak ditemukan.")

    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Ukuran file terlalu besar (maks 4MB).")

    filename = file.filename or "dokumen"
    content_type = file.content_type or ""

    text = chatbot.extract_file_context(filename, content_type, data, max_chars=MAX_FILE_CONTEXT_CHARS)
    if not text:
        raise HTTPException(status_code=400, detail="Gagal membaca isi file. Pastikan format PDF/JPG/PNG.")

    if not session_id:
        session_id = f"session_{datetime.now().timestamp()}"

    entry = {
        "id": uuid4().hex,
        "filename": filename,
        "content_type": content_type,
        "content": text,
        "summary": text[:240].rstrip() + ("..." if len(text) > 240 else ""),
        "created_at": datetime.now().isoformat(),
        "conversation_id": conversation_id
    }
    file_contexts.setdefault(session_id, []).append(entry)
    file_contexts[session_id] = file_contexts[session_id][-FILE_CONTEXT_LIMIT:]
    if conversation_id:
        file_contexts_by_convo.setdefault(conversation_id, []).append(entry)
        file_contexts_by_convo[conversation_id] = file_contexts_by_convo[conversation_id][-FILE_CONTEXT_LIMIT:]
    _save_file_contexts()

    summary = text[:240].rstrip() + ("..." if len(text) > 240 else "")

    return {
        "success": True,
        "session_id": session_id,
        "file_id": entry["id"],
        "filename": filename,
        "summary": summary
    }

@app.get("/api/files")
async def list_files(session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    items = _list_file_entries(session_id=session_id, conversation_id=conversation_id)
    return {"success": True, "items": items}

@app.delete("/api/files/{file_id}")
async def delete_file(file_id: str, session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    removed = _remove_file_entry(file_id, session_id=session_id, conversation_id=conversation_id)
    if not removed:
        raise HTTPException(status_code=404, detail="File tidak ditemukan")
    return {"success": True, "message": "File dihapus"}

@app.delete("/api/files")
async def clear_files(session_id: Optional[str] = None, conversation_id: Optional[str] = None):
    removed = _clear_files(conversation_id=conversation_id, session_id=session_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Tidak ada file untuk dihapus")
    return {"success": True, "message": "Lampiran dibersihkan"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )
