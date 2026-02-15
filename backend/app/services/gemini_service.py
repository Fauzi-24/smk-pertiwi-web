import ast
import json
import os
import re
import warnings
import io
import urllib.parse
import urllib.request
import time
import io
import urllib.parse
import urllib.request
import time
from difflib import SequenceMatcher
from datetime import datetime

from fastapi.concurrency import run_in_threadpool

warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
from PIL import Image

load_dotenv()


class SMKPertiwiChatbot:
    def __init__(self):
        # Inisialisasi API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.school_data_path = self._resolve_school_data_path()
        self.school_data = self._load_school_data()
        self.school_data_mtime = self._get_school_data_mtime()
        self.approved_feedback_path = self._resolve_approved_feedback_path()
        self.approved_feedback = self._load_approved_feedback()
        self.approved_feedback_mtime = self._get_approved_feedback_mtime()
        self.rag_path = self._resolve_rag_path()
        self.rag_documents = self._build_rag_documents(self.school_data)
        self._write_rag_file(self.rag_documents)
        self.possible_questions_path = self._resolve_possible_questions_path()
        self.possible_questions = self._build_possible_questions(self.school_data)
        self._write_possible_questions_file(self.possible_questions)
        self.materials_catalog = self._build_materials_catalog()
        self.system_instruction = self._build_system_instruction(self.school_data)
        self.school_keywords = self._build_school_keywords(self.school_data)

        self.enable_web_search = os.getenv("ENABLE_WEB_SEARCH", "").lower() in ("1", "true", "yes")
        self.auto_web_search = os.getenv("AUTO_WEB_SEARCH", "").lower() in ("1", "true", "yes")
        self.max_web_results = int(os.getenv("WEB_SEARCH_RESULTS", "5"))
        self.web_cache_ttl = int(os.getenv("WEB_SEARCH_CACHE_TTL", "1800"))
        self.web_cache_max = int(os.getenv("WEB_SEARCH_CACHE_MAX", "120"))
        self.web_cache = {}

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=self.system_instruction
        )
        self.vision_model = genai.GenerativeModel("gemini-2.5-flash")

    def _resolve_school_data_path(self):
        env_path = os.getenv("SCHOOL_DATA_PATH")
        if env_path and os.path.exists(env_path):
            return env_path

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        return os.path.join(base_dir, "frontend", "src", "data", "schoolData.js")

    def _resolve_rag_path(self):
        env_path = os.getenv("SCHOOL_RAG_PATH")
        if env_path:
            return env_path

        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(app_dir, "data", "school_rag.json")

    def _resolve_approved_feedback_path(self):
        env_path = os.getenv("APPROVED_FEEDBACK_PATH")
        if env_path:
            return env_path

        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(app_dir, "data", "feedback_approved.json")

    def _resolve_possible_questions_path(self):
        env_path = os.getenv("POSSIBLE_QUESTIONS_PATH")
        if env_path:
            return env_path

        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(app_dir, "data", "possible_questions.md")

    def _get_school_data_mtime(self):
        try:
            return os.path.getmtime(self.school_data_path)
        except OSError:
            return None

    def _get_approved_feedback_mtime(self):
        if not self.approved_feedback_path:
            return None
        try:
            return os.path.getmtime(self.approved_feedback_path)
        except OSError:
            return None

    def _extract_school_data_object(self, text):
        match = re.search(r"const\s+schoolData\s*=\s*", text)
        if not match:
            return None

        start = text.find("{", match.end())
        if start == -1:
            return None

        depth = 0
        in_single = False
        in_double = False
        escape = False

        for idx in range(start, len(text)):
            ch = text[idx]

            if in_single:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == "'":
                    in_single = False
                continue

            if in_double:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_double = False
                continue

            if ch == "'":
                in_single = True
                continue
            if ch == '"':
                in_double = True
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:idx + 1]

        return None

    def _quote_js_keys(self, text):
        out = []
        i = 0
        in_single = False
        in_double = False
        escape = False

        while i < len(text):
            ch = text[i]

            if in_single:
                out.append(ch)
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == "'":
                    in_single = False
                i += 1
                continue

            if in_double:
                out.append(ch)
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_double = False
                i += 1
                continue

            if ch == "'":
                in_single = True
                out.append(ch)
                i += 1
                continue
            if ch == '"':
                in_double = True
                out.append(ch)
                i += 1
                continue

            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < len(text) and (text[i].isalnum() or text[i] in ["_", "$"]):
                    i += 1
                key = text[start:i]

                j = i
                while j < len(text) and text[j].isspace():
                    j += 1

                if j < len(text) and text[j] == ":":
                    out.append('"')
                    out.append(key)
                    out.append('"')
                    out.append(text[i:j])
                    out.append(":")
                    i = j + 1
                else:
                    out.append(key)
                continue

            out.append(ch)
            i += 1

        return "".join(out)

    def _load_school_data(self):
        try:
            if not os.path.exists(self.school_data_path):
                return {}

            with open(self.school_data_path, "r", encoding="utf-8") as file:
                text = file.read()

            obj_text = self._extract_school_data_object(text)
            if not obj_text:
                return {}

            normalized = self._quote_js_keys(obj_text)
            data = ast.literal_eval(normalized)

            if isinstance(data, dict):
                return data

            return {}
        except Exception:
            return {}

    def _load_approved_feedback(self):
        path = self.approved_feedback_path
        if not path or not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []

    def _write_rag_file(self, documents):
        try:
            os.makedirs(os.path.dirname(self.rag_path), exist_ok=True)
            payload = {
                "source": "schoolData.js",
                "generated_at": datetime.now().isoformat(),
                "documents": documents
            }
            with open(self.rag_path, "w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _write_possible_questions_file(self, sections):
        if not sections or not self.possible_questions_path:
            return

        try:
            os.makedirs(os.path.dirname(self.possible_questions_path), exist_ok=True)
            lines = ["# Kemungkinan Pertanyaan untuk PRISM", ""]
            for title, items in sections.items():
                if not items:
                    continue
                lines.append(f"## {title}")
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")

            with open(self.possible_questions_path, "w", encoding="utf-8") as file:
                file.write("\n".join(lines).rstrip() + "\n")
        except Exception:
            pass

    def _dedupe_preserve(self, items):
        seen = set()
        output = []
        for item in items:
            if not item:
                continue
            key = item.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            output.append(item.strip())
        return output

    def _parse_teacher_entry(self, entry):
        name_part = entry.split("(")[0].strip()
        roles = []
        match = re.search(r"\((.+)\)", entry)
        if match:
            roles_raw = match.group(1)
            roles = [role.strip() for role in re.split(r"\s*/\s*|\s*\|\s*", roles_raw) if role.strip()]
        return {"name": name_part, "roles": roles, "raw": entry}

    def _is_placeholder_teacher(self, entry):
        if not entry:
            return True

        cleaned = self._normalize_text(entry)
        if not cleaned:
            return True

        placeholder_terms = ["guru baru", "tbd", "tba", "belum tersedia"]
        return any(term in cleaned for term in placeholder_terms)

    def _filter_placeholder_teachers(self, teachers):
        return [teacher for teacher in teachers if not self._is_placeholder_teacher(teacher)]

    def _normalize_text(self, text):
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def _similarity(self, left, right):
        return SequenceMatcher(None, left, right).ratio()

    def _tokenize(self, text):
        if not text:
            return []
        return [token for token in self._normalize_text(text).split() if token]

    def _extract_grade_semester(self, text):
        if not text:
            return None, None
        raw = text.lower()
        grade = None
        semester = None

        if re.search(r"\b(kelas|tingkat)\s*(10|x)\b", raw) or re.search(r"\b(10|x)\b", raw):
            grade = "10"
        if re.search(r"\b(kelas|tingkat)\s*(11|xi)\b", raw) or re.search(r"\b(11|xi)\b", raw):
            grade = "11"
        if re.search(r"\b(kelas|tingkat)\s*(12|xii)\b", raw) or re.search(r"\b(12|xii)\b", raw):
            grade = "12"

        if re.search(r"\bsemester\s*1\b|\bsmt\s*1\b|\bganjil\b", raw):
            semester = "1"
        if re.search(r"\bsemester\s*2\b|\bsmt\s*2\b|\bgenap\b", raw):
            semester = "2"

        return grade, semester

    def _build_school_keywords(self, data):
        tokens = set()
        codes = set()
        if not data:
            return {"tokens": tokens, "codes": codes}

        base_terms = [
            "smk", "pertiwi", "kuningan", "prism", "sekolah", "kepsek",
            "kepala sekolah", "guru", "pengajar", "mapel", "pelajaran",
            "jadwal", "jam", "keunggulan", "visi", "misi", "tujuan", "jurusan"
        ]
        for term in base_terms:
            tokens.update(self._normalize_text(term).split())

        name = data.get("name")
        if name:
            tokens.update(self._normalize_text(name).split())

        majors = data.get("majors", [])
        for major in majors:
            kode = major.get("kode")
            nama = major.get("nama")
            if kode:
                codes.add(self._normalize_text(kode))
                tokens.add(self._normalize_text(kode))
            if nama:
                tokens.update(self._normalize_text(nama).split())

        teachers = self._filter_placeholder_teachers(data.get("teachers", []))
        for entry in teachers:
            name_part = entry.split("(")[0]
            for token in self._normalize_text(name_part).split():
                if len(token) >= 4:
                    tokens.add(token)

        return {"tokens": tokens, "codes": codes}

    def _major_keyword_map(self):
        return {
            "RPL": ["rpl", "rekayasa", "perangkat", "lunak", "software", "pemrograman", "programming", "aplikasi"],
            "TKJ": ["tkj", "teknik", "komputer", "jaringan", "network", "server", "router"],
            "TKR": ["tkr", "kendaraan", "ringan", "mobil", "otomotif"],
            "TSM": ["tsm", "sepeda", "motor", "bengkel"],
            "TO": ["to", "ototronik", "otomotif", "elektronik", "kendaraan"],
            "LP": ["lp", "layanan", "perbankan", "bank", "teller", "keuangan"],
            "BDP": ["bdp", "bisnis", "daring", "pemasaran", "marketing", "jualan", "online", "ecommerce", "e-commerce"]
        }

    def _subject_aliases(self):
        return [
            {"label": "Bahasa Indonesia", "patterns": [r"bahasa indonesia", r"b\.\s*indonesia", r"bindo", r"indonesia"], "keywords": ["bahasa", "indonesia", "bindo"]},
            {"label": "Bahasa Inggris", "patterns": [r"bahasa inggris", r"b\.\s*inggris", r"\binggris\b", r"english"], "keywords": ["bahasa", "inggris", "english"]},
            {"label": "Bahasa Sunda", "patterns": [r"bahasa sunda", r"\bsunda\b"], "keywords": ["bahasa", "sunda"]},
            {"label": "Matematika", "patterns": [r"matematika", r"mtk"], "keywords": ["matematika", "mtk"]},
            {"label": "IPAS", "patterns": [r"\bipas\b", r"ipa", r"ips"], "keywords": ["ipas", "ipa", "ips"]},
            {"label": "PKN", "patterns": [r"\bpkn\b", r"ppkn", r"civics"], "keywords": ["pkn", "ppkn", "civics"]},
            {"label": "Sejarah", "patterns": [r"sejarah", r"history"], "keywords": ["sejarah", "history"]},
            {"label": "PAI", "patterns": [r"\bpai\b", r"pendidikan agama", r"agama"], "keywords": ["pai", "agama"]},
            {"label": "Olahraga", "patterns": [r"olahraga", r"penjaskes", r"pjok"], "keywords": ["olahraga", "penjaskes", "pjok"]},
            {"label": "Seni Budaya", "patterns": [r"seni budaya", r"\bseni\b", r"budaya"], "keywords": ["seni", "budaya"]},
            {"label": "Informatika", "patterns": [r"informatika", r"komputer"], "keywords": ["informatika", "komputer"]},
            {"label": "BK", "patterns": [r"\bbk\b", r"bimbingan konseling", r"konseling"], "keywords": ["bk", "konseling"]},
            {"label": "PKK", "patterns": [r"\bpkk\b"], "keywords": ["pkk"]},
            {"label": "Mapel Pilihan", "patterns": [r"mapel pilihan", r"mp pilihan"], "keywords": ["mapel pilihan", "mp pilihan"]}
        ]

    def _build_materials_catalog(self):
        return {
            "matematika": {
                "label": "Matematika",
                "grades": {
                    "10": {
                        "1": ["Bilangan & aljabar dasar", "Persamaan/pertidaksamaan", "Fungsi dasar", "Statistika dasar"],
                        "2": ["Geometri dasar", "Trigonometri dasar", "Peluang dasar", "Aplikasi aljabar"]
                    },
                    "11": {
                        "1": ["Fungsi lanjutan", "Barisan & deret", "Matriks dasar", "Trigonometri lanjutan"],
                        "2": ["Limit & turunan dasar", "Aplikasi turunan", "Statistika lanjutan", "Peluang lanjutan"]
                    },
                    "12": {
                        "1": ["Integral dasar", "Aplikasi integral", "Program linear", "Vektor/dimensi tiga"],
                        "2": ["Integral lanjutan", "Aplikasi vektor", "Statistika aplikasi", "Persiapan asesmen"]
                    }
                }
            },
            "bahasa indonesia": {
                "label": "Bahasa Indonesia",
                "grades": {
                    "10": {
                        "1": ["Teks laporan/eksposisi", "Kaidah kebahasaan", "Ringkasan/ulasan", "Literasi dasar"],
                        "2": ["Teks prosedur/negosiasi", "Puisi", "Resensi sederhana", "Presentasi lisan"]
                    },
                    "11": {
                        "1": ["Cerpen/drama", "Proposal/karya ilmiah", "Struktur argumentasi", "Presentasi"],
                        "2": ["Resensi", "Teks editorial", "Kebahasaan lanjut", "Proyek literasi"]
                    },
                    "12": {
                        "1": ["Artikel opini/argumentasi", "Esai/kritik", "Pidato persuasif", "Karya ilmiah"],
                        "2": ["Ulasan karya", "Editorial lanjutan", "Debat", "Portofolio menulis"]
                    }
                }
            },
            "bahasa inggris": {
                "label": "Bahasa Inggris",
                "grades": {
                    "10": {
                        "1": ["Introduction & descriptive", "Recount text", "Grammar dasar", "Vocabulary dasar"],
                        "2": ["Narrative text", "Procedure/announcement", "Dialog sehari-hari", "Writing dasar"]
                    },
                    "11": {
                        "1": ["Analytical exposition", "Report text", "Passive voice", "Writing formal"],
                        "2": ["Conditional sentences", "Email/resume", "Presentation skill", "Reading comprehension"]
                    },
                    "12": {
                        "1": ["Job application & CV", "Interview practice", "News item", "Discussion text"],
                        "2": ["Presentation lanjutan", "Writing lanjut", "Public speaking", "Portfolio task"]
                    }
                }
            },
            "bahasa sunda": {
                "label": "Bahasa Sunda",
                "grades": {
                    "10": {
                        "1": ["Undak-usuk basa", "Carita pondok", "Aksara Sunda dasar", "Kawih dasar"],
                        "2": ["Puisi Sunda", "Wawacan sederhana", "Biantara dasar", "Budaya lokal"]
                    },
                    "11": {
                        "1": ["Naskah drama", "Biantara/pidato", "Sastra Sunda", "Apresiasi karya"],
                        "2": ["Artikel sederhana", "Kritik sastra", "Presentasi", "Proyek budaya"]
                    },
                    "12": {
                        "1": ["Artikel/opini Sunda", "Analisis sastra", "Retorika", "Portofolio"],
                        "2": ["Publikasi karya", "Presentasi proyek", "Uji kompetensi literasi", "Karya akhir"]
                    }
                }
            },
            "ipas": {
                "label": "IPAS",
                "grades": {
                    "10": {
                        "1": ["Pengukuran & metode ilmiah", "Materi & perubahan", "Energi dasar", "Ekosistem"],
                        "2": ["Gerak & gaya", "Listrik dasar", "Sistem kehidupan", "Lingkungan"]
                    },
                    "11": {
                        "1": ["Sistem tubuh & genetika", "Gelombang", "Listrik & magnet", "Bumi & antariksa"],
                        "2": ["Reaksi kimia dasar", "Ekologi lanjut", "Teknologi terapan", "Proyek ilmiah"]
                    },
                    "12": {
                        "1": ["Bioteknologi dasar", "Energi terbarukan", "Iklim & lingkungan", "Analisis data"],
                        "2": ["Isu sains terkini", "Studi kasus", "Proyek akhir", "Persiapan asesmen"]
                    }
                }
            },
            "pkn": {
                "label": "PPKN",
                "grades": {
                    "10": {
                        "1": ["Pancasila & UUD 1945", "Bhinneka Tunggal Ika", "HAM", "Nilai kebangsaan"],
                        "2": ["Kewarganegaraan", "Demokrasi dasar", "Kewajiban warga negara", "Kasus kebangsaan"]
                    },
                    "11": {
                        "1": ["Sistem politik & demokrasi", "Hukum & konstitusi", "Wawasan nusantara", "Partisipasi warga"],
                        "2": ["Otonomi daerah", "Hak & kewajiban", "Kebijakan publik", "Proyek civic"]
                    },
                    "12": {
                        "1": ["Bela negara", "Anti korupsi", "Globalisasi", "Etika publik"],
                        "2": ["Isu kewarganegaraan", "Diskusi kebijakan", "Simulasi sidang", "Portofolio"]
                    }
                }
            },
            "sejarah": {
                "label": "Sejarah",
                "grades": {
                    "10": {
                        "1": ["Prasejarah", "Kerajaan nusantara", "Kolonialisme awal", "Perubahan sosial"],
                        "2": ["Kolonialisme lanjut", "Pergerakan awal", "Tokoh nasional", "Studi sumber sejarah"]
                    },
                    "11": {
                        "1": ["Pergerakan nasional", "Sumpah Pemuda", "Kemerdekaan", "Awal republik"],
                        "2": ["Orde Lama & Orde Baru", "Politik & ekonomi", "Sejarah lokal", "Analisis peristiwa"]
                    },
                    "12": {
                        "1": ["Reformasi", "Indonesia kontemporer", "Sejarah dunia modern", "Isu global"],
                        "2": ["Analisis sejarah kritis", "Proyek sejarah", "Presentasi riset", "Portofolio"]
                    }
                }
            },
            "pai": {
                "label": "PAI",
                "grades": {
                    "10": {
                        "1": ["Aqidah & akhlak", "Ibadah dasar", "Sejarah nabi", "Etika pergaulan"],
                        "2": ["Fiqh ibadah", "Akhlak sosial", "Moderasi beragama", "Proyek karakter"]
                    },
                    "11": {
                        "1": ["Fiqh muamalah", "Sejarah Islam", "Etika digital", "Kepemimpinan"],
                        "2": ["Akhlak sosial", "Toleransi", "Dakwah dasar", "Kajian kasus"]
                    },
                    "12": {
                        "1": ["Dakwah & komunikasi", "Penguatan karakter", "Isu keagamaan", "Proyek sosial"],
                        "2": ["Etika profesional", "Moderasi lanjutan", "Refleksi diri", "Portofolio"]
                    }
                }
            },
            "olahraga": {
                "label": "PJOK",
                "grades": {
                    "10": {
                        "1": ["Kebugaran jasmani", "Atletik dasar", "Permainan bola", "Kesehatan dasar"],
                        "2": ["Permainan beregu", "Teknik dasar olahraga", "Gizi dasar", "Kesehatan pribadi"]
                    },
                    "11": {
                        "1": ["Latihan kebugaran lanjut", "Permainan beregu lanjut", "Cedera olahraga", "Kebugaran mental"],
                        "2": ["Sport science dasar", "Latihan kondisi fisik", "Kesehatan reproduksi", "Proyek kebugaran"]
                    },
                    "12": {
                        "1": ["Kebugaran lanjut", "Program latihan", "Kesehatan & keselamatan", "Evaluasi kebugaran"],
                        "2": ["Proyek kebugaran", "Aktivitas rekreatif", "Refleksi kesehatan", "Portofolio"]
                    }
                }
            },
            "seni budaya": {
                "label": "Seni Budaya",
                "grades": {
                    "10": {
                        "1": ["Seni rupa dasar", "Musik dasar", "Tari dasar", "Teater dasar"],
                        "2": ["Apresiasi karya", "Teknik berkarya", "Pameran sederhana", "Proyek seni"]
                    },
                    "11": {
                        "1": ["Kreasi karya", "Manajemen pertunjukan", "Teknik lanjut", "Apresiasi"],
                        "2": ["Produksi karya", "Promosi karya", "Presentasi karya", "Portofolio"]
                    },
                    "12": {
                        "1": ["Proyek karya", "Pameran/pertunjukan", "Kurasi karya", "Kolaborasi"],
                        "2": ["Portofolio akhir", "Publikasi karya", "Evaluasi", "Presentasi akhir"]
                    }
                }
            },
            "informatika": {
                "label": "Informatika",
                "grades": {
                    "10": {
                        "1": ["Literasi digital", "Perangkat & OS", "Coding dasar", "Etika digital"],
                        "2": ["Data dasar", "Jaringan dasar", "Aplikasi perkantoran", "Proyek kecil"]
                    },
                    "11": {
                        "1": ["Algoritma dasar", "Struktur data", "Basis data", "Pengantar keamanan"],
                        "2": ["Web dasar", "API dasar", "Pemrograman lanjut", "Proyek semester"]
                    },
                    "12": {
                        "1": ["Pengembangan aplikasi", "Keamanan siber dasar", "Analitik data", "Manajemen proyek"],
                        "2": ["Proyek akhir", "Deploy aplikasi", "Presentasi", "Portofolio"]
                    }
                }
            },
            "bk": {
                "label": "BK",
                "grades": {
                    "10": {
                        "1": ["Adaptasi sekolah", "Belajar efektif", "Kenali minat-bakat", "Etika pergaulan"],
                        "2": ["Kesehatan mental dasar", "Relasi sosial", "Manajemen waktu", "Proyek pengembangan diri"]
                    },
                    "11": {
                        "1": ["Perencanaan karier", "Kesehatan mental", "Komunikasi efektif", "Etika digital"],
                        "2": ["Kesiapan kerja", "Manajemen stres", "Pengembangan diri", "Refleksi"]
                    },
                    "12": {
                        "1": ["Persiapan kerja/kuliah", "Simulasi wawancara", "Etika profesional", "Portofolio"],
                        "2": ["Kesiapan akhir", "Proyek karier", "Refleksi diri", "Pendampingan lanjut"]
                    }
                }
            },
            "pkk": {
                "label": "PKK",
                "grades": {
                    "10": {
                        "1": ["Mindset wirausaha", "Ide bisnis", "Dasar pemasaran", "Perencanaan sederhana"],
                        "2": ["Model bisnis", "Keuangan dasar", "Riset pasar", "Branding dasar"]
                    },
                    "11": {
                        "1": ["Produksi & operasional", "Pengendalian biaya", "Manajemen stok", "Strategi pemasaran"],
                        "2": ["Digital marketing", "Layanan pelanggan", "Evaluasi usaha", "Proyek bisnis"]
                    },
                    "12": {
                        "1": ["Pengembangan bisnis", "Pitching", "Legalitas dasar", "Kemitraan"],
                        "2": ["Skalasi usaha", "Proyek akhir", "Presentasi bisnis", "Portofolio usaha"]
                    }
                }
            },
            "rpl": {
                "label": "RPL",
                "grades": {
                    "10": {
                        "1": ["Dasar pemrograman", "Algoritma", "Struktur data dasar", "UI/UX dasar"],
                        "2": ["Basis data dasar", "Web dasar", "Pemrograman lanjut", "Proyek kecil"]
                    },
                    "11": {
                        "1": ["Web development", "Backend dasar & API", "Basis data lanjutan", "Testing dasar"],
                        "2": ["Frontend lanjut", "API lanjutan", "Keamanan aplikasi dasar", "Proyek semester"]
                    },
                    "12": {
                        "1": ["Mobile/Fullstack", "DevOps dasar", "Manajemen proyek", "Proyek akhir"],
                        "2": ["Deploy aplikasi", "Optimasi", "Presentasi produk", "Portofolio"]
                    }
                }
            },
            "tkj": {
                "label": "TKJ",
                "grades": {
                    "10": {
                        "1": ["Jaringan dasar", "Perakitan komputer", "Sistem operasi", "Troubleshooting dasar"],
                        "2": ["Pengkabelan", "Konfigurasi dasar", "Topologi jaringan", "Proyek kecil"]
                    },
                    "11": {
                        "1": ["Routing & switching", "Server dasar", "Keamanan jaringan", "Virtualisasi dasar"],
                        "2": ["Manajemen jaringan", "Monitoring", "Wireless", "Proyek semester"]
                    },
                    "12": {
                        "1": ["Jaringan lanjutan", "Cloud dasar", "Keamanan lanjut", "Project jaringan"],
                        "2": ["Optimasi jaringan", "Implementasi layanan", "Presentasi proyek", "Portofolio"]
                    }
                }
            },
            "tkr": {
                "label": "TKR",
                "grades": {
                    "10": {
                        "1": ["Dasar otomotif", "Sistem mesin", "Chassis & transmisi", "Perawatan berkala"],
                        "2": ["Sistem pendingin", "Sistem bahan bakar", "Rem & kemudi", "Praktik bengkel"]
                    },
                    "11": {
                        "1": ["EFI & sensor", "Sistem listrik", "Diagnosa kerusakan", "Servis berkala"],
                        "2": ["Kelistrikan lanjut", "Transmisi otomatis", "Overhaul dasar", "Proyek bengkel"]
                    },
                    "12": {
                        "1": ["Teknologi kendaraan", "Troubleshooting lanjut", "Perbaikan mesin", "Project layanan"],
                        "2": ["Overhaul lanjut", "Pengujian", "Manajemen bengkel", "Portofolio"]
                    }
                }
            },
            "tsm": {
                "label": "TSM",
                "grades": {
                    "10": {
                        "1": ["Dasar mesin sepeda motor", "Servis ringan", "Sistem bahan bakar", "Kelistrikan dasar"],
                        "2": ["Sistem pendingin", "Sistem rem", "Chassis & suspensi", "Praktik bengkel"]
                    },
                    "11": {
                        "1": ["Sistem injeksi", "Tune-up", "Diagnosa dasar", "Kelistrikan lanjut"],
                        "2": ["Overhaul dasar", "Modifikasi dasar", "Manajemen bengkel", "Proyek"]
                    },
                    "12": {
                        "1": ["Overhaul lanjut", "Diagnosa lanjutan", "Performa mesin", "Project layanan"],
                        "2": ["Uji kompetensi", "Proyek akhir", "Presentasi", "Portofolio"]
                    }
                }
            },
            "to": {
                "label": "TO",
                "grades": {
                    "10": {
                        "1": ["Elektronika dasar", "Sensor & aktuator", "Sistem kelistrikan", "Dasar otomotif"],
                        "2": ["Sistem kontrol dasar", "Rangkaian listrik", "Diagnosa dasar", "Praktik bengkel"]
                    },
                    "11": {
                        "1": ["ECU & kontrol", "CAN bus", "Sistem keselamatan", "Diagnosa lanjutan"],
                        "2": ["Integrasi sistem", "Elektronik otomotif", "Troubleshooting", "Proyek"]
                    },
                    "12": {
                        "1": ["Elektronik otomotif lanjut", "Smart car dasar", "Project akhir", "Presentasi"],
                        "2": ["Optimasi sistem", "Analisis data kendaraan", "Portofolio", "Uji kompetensi"]
                    }
                }
            },
            "lp": {
                "label": "LP",
                "grades": {
                    "10": {
                        "1": ["Dasar perbankan", "Layanan nasabah", "Produk bank", "Etika layanan"],
                        "2": ["Administrasi perbankan", "Komunikasi layanan", "Kas & transaksi", "Praktik layanan"]
                    },
                    "11": {
                        "1": ["Akuntansi dasar", "Transaksi perbankan", "Administrasi", "Keamanan data"],
                        "2": ["Layanan kredit dasar", "Kepatuhan", "Produk digital", "Proyek layanan"]
                    },
                    "12": {
                        "1": ["Fintech & digital banking", "Kepatuhan lanjut", "Analisis layanan", "Project akhir"],
                        "2": ["Simulasi layanan", "Evaluasi", "Presentasi", "Portofolio"]
                    }
                }
            },
            "bdp": {
                "label": "BDP",
                "grades": {
                    "10": {
                        "1": ["Dasar pemasaran", "Branding", "Riset pasar", "Komunikasi pemasaran"],
                        "2": ["Promosi dasar", "Penjualan", "Konten dasar", "Proyek kecil"]
                    },
                    "11": {
                        "1": ["Digital marketing", "Marketplace", "Konten kreatif", "Strategi promosi"],
                        "2": ["Analitik dasar", "Campaign", "Manajemen toko online", "Proyek semester"]
                    },
                    "12": {
                        "1": ["Analitik pemasaran", "Campaign lanjut", "Bisnis online", "Project penjualan"],
                        "2": ["Optimasi penjualan", "Presentasi", "Portofolio", "Uji kompetensi"]
                    }
                }
            }
            ,
            "mapel pilihan": {
                "label": "Mapel Pilihan",
                "grades": {
                    "10": {
                        "1": ["Pengayaan kompetensi dasar", "Pemantapan materi jurusan", "Latihan proyek sederhana"],
                        "2": ["Pendalaman topik pilihan", "Praktik terarah", "Proyek kecil sesuai jurusan"]
                    },
                    "11": {
                        "1": ["Pendalaman kompetensi", "Studi kasus", "Proyek menengah"],
                        "2": ["Spesialisasi topik", "Praktik lanjutan", "Proyek semester"]
                    },
                    "12": {
                        "1": ["Pendalaman lanjutan", "Proyek akhir", "Persiapan uji kompetensi"],
                        "2": ["Proyek akhir lanjutan", "Presentasi portofolio", "Evaluasi kompetensi"]
                    }
                }
            }
        }

    def _is_school_query(self, query):
        normalized = self._normalize_query(query)
        if not normalized:
            return False

        if self._contains(
            normalized,
            [
                r"\bsmk\b", r"\bpertiwi\b", r"\bkuningan\b", r"\bsekolah\b",
                r"\bjurusan\b", r"\bguru\b", r"\bmapel\b", r"\bpelajaran\b",
                r"\bkepsek\b", r"\bkepala sekolah\b", r"\bjadwal\b",
                r"\bkeunggul\w*\b", r"\bunggulan\w*\b", r"\bvisi\b", r"\bmisi\b"
            ]
        ):
            return True

        tokens = set(normalized.split())
        keyword_data = self.school_keywords or {}
        keyword_tokens = keyword_data.get("tokens", set())
        keyword_codes = keyword_data.get("codes", set())

        if tokens & keyword_codes:
            return True
        if tokens & keyword_tokens:
            return True

        return False

    def _is_school_query_strict(self, query):
        normalized = self._normalize_query(query)
        if not normalized:
            return False

        if self._contains(
            normalized,
            [
                r"\bsmk\b", r"\bpertiwi\b", r"\bkuningan\b", r"\bsekolah\b",
                r"\bjurusan\b", r"\bguru\b", r"\bmapel\b", r"\bpelajaran\b",
                r"\bkepsek\b", r"\bkepala sekolah\b", r"\bjadwal\b",
                r"\bkeunggul\w*\b", r"\bunggulan\w*\b", r"\bvisi\b", r"\bmisi\b"
            ]
        ):
            return True

        tokens = set(normalized.split())
        keyword_data = self.school_keywords or {}
        keyword_codes = keyword_data.get("codes", set())
        if tokens & keyword_codes:
            return True

        return False

    def _normalize_query(self, text):
        if not text:
            return ""

        cleaned = text.lower()
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)

        replacements = [
            (r"\bjurusana\b", "jurusan"),
            (r"\bjurusn\b", "jurusan"),
            (r"\bjurusa\b", "jurusan"),
            (r"\bjuruan\b", "jurusan"),
            (r"\bmapelny\b", "mapel"),
            (r"\bmapelnya\b", "mapel"),
            (r"\bmapel nya\b", "mapel"),
            (r"\bmaple\b", "mapel"),
            (r"\bmapell\b", "mapel"),
            (r"\bpelajaranya\b", "pelajaran"),
            (r"\bpelajarannya\b", "pelajaran"),
            (r"\bpelajaran nya\b", "pelajaran"),
            (r"\bpelajarann\b", "pelajaran"),
            (r"\bkapsek\b", "kepsek"),
            (r"\bkeps?ek\b", "kepsek"),
            (r"\bskolah\b", "sekolah"),
            (r"\bsekola\b", "sekolah"),
            (r"\bgurunya\b", "guru"),
            (r"\bngajar\b", "mengajar"),
            (r"\bmengajar\b", "mengajar"),
        ]
        for pattern, repl in replacements:
            cleaned = re.sub(pattern, repl, cleaned)

        cleaned = re.sub(r"\br\s*p\s*l\b", "rpl", cleaned)
        cleaned = re.sub(r"\bt\s*k\s*j\b", "tkj", cleaned)
        cleaned = re.sub(r"\bt\s*k\s*r\b", "tkr", cleaned)
        cleaned = re.sub(r"\bt\s*s\s*m\b", "tsm", cleaned)
        cleaned = re.sub(r"\bt\s*o\b", "to", cleaned)
        cleaned = re.sub(r"\bl\s*p\b", "lp", cleaned)
        cleaned = re.sub(r"\bb\s*d\s*p\b", "bdp", cleaned)

        return self._normalize_text(cleaned)

    def _normalize_name(self, name):
        name = re.sub(
            r"\b(s\.?pd\.?|m\.?pd\.?|s\.?kom\.?|st\.?|se\.?|s\.?e\.?|s\.?or\.?|m\.?si\.?|drs\.?|ir\.?)\b",
            "",
            name,
            flags=re.IGNORECASE
        )
        return self._normalize_text(name)

    def _match_teacher_entry(self, query, teachers):
        normalized_query = self._normalize_query(query)
        best_match = None
        best_len = 0
        major_codes = {"rpl", "tkj", "tkr", "tsm", "to", "lp", "bdp"}
        stopwords = {
            "guru", "bapak", "ibu", "pak", "bu", "ust", "ustadz", "ustadzah",
            "kepsek", "kepala", "sekolah", "koordinator", "koord", "bk",
            "pd", "mp", "pilihan", "jurusan", "mapel", "mata", "pelajaran",
            "ngajar", "mengajar"
        }

        for entry in teachers:
            if self._is_placeholder_teacher(entry):
                continue
            parsed = self._parse_teacher_entry(entry)
            name_key = self._normalize_name(parsed["name"])
            if not name_key:
                continue

            if name_key in normalized_query:
                if len(name_key) > best_len:
                    best_match = parsed
                    best_len = len(name_key)
                continue

            tokens = [
                token for token in name_key.split()
                if len(token) > 2 and token not in stopwords and token not in major_codes
            ]
            if tokens:
                overlap = [token for token in tokens if token in normalized_query]
                if len(overlap) >= 2:
                    score = len(name_key)
                    if score > best_len:
                        best_match = parsed
                        best_len = score

        if best_match:
            return best_match

        query_tokens = {
            token for token in normalized_query.split()
            if len(token) >= 4 and token not in stopwords and token not in major_codes
        }
        if not query_tokens:
            return None

        candidates = []
        for entry in teachers:
            if self._is_placeholder_teacher(entry):
                continue
            parsed = self._parse_teacher_entry(entry)
            name_tokens = {
                token for token in self._normalize_name(parsed["name"]).split()
                if token and token not in stopwords and token not in major_codes
            }
            if query_tokens & name_tokens:
                candidates.append(parsed)

        if len(candidates) == 1:
            return candidates[0]

        return None

    def _build_rag_documents(self, data):
        if not data:
            return []

        documents = []

        def add_doc(doc_id, title, content, tags):
            if content:
                documents.append({
                    "id": doc_id,
                    "title": title,
                    "content": content,
                    "tags": tags
                })

        name = data.get("name")
        address = data.get("address")
        headmaster = data.get("headmaster")
        if name or address or headmaster:
            parts = []
            if name:
                parts.append(f"Nama: {name}")
            if address:
                parts.append(f"Alamat: {address}")
            if headmaster:
                parts.append(f"Kepala Sekolah: {headmaster}")
            add_doc("profil-sekolah", "Profil Sekolah", "\n".join(parts), ["profil", "sekolah"])

        history = data.get("history")
        if history:
            add_doc("sejarah", "Profil Singkat", history, ["sejarah", "profil"])

        vision = data.get("vision")
        mission = data.get("mission", [])
        if vision or mission:
            lines = []
            if vision:
                lines.append(f"Visi: {vision}")
            if mission:
                lines.append("Misi:")
                lines.extend([f"- {item}" for item in mission])
            add_doc("visi-misi", "Visi dan Misi", "\n".join(lines), ["visi", "misi"])

        goals = data.get("goals", [])
        if goals:
            add_doc("tujuan", "Tujuan Sekolah", self._format_list(goals), ["tujuan"])

        advantages = data.get("advantages", [])
        if advantages:
            add_doc("keunggulan", "Keunggulan Sekolah", self._format_list(advantages), ["keunggulan"])

        quick_facts = data.get("quickFacts", [])
        if quick_facts:
            add_doc("fakta", "Fakta Singkat", self._format_list(quick_facts), ["fakta", "data singkat"])

        schedule = data.get("schedule", [])
        if schedule:
            add_doc("jadwal", "Jadwal Pelajaran", self._format_list(schedule), ["jadwal", "jam sekolah"])

        majors = data.get("majors", [])
        if majors:
            lines = []
            for major in majors:
                nama = major.get("nama")
                kode = major.get("kode")
                desc = major.get("deskripsi")
                if nama and kode:
                    header = f"{nama} ({kode})"
                else:
                    header = nama or kode
                if header and desc:
                    lines.append(f"{header}: {desc}")
                elif header:
                    lines.append(header)
            add_doc("jurusan", "Daftar Jurusan", "\n".join(lines), ["jurusan", "kompetensi", "program"])

        teachers = self._filter_placeholder_teachers(data.get("teachers", []))
        if teachers:
            add_doc("guru", "Daftar Guru", self._format_list(teachers), ["guru", "pengajar", "mapel"])

            major_codes = ["RPL", "TKJ", "TKR", "TSM", "TO", "LP", "BDP"]
            by_major = {code: [] for code in major_codes}
            by_role = {}

            for entry in teachers:
                parsed = self._parse_teacher_entry(entry)
                roles = parsed["roles"]
                for code in major_codes:
                    if re.search(rf"\b{re.escape(code)}\b", entry, flags=re.IGNORECASE):
                        by_major[code].append(parsed["name"])

                for role in roles:
                    role_key = self._normalize_role_label(role)
                    if not role_key:
                        continue
                    by_role.setdefault(role_key, []).append(parsed["name"])

            for code, names in by_major.items():
                if names:
                    add_doc(
                        f"guru-{code.lower()}",
                        f"Guru {code}",
                        self._format_list(sorted(set(names))),
                        ["guru", "jurusan", code.lower()]
                    )

            for code in major_codes:
                roles = self._get_roles_by_major(teachers, code)
                if roles:
                    add_doc(
                        f"mapel-{code.lower()}",
                        f"Mapel/Kompetensi {code}",
                        self._format_list(roles),
                        ["mapel", "jurusan", code.lower()]
                    )

            for role, names in by_role.items():
                add_doc(
                    f"guru-{self._normalize_text(role).replace(' ', '-')}",
                    f"Guru {role}",
                    self._format_list(sorted(set(names))),
                    ["guru", "mapel", self._normalize_text(role)]
                )

        documents.extend(self._build_faq_documents(data))
        documents.extend(self._build_approved_documents())

        return documents

    def _build_approved_documents(self):
        approved = self.approved_feedback or []
        docs = []
        for item in approved:
            correction = item.get("correction") or item.get("answer") or ""
            question = item.get("question") or item.get("user_question") or ""
            if not correction:
                continue
            title = "Koreksi Admin"
            if question:
                title = f"Koreksi Admin: {question[:60]}"
            content_lines = []
            if question:
                content_lines.append(f"Q: {question}")
            content_lines.append(f"A: {correction}")
            source = item.get("source")
            if source:
                content_lines.append(f"Sumber: {source}")
            docs.append({
                "id": f"admin-{item.get('id', '')}",
                "title": title,
                "content": "\n".join(content_lines),
                "tags": ["admin", "koreksi", "pembelajaran"]
            })
        return docs

    def _build_possible_questions(self, data):
        if not data:
            return {}

        majors = data.get("majors", [])
        teachers = data.get("teachers", [])

        profil = []
        profil_templates = [
            "Nama lengkap {school} apa?",
            "Alamat {school} di mana?",
            "Letak {school} di mana?",
            "Siapa kepala sekolah {school}?",
            "Siapa kepsek {school}?",
            "Profil singkat {school}?",
            "Info singkat tentang {school}?",
            "Sekolah {school} berada di mana?"
        ]
        school_name = data.get("name", "SMK Pertiwi Kuningan")
        for template in profil_templates:
            profil.append(template.format(school=school_name))

        visi_misi = [
            "Apa visi sekolah?",
            "Apa misi sekolah?",
            "Tujuan sekolah apa saja?",
            f"Visi dan misi {school_name}?"
        ]

        keunggulan = [
            f"Apa keunggulan {school_name}?",
            "Kelebihan sekolah ini apa?",
            "Program unggulan sekolah?",
            "Keunggulan fasilitas sekolah apa saja?"
        ]

        fakta = [
            f"Data singkat {school_name}?",
            "Fakta singkat tentang sekolah?",
            f"{school_name} berdiri tahun berapa?",
            "Jumlah siswa aktif berapa?",
            "Jumlah alumni berapa?"
        ]

        jadwal = [
            f"Jadwal pelajaran {school_name}?",
            "Jam pelajaran mulai jam berapa?",
            "Jam istirahat sekolah kapan?",
            "Jam masuk sekolah berapa?"
        ]

        jurusan = [
            f"Jurusan apa saja di {school_name}?",
            f"Daftar jurusan {school_name}?",
            "Kompetensi keahlian apa saja?",
            "Program keahlian apa saja?"
        ]

        guru_mapel = [
            f"Siapa saja guru di {school_name}?",
            f"Daftar guru {school_name}?",
            "Guru mapel Bahasa Indonesia siapa?",
            "Guru mapel Bahasa Inggris siapa?",
            "Guru mapel Matematika siapa?",
            "Guru PAI siapa?",
            "Guru IPAS siapa?",
            "Siapa guru BK?",
            "Siapa guru PKK?"
        ]

        jumlah = [
            "Jumlah guru berapa?",
            "Berapa total guru?",
            "Jumlah jurusan ada berapa?",
            "Total jurusan ada berapa?"
        ]

        major_aliases = []
        for major in majors:
            kode = major.get("kode")
            nama = major.get("nama")
            if kode:
                major_aliases.append(kode)
            if nama:
                major_aliases.append(nama)

        teacher_templates = [
            "Siapa saja guru {major}?",
            "Daftar guru {major}?",
            "Guru jurusan {major} siapa?",
            "Siapa pengajar {major}?",
            "Siapa yang mengajar {major}?"
        ]
        subject_templates = [
            "Mapel {major} apa saja?",
            "Pelajaran {major} apa saja?",
            "Mata pelajaran {major} apa?",
            "Kompetensi {major} apa saja?"
        ]
        focus_templates = [
            "{major} fokus di bidang apa?",
            "{major} belajar apa saja?",
            "Jurusan {major} belajar apa?",
            "Fokus jurusan {major} apa?",
            "Bidang keahlian {major} apa?"
        ]

        for major in major_aliases:
            for template in teacher_templates:
                jurusan.append(template.format(major=major))
            for template in subject_templates:
                jurusan.append(template.format(major=major))
            for template in focus_templates:
                jurusan.append(template.format(major=major))

        subject_aliases = self._subject_aliases()
        for subject in subject_aliases:
            label = subject["label"]
            guru_mapel.append(f"Guru {label} siapa?")
            guru_mapel.append(f"Siapa guru {label}?")
            guru_mapel.append(f"Guru mapel {label} siapa?")

        if teachers:
            guru_mapel.append("Guru wali kelas ada siapa saja?")

        sections = {
            "Profil Sekolah": self._dedupe_preserve(profil),
            "Visi Misi Tujuan": self._dedupe_preserve(visi_misi),
            "Keunggulan": self._dedupe_preserve(keunggulan),
            "Fakta Singkat": self._dedupe_preserve(fakta),
            "Jadwal": self._dedupe_preserve(jadwal),
            "Jurusan": self._dedupe_preserve(jurusan),
            "Guru dan Mapel": self._dedupe_preserve(guru_mapel),
            "Jumlah": self._dedupe_preserve(jumlah)
        }

        return sections

    def _build_faq_documents(self, data):
        if not data:
            return []

        documents = []

        def add_doc(doc_id, title, lines, tags):
            if lines:
                documents.append({
                    "id": doc_id,
                    "title": title,
                    "content": "\n".join(lines),
                    "tags": tags
                })

        name = data.get("name")
        address = data.get("address")
        headmaster = data.get("headmaster")
        vision = data.get("vision")
        mission = data.get("mission", [])
        goals = data.get("goals", [])
        history = data.get("history")
        advantages = data.get("advantages", [])
        quick_facts = data.get("quickFacts", [])
        schedule = data.get("schedule", [])
        majors = data.get("majors", [])
        teachers = self._filter_placeholder_teachers(data.get("teachers", []))

        profil_lines = [
            "Q: Nama lengkap sekolah apa?",
            f"A: {name or 'Data tidak tersedia di schoolData.js.'}",
            "Q: Alamat SMK Pertiwi Kuningan di mana?",
            f"A: {address or 'Data tidak tersedia di schoolData.js.'}",
            "Q: Siapa kepala sekolah?",
            f"A: {headmaster or 'Data tidak tersedia di schoolData.js.'}",
            "Q: Siapa kepsek SMK Pertiwi Kuningan?",
            f"A: {headmaster or 'Data tidak tersedia di schoolData.js.'}"
        ]
        add_doc("faq-profil", "FAQ Profil Sekolah", profil_lines, ["faq", "profil", "kepsek", "alamat"])

        if history:
            sejarah_lines = [
                "Q: Ceritakan profil singkat SMK Pertiwi Kuningan.",
                f"A: {history}",
                "Q: Sejarah SMK Pertiwi Kuningan?",
                f"A: {history}"
            ]
            add_doc("faq-sejarah", "FAQ Sejarah", sejarah_lines, ["faq", "sejarah"])

        visi_misi_lines = []
        if vision:
            visi_misi_lines.extend([
                "Q: Apa visi sekolah?",
                f"A: {vision}"
            ])
        if mission:
            visi_misi_lines.extend([
                "Q: Misi sekolah apa saja?",
                "A: " + "; ".join(mission)
            ])
        if goals:
            visi_misi_lines.extend([
                "Q: Tujuan sekolah apa saja?",
                "A: " + "; ".join(goals)
            ])
        add_doc("faq-visi-misi", "FAQ Visi Misi", visi_misi_lines, ["faq", "visi", "misi", "tujuan"])

        if advantages:
            keunggulan_lines = [
                "Q: Apa keunggulan SMK Pertiwi Kuningan?",
                "A: " + "; ".join(advantages),
                "Q: Kelebihan sekolah ini apa?",
                "A: " + "; ".join(advantages)
            ]
            add_doc("faq-keunggulan", "FAQ Keunggulan", keunggulan_lines, ["faq", "keunggulan"])

        if quick_facts:
            fakta_lines = [
                "Q: Data singkat SMK Pertiwi Kuningan?",
                "A: " + "; ".join(quick_facts),
                "Q: Fakta singkat tentang sekolah?",
                "A: " + "; ".join(quick_facts)
            ]
            add_doc("faq-fakta", "FAQ Fakta Singkat", fakta_lines, ["faq", "fakta"])

        if schedule:
            jadwal_lines = [
                "Q: Jadwal pelajaran SMK Pertiwi Kuningan?",
                "A: " + "; ".join(schedule),
                "Q: Jam pelajaran mulai jam berapa?",
                f"A: {schedule[0] if schedule else 'Data tidak tersedia di schoolData.js.'}"
            ]
            add_doc("faq-jadwal", "FAQ Jadwal", jadwal_lines, ["faq", "jadwal"])

        if majors:
            major_list = [
                f"{item.get('nama')} ({item.get('kode')})"
                for item in majors
                if item.get("nama") and item.get("kode")
            ]
            jurusan_lines = [
                "Q: Jurusan apa saja di SMK Pertiwi Kuningan?",
                "A: " + "; ".join(major_list) if major_list else "A: Data jurusan tidak tersedia di schoolData.js."
            ]
            for major in majors:
                kode = major.get("kode")
                nama = major.get("nama")
                desc = major.get("deskripsi")
                if kode and desc:
                    jurusan_lines.extend([
                        f"Q: {kode} fokus di bidang apa?",
                        f"A: {desc}"
                    ])
                    jurusan_lines.extend([
                        f"Q: Mapel {kode} apa saja?",
                        "A: Data mapel per jurusan diambil dari daftar guru."
                    ])
                if nama and desc:
                    jurusan_lines.extend([
                        f"Q: {nama} belajar apa?",
                        f"A: {desc}"
                    ])
            add_doc("faq-jurusan", "FAQ Jurusan", jurusan_lines, ["faq", "jurusan"])

        if teachers:
            guru_lines = [
                "Q: Siapa saja guru di SMK Pertiwi Kuningan?",
                "A: " + "; ".join(teachers)
            ]

            major_codes = ["RPL", "TKJ", "TKR", "TSM", "TO", "LP", "BDP"]
            for code in major_codes:
                names = self._get_teachers_by_major(teachers, code)
                if names:
                    guru_lines.extend([
                        f"Q: Siapa guru {code}?",
                        "A: " + "; ".join(names)
                    ])
                roles = self._get_roles_by_major(teachers, code)
                if roles:
                    guru_lines.extend([
                        f"Q: Mapel {code} apa saja?",
                        "A: " + "; ".join(roles)
                    ])

            roles = self._get_unique_roles(teachers)
            for role in roles:
                names = [self._parse_teacher_entry(entry)["name"] for entry in teachers if role in entry]
                if names:
                    guru_lines.extend([
                        f"Q: Guru {role} siapa?",
                        "A: " + "; ".join(sorted(set(names)))
                    ])

            add_doc("faq-guru", "FAQ Guru dan Mapel", guru_lines, ["faq", "guru", "mapel"])

        return documents

    def _refresh_school_data(self):
        current_mtime = self._get_school_data_mtime()
        approved_mtime = self._get_approved_feedback_mtime()
        school_changed = current_mtime is not None and current_mtime != self.school_data_mtime
        approved_changed = approved_mtime is not None and approved_mtime != self.approved_feedback_mtime

        if not school_changed and not approved_changed:
            return

        if school_changed:
            self.school_data = self._load_school_data()
            self.school_data_mtime = current_mtime
            self.possible_questions = self._build_possible_questions(self.school_data)
            self._write_possible_questions_file(self.possible_questions)
            self.materials_catalog = self._build_materials_catalog()
            self.system_instruction = self._build_system_instruction(self.school_data)
            self.school_keywords = self._build_school_keywords(self.school_data)
            self.model = genai.GenerativeModel(
                "gemini-2.5-flash",
                system_instruction=self.system_instruction
            )

        if approved_changed:
            self.approved_feedback = self._load_approved_feedback()
            self.approved_feedback_mtime = approved_mtime

        self.rag_documents = self._build_rag_documents(self.school_data)
        self._write_rag_file(self.rag_documents)

    def _build_school_context(self, data):
        if not data:
            return "DATA SEKOLAH: (tidak tersedia)"

        lines = []

        name = data.get("name")
        if name:
            lines.append(f"Nama: {name}")

        address = data.get("address")
        if address:
            lines.append(f"Alamat: {address}")

        headmaster = data.get("headmaster")
        if headmaster:
            lines.append(f"Kepala Sekolah: {headmaster}")

        vision = data.get("vision")
        if vision:
            lines.append(f"Visi: {vision}")

        history = data.get("history")
        if history:
            lines.append(f"Profil Singkat: {history}")

        quick_facts = data.get("quickFacts", [])
        if quick_facts:
            lines.append("Fakta Singkat:")
            lines.extend([f"- {fact}" for fact in quick_facts])

        advantages = data.get("advantages", [])
        if advantages:
            lines.append("Keunggulan:")
            lines.extend([f"- {item}" for item in advantages])

        mission = data.get("mission", [])
        if mission:
            lines.append("Misi:")
            lines.extend([f"- {item}" for item in mission])

        goals = data.get("goals", [])
        if goals:
            lines.append("Tujuan:")
            lines.extend([f"- {item}" for item in goals])

        schedule = data.get("schedule", [])
        if schedule:
            lines.append("Jadwal Pelajaran:")
            lines.extend([f"- {slot}" for slot in schedule])

        majors = data.get("majors", [])
        if majors:
            lines.append("Jurusan:")
            for major in majors:
                nama = major.get("nama")
                kode = major.get("kode")
                desc = major.get("deskripsi")
                if nama and kode and desc:
                    lines.append(f"- {nama} ({kode}): {desc}")
                elif nama and kode:
                    lines.append(f"- {nama} ({kode})")
                elif nama:
                    lines.append(f"- {nama}")
                elif kode:
                    lines.append(f"- {kode}")

        teachers = data.get("teachers", [])
        if teachers:
            lines.append("Daftar Guru:")
            lines.extend([f"- {teacher}" for teacher in teachers])

        return "\n".join(lines)

    def _build_system_instruction(self, data):
        context = self._build_school_context(data)
        return (
            "Anda adalah \"Prism\", asisten AI cerdas untuk SMK Pertiwi Kuningan (layaknya Google Gemini).\n"
            "PENTING: Website ini dibuat oleh Fathurrachman Fauzi. Jika ditanya siapa pembuat/developer, jawab: Fathurrachman Fauzi.\n\n"
            "Tugas Anda: Menjawab pertanyaan pengguna dengan akurat, ramah, dan informatif menggunakan DATA RESMI di bawah.\n"
            "Gaya Bahasa: Natural, luwes, membantu, dan profesional. Gunakan format Markdown (Bold, List, Tabel) agar mudah dibaca.\n\n"
            "DATA RESMI (schoolData.js):\n"
            f"{context}\n\n"
            "PEDOMAN PENTING:\n"
            "1. **Prioritaskan Data Resmi**: Gunakan data di atas sebagai kebenaran mutlak.\n"
            "2. **Format Markdown**: Gunakan **bold** untuk poin penting, dan list untuk rincian.\n"
            "3. **Saran Pertanyaan**: Di AKHIR setiap jawaban, berikan 3 opsi pertanyaan lanjutan yang relevan dengan konteks.\n"
            "   Format:\n"
            "   **Mungkin kamu ingin tahu:**\n"
            "   1. [Pertanyaan 1]\n"
            "   2. [Pertanyaan 2]\n"
            "   3. [Pertanyaan 3]\n"
            "4. **Lokasi & Umum**: Jika pengguna bertanya lokasi (misal: 'Bengkel Bandung Motor'), tempat PKL, atau pengetahuan umum di luar data sekolah, **JAWABLAH secara langsung** menggunakan pengetahuan Anda sebagai AI. Jangan terpaku hanya pada data sekolah jika pertanyaan bersifat umum atau geografis.\n"
            "5. **Sikap**: Jadilah asisten yang solutif. Jika tidak tahu, tawarkan untuk mencari informasi di internet.\n"
        )

    def _contains(self, text, patterns):
        return any(re.search(pattern, text) for pattern in patterns)

    def _format_list(self, items):
        return "\n".join([f"- {item}" for item in items])

    def _normalize_role_label(self, role):
        if not role:
            return ""

        cleaned = role.strip()
        cleaned = re.sub(r"^pd\.?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.replace("Mp.", "Mapel").replace("mp.", "mapel")
        cleaned = re.sub(r"\bB\.\s*Indonesia\b", "Bahasa Indonesia", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bB\.\s*Inggris\b", "Bahasa Inggris", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bB\.\s*Sunda\b", "Bahasa Sunda", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def _get_teachers_by_major(self, teachers, code):
        names = []
        if not code:
            return names
        for entry in teachers:
            if self._is_placeholder_teacher(entry):
                continue
            if re.search(rf"\b{re.escape(code)}\b", entry, flags=re.IGNORECASE):
                parsed = self._parse_teacher_entry(entry)
                if parsed["name"]:
                    names.append(parsed["name"])
        return sorted(set(names))

    def _get_unique_roles(self, teachers):
        roles = set()
        for entry in teachers:
            if self._is_placeholder_teacher(entry):
                continue
            parsed = self._parse_teacher_entry(entry)
            for role in parsed["roles"]:
                normalized = self._normalize_role_label(role)
                if normalized:
                    roles.add(normalized)
        return sorted(roles)

    def _get_roles_by_major(self, teachers, code):
        if not teachers or not code:
            return []

        roles = set()
        for entry in teachers:
            if self._is_placeholder_teacher(entry):
                continue
            if re.search(rf"\b{re.escape(code)}\b", entry, flags=re.IGNORECASE):
                parsed = self._parse_teacher_entry(entry)
                for role in parsed["roles"]:
                    normalized = self._normalize_role_label(role)
                    if normalized:
                        roles.add(normalized)
        return sorted(roles)

    def _material_label_key(self, label):
        if not label:
            return ""
        normalized = self._normalize_role_label(label) or label
        key = self._normalize_text(normalized)
        if key.startswith("pd "):
            key = key.replace("pd ", "")
        if "mapel pilihan" in key or "mp pilihan" in key:
            return "mapel pilihan"
        if "bahasa indonesia" in key:
            return "bahasa indonesia"
        if "bahasa inggris" in key:
            return "bahasa inggris"
        if "bahasa sunda" in key:
            return "bahasa sunda"
        if "matematika" in key or key == "mtk":
            return "matematika"
        if "ipas" in key or key in ("ipa", "ips"):
            return "ipas"
        if key in ("pkn", "ppkn"):
            return "pkn"
        if "sejarah" in key:
            return "sejarah"
        if "pai" in key or "agama" in key:
            return "pai"
        if "olahraga" in key or "pjok" in key or "penjaskes" in key:
            return "olahraga"
        if "seni budaya" in key or key == "seni" or key == "budaya":
            return "seni budaya"
        if "informatika" in key or key == "komputer":
            return "informatika"
        if "bk" == key or "konseling" in key:
            return "bk"
        if "pkk" in key:
            return "pkk"
        for code in ["rpl", "tkj", "tkr", "tsm", "to", "lp", "bdp"]:
            if re.search(rf"\b{code}\b", key):
                return code
        return key

    def _format_materials(self, label, grades, grade=None, semester=None):
        lines = [f"Materi umum {label} (kelas 10-12):"]
        grade_order = [grade] if grade else ["10", "11", "12"]
        for g in grade_order:
            content = grades.get(g) if grades else None
            if not content:
                continue
            if isinstance(content, list):
                lines.append(f"Kelas {g}: " + "; ".join(content))
                continue
            if isinstance(content, dict):
                if semester:
                    topics = content.get(str(semester))
                    if topics:
                        lines.append(f"Kelas {g} Semester {semester}: " + "; ".join(topics))
                else:
                    sem1 = content.get("1")
                    sem2 = content.get("2")
                    if sem1:
                        lines.append(f"Kelas {g} Semester 1: " + "; ".join(sem1))
                    if sem2:
                        lines.append(f"Kelas {g} Semester 2: " + "; ".join(sem2))
        lines.append("Catatan: materi bisa menyesuaikan kurikulum sekolah dan guru pengampu.")
        return "\n".join(lines)

    def _retrieve_rag(self, query, top_k=4):
        if not self.rag_documents:
            return []

        normalized_query = self._normalize_query(query)
        query_tokens = set(re.findall(r"[a-z0-9]+", normalized_query))
        scored = []

        for doc in self.rag_documents:
            doc_text = f"{doc.get('title', '')} {doc.get('content', '')} {' '.join(doc.get('tags', []))}"
            doc_tokens = set(re.findall(r"[a-z0-9]+", doc_text.lower()))
            score = len(query_tokens & doc_tokens)
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    def _build_rag_context(self, query):
        docs = self._retrieve_rag(query)
        if not docs:
            return None

        blocks = []
        for doc in docs:
            title = doc.get("title", "Dokumen")
            content = doc.get("content", "")
            if content:
                blocks.append(f"[{title}]\n{content}")
        return "\n\n".join(blocks) if blocks else None

    def _should_search_web(self, query, has_rag_context=False, school_query=False):
        if not self.enable_web_search:
            return False

        if not school_query:
            return True

        keywords = [
            "internet",
            "online",
            "cari",
            "search",
            "google",
            "berita",
            "terbaru",
            "update",
            "informasi terbaru"
        ]
        query_lower = query.lower()
        explicit_search = any(keyword in query_lower for keyword in keywords)

        if school_query and not explicit_search:
            return False

        if self.auto_web_search and not has_rag_context:
            return True

        return explicit_search

    def _search_web(self, query):
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return []

        engine = (os.getenv("SERPAPI_ENGINE") or "google").strip()
        max_results = max(1, min(self.max_web_results, 10))
        hl = (os.getenv("SERPAPI_HL") or "id").strip()
        gl = (os.getenv("SERPAPI_GL") or "id").strip()
        cache_key = f"{engine}|{hl}|{gl}|{self._normalize_query(query)}"
        cached = self.web_cache.get(cache_key)
        now = time.time()
        if cached and now - cached["ts"] < self.web_cache_ttl:
            return cached["results"]
        params = {
            "engine": engine,
            "q": query,
            "api_key": api_key,
            "num": max_results,
            "hl": hl,
            "gl": gl
        }
        url = f"https://serpapi.com/search.json?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=12) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []

        results = []
        for item in payload.get("organic_results", [])[:max_results]:
            title = item.get("title")
            href = item.get("link") or item.get("url")
            snippet = item.get("snippet") or item.get("snippet_highlighted_words")
            if isinstance(snippet, list):
                snippet = " ".join(snippet)
            if title and href:
                results.append({
                    "title": title,
                    "href": href,
                    "snippet": snippet or ""
                })

        if results:
            self.web_cache[cache_key] = {"ts": now, "results": results}
            if len(self.web_cache) > self.web_cache_max:
                oldest = sorted(self.web_cache.items(), key=lambda item: item[1]["ts"])[: max(1, len(self.web_cache) - self.web_cache_max)]
                for key, _ in oldest:
                    self.web_cache.pop(key, None)

        return results

    def extract_file_context(self, filename, content_type, file_bytes, max_chars=6000):
        if not file_bytes:
            return None

        content_type = (content_type or "").lower()
        name = (filename or "").lower()
        text = ""

        if "pdf" in content_type or name.endswith(".pdf"):
            text = self._extract_pdf_text(file_bytes)
        elif any(ext in content_type for ext in ["image/", "png", "jpeg", "jpg", "webp"]) or any(
            name.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]
        ):
            text = self._extract_image_text(file_bytes)
        else:
            return None

        text = (text or "").strip()
        if not text:
            return None
        if max_chars and len(text) > max_chars:
            text = text[:max_chars].rstrip() + "..."
        return text

    def _extract_pdf_text(self, file_bytes):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if page_text:
                    pages.append(page_text.strip())
            return "\n".join(pages).strip()
        except Exception:
            return ""

    def _extract_image_text(self, file_bytes):
        try:
            image = Image.open(io.BytesIO(file_bytes))
        except Exception:
            return ""

        try:
            prompt = (
                "Ekstrak teks penting dari gambar ini dalam bahasa Indonesia. "
                "Jika tidak ada teks, jelaskan isi gambar secara singkat."
            )
            response = self.vision_model.generate_content([prompt, image])
            return (response.text or "").strip()
        except Exception:
            return ""

    def _match_major(self, query, majors):
        query_lower = self._normalize_query(query)
        for major in majors:
            kode = (major.get("kode") or "").lower()
            nama = (major.get("nama") or "").lower()
            if kode and re.search(rf"\b{re.escape(kode)}\b", query_lower):
                return major
            if nama and nama in query_lower:
                return major

        for alias in self._major_aliases():
            if self._contains(query_lower, alias["patterns"]):
                code = alias["code"]
                for major in majors:
                    if (major.get("kode") or "").lower() == code.lower():
                        return major
                return {"kode": code}

        fuzzy_major = self._fuzzy_major_match(query, majors)
        if fuzzy_major:
            return fuzzy_major
        return None

    def _fuzzy_major_match(self, query, majors):
        tokens = [token for token in self._tokenize(query) if len(token) >= 3]
        if not tokens or not majors:
            return None

        keyword_map = self._major_keyword_map()
        for major in majors:
            kode = (major.get("kode") or "").lower()
            nama_tokens = self._tokenize(major.get("nama", ""))
            keywords = keyword_map.get(major.get("kode") or "", [])
            for token in tokens:
                if kode and self._similarity(token, kode) >= 0.86:
                    return major
                for name_token in nama_tokens:
                    if len(name_token) >= 4 and self._similarity(token, name_token) >= 0.88:
                        return major
                for key in keywords:
                    if len(key) >= 4 and self._similarity(token, key) >= 0.9:
                        return major

        return None

    def _extract_major_code(self, query, majors=None):
        query_lower = self._normalize_query(query)
        codes = []
        if majors:
            codes = [major.get("kode") for major in majors if major.get("kode")]
        if not codes:
            codes = ["RPL", "TKJ", "TKR", "TSM", "TO", "LP", "BDP"]
        for code in codes:
            if not code:
                continue
            if re.search(rf"\b{re.escape(code.lower())}\b", query_lower):
                return code

        if majors:
            fuzzy = self._fuzzy_major_match(query, majors)
            if fuzzy and fuzzy.get("kode"):
                return fuzzy.get("kode")
        return None

    def _find_major_ref(self, text, majors):
        if not text or not majors:
            return None

        major = self._match_major(text, majors)
        if major:
            return major

        code = self._extract_major_code(text, majors)
        if code:
            for item in majors:
                if (item.get("kode") or "").lower() == code.lower():
                    return item
            return {"kode": code}

        return None

    def _infer_major_from_history(self, history, majors):
        if not history or not majors:
            return None

        for item in reversed(history):
            if not item:
                continue
            text = item.get("content") or item.get("message") or ""
            major = self._find_major_ref(text, majors)
            if major:
                return major

        return None

    def _apply_history_context(self, user_message, history):
        majors = self.school_data.get("majors", [])
        if not majors or not history:
            return user_message

        if self._find_major_ref(user_message, majors):
            return user_message

        normalized = self._normalize_query(user_message)
        if not self._contains(
            normalized,
            [
                r"\bguru\b",
                r"\bgurunya\b",
                r"\bpengajar\b",
                r"\bngajar\b",
                r"\bmengajar\b",
                r"\bmapel\b",
                r"\bpelajaran\b",
                r"\bfokus\b",
                r"\bbidang\b",
                r"\bbelajar\b",
                r"\bkompetensi\b",
                r"\bkurikulum\b",
                r"\bapa dipelajari\b"
            ]
        ):
            return user_message

        major = self._infer_major_from_history(history, majors)
        if not major:
            return user_message

        kode = major.get("kode")
        nama = major.get("nama")
        if kode:
            return f"{user_message} jurusan {kode}"
        if nama:
            return f"{user_message} jurusan {nama}"

        return user_message

    def _major_aliases(self):
        return [
            {"code": "RPL", "patterns": [r"\brpl\b", r"rekayasa perangkat lunak", r"perangkat lunak", r"software", r"pemrograman", r"programming", r"aplikasi"]},
            {"code": "TKJ", "patterns": [r"\btkj\b", r"teknik komputer", r"komputer dan jaringan", r"jaringan komputer", r"network", r"server", r"router"]},
            {"code": "TKR", "patterns": [r"\btkr\b", r"teknik kendaraan ringan", r"kendaraan ringan", r"mobil", r"otomotif mobil"]},
            {"code": "TSM", "patterns": [r"\btsm\b", r"teknik sepeda motor", r"sepeda motor", r"motor", r"bengkel motor"]},
            {"code": "TO", "patterns": [r"\bto\b", r"ototronik", r"teknik otomotif", r"elektronik otomotif", r"kendaraan pintar"]},
            {"code": "LP", "patterns": [r"\blp\b", r"layanan perbankan", r"perbankan", r"teller", r"bank", r"keuangan"]},
            {"code": "BDP", "patterns": [r"\bbdp\b", r"bisnis daring", r"pemasaran", r"marketing", r"digital marketing", r"jualan online", r"e commerce", r"e-commerce"]}
        ]

    def _detect_teacher_filter(self, query):
        filters = []
        for alias in self._major_aliases():
            filters.append({"label": alias["code"], "patterns": alias["patterns"]})

        subject_aliases = self._subject_aliases()
        for subject in subject_aliases:
            filters.append({"label": subject["label"], "patterns": subject["patterns"]})

        for entry in filters:
            if self._contains(query, entry["patterns"]):
                return entry

        tokens = [token for token in self._tokenize(query) if len(token) >= 3]
        if not tokens:
            return None

        for subject in subject_aliases:
            for token in tokens:
                for keyword in subject.get("keywords", []):
                    if len(keyword) >= 3 and self._similarity(token, keyword) >= 0.9:
                        return {"label": subject["label"], "patterns": subject["patterns"]}

        return None

    def _filter_teachers(self, teachers, patterns):
        filtered = []
        for teacher in teachers:
            if self._is_placeholder_teacher(teacher):
                continue
            teacher_lower = teacher.lower()
            if self._contains(teacher_lower, patterns):
                filtered.append(teacher)
        return filtered

    def _try_answer_from_data(self, user_message):
        data = self.school_data
        if not data:
            return None

        query = self._normalize_query(user_message)
        teachers = self._filter_placeholder_teachers(data.get("teachers", []))
        majors = data.get("majors", [])
        major_match = self._match_major(user_message, majors) if majors else None
        major_code = self._extract_major_code(user_message, majors)
        asks_teacher = self._contains(query, [r"\bguru\b", r"\bpengajar\b", r"\btenaga pengajar\b", r"\bdaftar guru\b", r"\bngajar\b", r"\bmengajar\b"])
        asks_schedule = self._contains(query, [r"\bjadwal\b", r"\bjam pelajaran\b", r"\bjam sekolah\b"])
        asks_subject = self._contains(query, [r"\bmapel\b", r"\bmata pelajaran\b", r"\bpelajaran\b"]) and not asks_schedule
        asks_material = self._contains(
            query,
            [
                r"\bmateri\b",
                r"\bbab\b",
                r"\btopik\b",
                r"\bbelajar\b.*\bapa\b",
                r"\bkurikulum\b"
            ]
        ) and not asks_schedule
        asks_focus = self._contains(query, [r"\bfokus\b", r"\bbidang\b", r"\bbelajar\b", r"\bkompetensi\b", r"\bkurikulum\b", r"\bapa dipelajari\b"])
        asks_teacher_list = self._contains(query, [r"\bdaftar guru\b", r"\bsiapa saja guru\b", r"\bsemua guru\b", r"\bguru di sekolah\b", r"\bguru smk\b"])
        asks_all_majors = self._contains(query, [r"\bsemua jurusan\b", r"\bseluruh jurusan\b", r"\bsemua kompetensi\b", r"\bsemua program\b", r"\bsemua prodi\b"])
        count_terms = {"berapa", "jumlah", "total", "banyak"}
        tokens = set(query.split())
        asks_teacher_count = (tokens & count_terms) and ({"guru", "pengajar"} & tokens)
        asks_major_count = (tokens & count_terms) and ({"jurusan", "kompetensi", "program", "prodi"} & tokens)
        asks_capability = self._contains(
            query,
            [
                r"\bbisa\b.*\bapa\b",
                r"\bbisa\b.*\bjawab\b",
                r"\bbisa\b.*\bbantu\b",
                r"\bkamu bisa apa\b",
                r"\blu bisa apa\b",
                r"\bfitur\b",
                r"\bmenu\b",
                r"\binfo apa saja\b"
            ]
        )

        if asks_capability:
            features = []
            name = data.get("name")
            if name or data.get("address") or data.get("headmaster"):
                features.append("Profil sekolah (nama, alamat, kepala sekolah, profil singkat).")
            if data.get("vision") or data.get("mission") or data.get("goals"):
                features.append("Visi, misi, dan tujuan sekolah.")
            if data.get("advantages"):
                features.append("Keunggulan sekolah dan fasilitas unggulan.")
            if data.get("schedule"):
                features.append("Jadwal pelajaran dan jam sekolah.")
            if data.get("majors"):
                features.append("Jurusan yang tersedia beserta fokus pembelajarannya.")
            if data.get("teachers"):
                features.append("Daftar guru dan mapel yang diampu (termasuk per jurusan).")
            if data.get("quickFacts"):
                features.append("Fakta singkat dan data ringkas sekolah.")

            intro = (
                "Halo! Saya PRISM, asisten AI SMK Pertiwi Kuningan. "
                "Berikut informasi yang bisa saya bantu jelaskan:"
            )
            if features:
                return intro + "\n" + self._format_list(features) + "\n\nSilakan tanya hal spesifik yang kamu butuhkan."
            return "Saya bisa membantu menjawab informasi resmi seputar SMK Pertiwi Kuningan. Silakan tanya hal spesifik yang kamu butuhkan."

        if asks_major_count and majors:
            daftar = [f"{item.get('nama')} ({item.get('kode')})" for item in majors if item.get("nama") and item.get("kode")]
            response = f"Jumlah jurusan: {len(majors)}."
            if daftar:
                response += "\nDaftar jurusan:\n" + self._format_list(daftar)
            return response

        if majors and self._contains(query, [r"\bjurusan\b", r"\bkompetensi\b", r"\bprogram\b", r"\bprodi\b"]) and self._contains(
            query,
            [r"apa saja", r"apa aja", r"\bdaftar\b", r"\bsemua\b", r"\bjurusan apa\b"]
        ):
            daftar = [f"{item.get('nama')} ({item.get('kode')})" for item in majors if item.get("nama") and item.get("kode")]
            if daftar:
                return "Daftar jurusan:\n" + self._format_list(daftar)
            return "Data jurusan tidak tersedia di schoolData.js."

        if asks_teacher_count and teachers:
            if major_match or major_code:
                kode = (major_match.get("kode") if major_match else None) or major_code
                nama = (major_match.get("nama") if major_match else None) or kode
                names = self._get_teachers_by_major(teachers, kode)
                return f"Jumlah guru {nama}: {len(names)}."
            return f"Jumlah guru: {len(teachers)}."

        if asks_all_majors and asks_teacher and majors and teachers:
            lines = []
            for major in majors:
                kode = major.get("kode")
                nama = major.get("nama") or kode
                names = self._get_teachers_by_major(teachers, kode)
                if names:
                    lines.append(f"{nama} ({kode}): " + "; ".join(names))
            if lines:
                return "Guru per jurusan:\n" + self._format_list(lines)

        if (major_match or major_code) and (asks_teacher or asks_subject or asks_focus):
            responses = []
            kode = (major_match.get("kode") if major_match else None) or major_code
            nama = (major_match.get("nama") if major_match else None) or kode
            desc = major_match.get("deskripsi") if major_match else None

            if asks_teacher:
                if teachers:
                    names = self._get_teachers_by_major(teachers, kode)
                    if names:
                        responses.append(f"Guru pengampu {nama}:\n" + self._format_list(names))
                    else:
                        responses.append(f"Data guru untuk {nama} belum tersedia di schoolData.js.")
                else:
                    responses.append("Data guru belum tersedia di schoolData.js.")

            if asks_subject and not asks_teacher:
                if teachers:
                    roles = self._get_roles_by_major(teachers, kode)
                    if roles:
                        responses.append(
                            f"Mapel/kompetensi yang tercatat untuk {nama}:\n"
                            + self._format_list(roles)
                        )
                    else:
                        responses.append("Data mapel per jurusan belum tersedia di schoolData.js.")
                else:
                    responses.append("Data mapel per jurusan belum tersedia di schoolData.js.")

            if asks_focus or asks_subject:
                if desc:
                    responses.append(f"{nama} fokus pada: {desc}")
                else:
                    responses.append(f"Data fokus jurusan {nama} belum tersedia di schoolData.js.")

            if responses:
                return "\n\n".join(responses)

        if asks_material:
            grade, semester = self._extract_grade_semester(user_message)
            labels = []
            matched_teacher = self._match_teacher_entry(user_message, teachers)
            if matched_teacher and matched_teacher["roles"]:
                labels.extend([self._normalize_role_label(role) or role for role in matched_teacher["roles"]])

            teacher_filter = self._detect_teacher_filter(query)
            if teacher_filter:
                labels.append(teacher_filter["label"])

            if major_match or major_code:
                labels.append((major_match.get("kode") if major_match else None) or major_code)

            labels = [label for label in labels if label]
            materials_responses = []
            for label in self._dedupe_preserve(labels):
                key = self._material_label_key(label)
                materials = self.materials_catalog.get(key) if self.materials_catalog else None
                if materials:
                    materials_responses.append(
                        self._format_materials(materials["label"], materials["grades"], grade=grade, semester=semester)
                    )

            if materials_responses:
                return "\n\n".join(materials_responses)

            if labels:
                return "Materi detail untuk mapel tersebut belum tersedia. Sebutkan mapel/jurusan yang jelas agar saya bisa bantu."
            return "Maksudnya materi mapel apa? Contoh: Matematika, Bahasa Indonesia, RPL, TKJ."

        if teachers and (asks_teacher or asks_subject):
            matched_teacher = self._match_teacher_entry(user_message, teachers)
            if matched_teacher:
                if matched_teacher["roles"]:
                    normalized_roles = [
                        self._normalize_role_label(role) or role
                        for role in matched_teacher["roles"]
                    ]
                    roles_text = ", ".join(normalized_roles)
                    return f"{matched_teacher['name']} mengajar: {roles_text}."
                return f"Data mapel untuk {matched_teacher['name']} belum tersedia di schoolData.js."

            if asks_teacher and major_code:
                names = self._get_teachers_by_major(teachers, major_code)
                if names:
                    return f"Guru pengampu {major_code}:\n" + self._format_list(names)
                return f"Data guru untuk {major_code} belum tersedia di schoolData.js."

            if asks_teacher_list:
                return "Daftar guru:\n" + self._format_list(teachers)

            if asks_teacher and not major_match and not major_code:
                jurusan_opsi = []
                for item in majors:
                    kode = item.get("kode")
                    nama = item.get("nama")
                    if kode and nama:
                        jurusan_opsi.append(f"{nama} ({kode})")
                    elif kode:
                        jurusan_opsi.append(kode)
                if jurusan_opsi:
                    return "Maksudnya guru jurusan apa? Contoh:\n" + self._format_list(jurusan_opsi)
                return "Maksudnya guru jurusan apa?"

            roles = self._get_unique_roles(teachers)
            if roles:
                return "Daftar mapel/kompetensi dari data guru:\n" + self._format_list(roles)

        if self._contains(query, [r"\bkepsek\b", r"\bkepala sekolah\b"]):
            name = data.get("headmaster")
            if name:
                return f"Kepala sekolah SMK Pertiwi Kuningan: {name}."
            return "Data kepala sekolah belum tersedia di schoolData.js."

        if self._contains(query, [r"\balamat\b", r"\blokasi\b", r"\bdi mana\b", r"\bdimana\b", r"\bletak\b"]):
            address = data.get("address")
            if address:
                return f"Alamat SMK Pertiwi Kuningan: {address}."
            return "Data alamat sekolah belum tersedia di schoolData.js."

        if self._contains(query, [r"\bnama sekolah\b", r"\bnama lengkap\b"]):
            name = data.get("name")
            if name:
                return f"Nama sekolah: {name}."
            return "Data nama sekolah belum tersedia di schoolData.js."

        if majors:
            major_match = major_match or self._match_major(user_message, majors)
            is_teacher_query = asks_teacher or asks_subject
            if major_match and not is_teacher_query:
                nama = major_match.get("nama")
                kode = major_match.get("kode")
                desc = major_match.get("deskripsi")
                if nama and kode and desc:
                    return f"{nama} ({kode}): {desc}"
                if nama and desc:
                    return f"{nama}: {desc}"
                if kode and desc:
                    return f"{kode}: {desc}"

            if self._contains(query, [r"\bjurusan\b", r"\bkompetensi\b", r"\bprogram\b"]) and self._contains(query, [r"apa saja", r"apa aja", r"daftar", r"\bsemua\b"]):
                daftar = [f"{item.get('nama')} ({item.get('kode')})" for item in majors if item.get("nama") and item.get("kode")]
                if daftar:
                    return "Daftar jurusan:\n" + self._format_list(daftar)

        if "visi" in query and "misi" in query:
            vision = data.get("vision")
            mission = data.get("mission", [])
            if vision or mission:
                response = []
                if vision:
                    response.append(f"Visi: {vision}")
                if mission:
                    response.append("Misi:\n" + self._format_list(mission))
                return "\n".join(response)
            return "Data visi dan misi belum tersedia di schoolData.js."

        if "visi" in query:
            vision = data.get("vision")
            if vision:
                return f"Visi: {vision}"
            return "Data visi belum tersedia di schoolData.js."

        if "misi" in query:
            mission = data.get("mission", [])
            if mission:
                return "Misi:\n" + self._format_list(mission)
            return "Data misi belum tersedia di schoolData.js."

        if self._contains(query, [r"\btujuan\b", r"\bgoals?\b"]):
            goals = data.get("goals", [])
            if goals:
                return "Tujuan sekolah:\n" + self._format_list(goals)
            return "Data tujuan sekolah belum tersedia di schoolData.js."

        if self._contains(query, [r"\bsejarah\b", r"\bprofil\b", r"\btentang sekolah\b"]):
            history = data.get("history")
            if history:
                return f"Profil singkat: {history}"
            return "Data profil sekolah belum tersedia di schoolData.js."

        if self._contains(query, [
            r"\bkeunggul\w*\b",
            r"\bunggulan\w*\b",
            r"\bkelebih\w*\b",
            r"\bkeistimewa\w*\b",
            r"\bnilai tambah\b",
            r"\bnilai plus\b"
        ]):
            advantages = data.get("advantages", [])
            if advantages:
                return "Keunggulan sekolah:\n" + self._format_list(advantages)
            return "Data keunggulan sekolah belum tersedia di schoolData.js."

        if self._contains(query, [r"\bfakta\b", r"\bquick facts?\b", r"\bdata singkat\b"]):
            quick_facts = data.get("quickFacts", [])
            if quick_facts:
                return "Fakta singkat:\n" + self._format_list(quick_facts)
            return "Data fakta singkat belum tersedia di schoolData.js."

        if asks_schedule:
            schedule = data.get("schedule", [])
            if schedule:
                return "Jadwal pelajaran:\n" + self._format_list(schedule)
            return "Data jadwal pelajaran belum tersedia di schoolData.js."

        if self._contains(query, [r"\bguru\b", r"\bpengajar\b", r"\btenaga pengajar\b", r"\bdaftar guru\b", r"\bngajar\b", r"\bmengajar\b"]):
            if not teachers:
                return "Data guru belum tersedia di schoolData.js."

            teacher_filter = self._detect_teacher_filter(query)
            if teacher_filter:
                filtered = self._filter_teachers(teachers, teacher_filter["patterns"])
                if not filtered:
                    return f"Data guru untuk {teacher_filter['label']} belum tersedia di schoolData.js."
                return f"Daftar guru {teacher_filter['label']}:\n" + self._format_list(filtered)

            return "Daftar guru:\n" + self._format_list(teachers)

        return None

    def get_response(self, user_message: str, memory=None, file_context=None):
        try:
            self._refresh_school_data()
            file_hint = False
            if file_context:
                normalized = self._normalize_query(user_message)
                file_hint = self._contains(
                    normalized,
                    [
                        r"\bfile\b",
                        r"\bdokumen\b",
                        r"\blampiran\b",
                        r"\bbrosur\b",
                        r"\bpdf\b",
                        r"\bgambar\b",
                        r"\bfoto\b"
                    ]
                )

            direct_answer = self._try_answer_from_data(user_message)

            school_query = self._is_school_query_strict(user_message)
            rag_context = self._build_rag_context(user_message) if school_query else None
            web_results = []
            prompt = user_message
            memory_context = None
            if memory and not school_query:
                safe_memory = [item.strip() for item in memory if isinstance(item, str) and item.strip()]
                if safe_memory:
                    memory_context = "\n".join(f"- {item}" for item in safe_memory[:12])

            context_blocks = []
            if direct_answer:
                context_blocks.append(f"INFORMASI PASTI DARI SISTEM (Gunakan ini sebagai jawaban utama, tapi sampaikan dengan gaya natural):\n{direct_answer}")
            if file_context:
                context_blocks.append("KONTEKS FILE:\n" + file_context)
            if rag_context:
                context_blocks.append("KONTEKS SEKOLAH:\n" + rag_context)

            should_search = self._should_search_web(
                user_message,
                has_rag_context=bool(rag_context),
                school_query=school_query
            )
            if file_context:
                short_query = len(self._normalize_query(user_message).split()) <= 3
                file_hint = file_hint or short_query or self._contains(
                    self._normalize_query(user_message),
                    [r"\bini\b", r"\bitu\b", r"\bini apa\b", r"\bjelasin\b"]
                )

            if direct_answer:
                should_search = False

            if file_hint:
                should_search = False

            if should_search:
                web_results = self._search_web(user_message)
                if web_results:
                    search_lines = [
                        f"- {item['title']}: {item['snippet']} ({item['href']})"
                        for item in web_results
                    ]
                    context_intro = ""
                    if context_blocks:
                        context_intro = "\n\n".join(context_blocks) + "\n\n"
                        prompt = (
                            (f"RIWAYAT PENGGUNA:\n{memory_context}\n\n" if memory_context else "")
                            + context_intro
                            + "HASIL PENCARIAN INTERNET:\n"
                            + f"{'\n'.join(search_lines)}\n\n"
                            + f"Pertanyaan: {user_message}\n"
                            + "Jawab berdasarkan hasil pencarian. Gunakan konteks file jika relevan. Sertakan daftar sumber."
                        )
                elif context_blocks:
                    prompt = (
                        "\n\n".join(context_blocks)
                        + "\n\n"
                        + f"Pertanyaan: {user_message}\n"
                        + "Gunakan konteks di atas jika relevan. Jika konteks file tidak relevan, abaikan."
                    )
                elif memory_context:
                    prompt = (
                        f"RIWAYAT PENGGUNA:\n{memory_context}\n\n"
                        f"Pertanyaan: {user_message}\n"
                        "Jawab secara jelas dan ringkas."
                    )
            elif context_blocks:
                prompt = (
                    "\n\n".join(context_blocks)
                    + "\n\n"
                    + f"Pertanyaan: {user_message}\n"
                    + "Gunakan konteks di atas jika relevan. Jika konteks file tidak relevan, abaikan."
                )
            elif memory_context:
                prompt = (
                    f"RIWAYAT PENGGUNA:\n{memory_context}\n\n"
                    f"Pertanyaan: {user_message}\n"
                    "Jawab secara jelas dan ringkas."
                )
            else:
                # Fallback prompt if no context but we want Gemini behavior
                prompt = (
                    f"Pertanyaan: {user_message}\n"
                    "Jawab dengan baik dan informatif."
                )

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.65,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=1500,
                )
            )

            message = response.text
            if web_results and "Sumber" not in message:
                sources = "\n".join([f"- {item['title']}: {item['href']}" for item in web_results])
                message = f"{message}\n\nSumber:\n{sources}"

            if direct_answer:
                source_label = "schoolData"
            elif rag_context:
                source_label = "schoolData"
            elif web_results:
                source_label = "web"
            elif file_context:
                source_label = "file"
            else:
                source_label = "model"

            return {
                "success": True,
                "message": message,
                "source": source_label
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Maaf, terjadi kesalahan: {str(e)}",
                "error": str(e)
            }

    async def get_response_stream(self, user_message: str, history: list = None, memory=None, file_context=None, language: str = "id"):
        """Generator to stream response chunks"""
        try:
            self._refresh_school_data()
            
            # Language Instruction
            lang_instruction = ""
            if language == "en":
                lang_instruction = "\n\n(IMPORTANT: Please answer in ENGLISH)"
            elif language == "su":
                lang_instruction = "\n\n(PENTING: Jawab menggunakan BAHASA SUNDA yang sopan/lemes)"
            elif language == "jw":
                lang_instruction = "\n\n(PENTING: Jawab menggunakan BAHASA JAWA yang sopan)"
            
            file_hint = False
            if file_context:
                normalized = self._normalize_query(user_message)
                file_hint = self._contains(
                    normalized,
                    [r"\bfile\b", r"\bdokumen\b", r"\blampiran\b", r"\bbrosur\b", r"\bpdf\b", r"\bgambar\b", r"\bfoto\b"]
                )

            direct_answer = self._try_answer_from_data(user_message)
            
            # If we have a direct answer, yield it immediately and return
            if direct_answer:
                yield json.dumps({"type": "chunk", "content": direct_answer}) + "\n"
                yield json.dumps({"type": "source", "label": "schoolData"}) + "\n"
                return

            school_query = self._is_school_query_strict(user_message)
            rag_context = self._build_rag_context(user_message) if school_query else None
            web_results = []
            prompt = user_message
            memory_context = None
            
            if memory and not school_query:
                safe_memory = [item.strip() for item in memory if isinstance(item, str) and item.strip()]
                if safe_memory:
                    memory_context = "\n".join(f"- {item}" for item in safe_memory[:12])

            context_blocks = []
            if file_context:
                context_blocks.append("KONTEKS FILE:\n" + file_context)
            if rag_context:
                context_blocks.append("KONTEKS SEKOLAH:\n" + rag_context)

            should_search = self._should_search_web(
                user_message,
                has_rag_context=bool(rag_context),
                school_query=school_query
            )
            
            if file_context:
                short_query = len(self._normalize_query(user_message).split()) <= 3
                file_hint = file_hint or short_query or self._contains(
                    self._normalize_query(user_message),
                    [r"\bini\b", r"\bitu\b", r"\bini apa\b", r"\bjelasin\b"]
                )

            if file_hint:
                should_search = False

            source_label = "model"
            if rag_context:
                source_label = "schoolData"
            elif file_context:
                source_label = "file"

            if should_search:
                web_results = await run_in_threadpool(self._search_web, user_message)
                if web_results:
                    source_label = "web"
                    search_lines = [
                        f"- {item['title']}: {item['snippet']} ({item['href']})"
                        for item in web_results
                    ]
                    context_intro = ""
                    if context_blocks:
                        context_intro = "\n\n".join(context_blocks) + "\n\n"
                    
                    history_text = ""
                    if history:
                        history_text = "RIWAYAT CHAT:\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-5:]]) + "\n\n"

                    prompt = (
                        (f"RIWAYAT PENGGUNA:\n{memory_context}\n\n" if memory_context else "")
                        + history_text
                        + context_intro
                        + "HASIL PENCARIAN INTERNET:\n"
                        + f"{'\n'.join(search_lines)}\n\n"
                        + f"Pertanyaan: {user_message}\n"
                        + "Jawab berdasarkan hasil pencarian. Gunakan konteks file jika relevan. Sertakan daftar sumber."
                    )
                elif context_blocks:
                    prompt = (
                        "\n\n".join(context_blocks)
                        + "\n\n"
                        + f"Pertanyaan: {user_message}\n"
                        + "Gunakan konteks di atas jika relevan. Jika konteks file tidak relevan, abaikan."
                    )
            elif context_blocks:
                prompt = (
                    "\n\n".join(context_blocks)
                    + "\n\n"
                    + f"Pertanyaan: {user_message}\n"
                    + "Gunakan konteks di atas jika relevan. Jika konteks file tidak relevan, abaikan."
                )
            elif memory_context:
                prompt = (
                    f"RIWAYAT PENGGUNA:\n{memory_context}\n\n"
                    f"Pertanyaan: {user_message}\n"
                    "Jawab secara jelas dan ringkas."
                )
            elif history:
                 # Apply history if available and no other context override
                prompt = self._apply_history_context(user_message, history)

            # Append Language Instruction
            if lang_instruction:
                prompt += lang_instruction

            response_stream = await self.model.generate_content_async(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.65,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=1500,
                )
            )

            async for chunk in response_stream:
                if chunk.text:
                    yield json.dumps({"type": "chunk", "content": chunk.text}) + "\n"
            
            # Send source info at the end
            if web_results:
                sources = [{"label": item['title'], "url": item['href']} for item in web_results]
                yield json.dumps({"type": "source", "label": "web", "details": sources}) + "\n"
            else:
                 yield json.dumps({"type": "source", "label": source_label}) + "\n"

        except Exception as e:
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"
            
    def _apply_history_context(self, user_message, history):
        if not history:
            return user_message
        
        # Take last 5 turns
        relevant = history[-10:]
        transcript = []
        for msg in relevant:
            role = "Model" if msg.get("role") == "assistant" else "User"
            content = msg.get("message") or msg.get("content") or ""
            transcript.append(f"{role}: {content}")
            
        context = "\n".join(transcript)
        return (
            f"RIWAYAT PERCAKAPAN:\n{context}\n\n"
            f"User: {user_message}\n"
            "Model (lanjutkan respons):"
        )


# Instance global
chatbot = SMKPertiwiChatbot()
