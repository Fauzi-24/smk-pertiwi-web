"""
Email service for sending notifications to students and admins.
Uses Gmail SMTP with TLS encryption.
"""

import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Email configuration - will be loaded from environment variables
EMAIL_CONFIG = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': 'ozieefauzi599@gmail.com',  # Will be replaced by env var
    'password': '',  # Will be set from env var - USE APP PASSWORD
    'from_name': 'SMK Pertiwi Kuningan',
    'from_email': 'ozieefauzi599@gmail.com'
}

def set_email_credentials(username: str, password: str):
    """Set email credentials from environment variables"""
    EMAIL_CONFIG['username'] = username
    EMAIL_CONFIG['from_email'] = username
    EMAIL_CONFIG['password'] = password

def create_registration_email(student_name: str, nisn: str, major: str) -> str:
    """Create registration confirmation email HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; border-left: 4px solid #2563eb; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6b7280; font-size: 14px; }}
            .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Pendaftaran Berhasil!</h1>
                <p>PPDB SMK Pertiwi Kuningan</p>
            </div>
            <div class="content">
                <p>Yth. <strong>{student_name}</strong>,</p>
                
                <p>Terima kasih telah mendaftar di <strong>SMK Pertiwi Kuningan</strong>. Pendaftaran Anda telah kami terima dan sedang dalam proses verifikasi.</p>
                
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #2563eb;">📋 Detail Pendaftaran</h3>
                    <p><strong>NISN:</strong> {nisn}<br>
                    <strong>Jurusan Pilihan:</strong> {major}<br>
                    <strong>Tanggal Daftar:</strong> {datetime.now().strftime('%d %B %Y, %H:%M WIB')}</p>
                </div>
                
                <h3>📌 Langkah Selanjutnya:</h3>
                <ol>
                    <li>Tim admin kami akan memverifikasi data Anda</li>
                    <li>Anda akan menerima email notifikasi hasil seleksi</li>
                    <li>Proses verifikasi memakan waktu 1-3 hari kerja</li>
                </ol>
                
                <p><strong>Catatan Penting:</strong></p>
                <ul>
                    <li>Pastikan email Anda aktif untuk menerima notifikasi</li>
                    <li>Simpan NISN Anda untuk keperluan tracking</li>
                    <li>Jika ada pertanyaan, hubungi kami via WhatsApp</li>
                </ul>
                
                <div style="text-align: center;">
                    <a href="https://wa.me/6281234567890?text=Halo,%20saya%20telah%20mendaftar%20PPDB%20dengan%20NISN%20{nisn}" class="button">
                        💬 Hubungi Admin
                    </a>
                </div>
            </div>
            <div class="footer">
                <p><strong>SMK Pertiwi Kuningan</strong><br>
                Jalan Siliwangi No. 26A, Kasturi, Kuningan, Jawa Barat<br>
                📞 (0232) 871146 | 📧 info@smkpertiwi.sch.id</p>
                <p style="font-size: 12px; color: #9ca3af;">
                    Email ini dikirim secara otomatis. Mohon tidak membalas email ini.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def create_acceptance_email(student_name: str, nisn: str, major: str) -> str:
    """Create acceptance notification email HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); color: white; padding: 40px 20px; text-align: center; }}
            .logo-text {{ font-size: 24px; font-weight: bold; margin: 0; }}
            .content {{ background: #ffffff; padding: 40px; }}
            .status-box {{ background: #f0fdf4; border: 2px solid #16a34a; padding: 20px; border-radius: 8px; text-align: center; margin: 25px 0; }}
            .status-title {{ color: #16a34a; font-size: 20px; font-weight: bold; margin: 0 0 5px 0; text-transform: uppercase; }}
            .status-text {{ font-size: 16px; margin: 0; }}
            .details-box {{ background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 25px; border-left: 4px solid #16a34a; }}
            .details-row {{ margin-bottom: 10px; display: flex; }}
            .details-label {{ font-weight: bold; width: 140px; color: #64748b; }}
            .details-value {{ flex: 1; color: #0f172a; font-weight: 500; }}
            .steps-box {{ margin-top: 30px; }}
            .step-item {{ margin-bottom: 15px; padding-left: 10px; border-left: 3px solid #e2e8f0; }}
            .footer {{ background: #f1f5f9; text-align: center; padding: 20px; font-size: 12px; color: #64748b; }}
            .button {{ display: inline-block; background: #16a34a; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 10px; }}
            .button:hover {{ background: #15803d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-text">SMK PERTIWI KUNINGAN</div>
                <p style="margin: 10px 0 0; opacity: 0.9;">Panitia Penerimaan Peserta Didik Baru</p>
            </div>
            <div class="content">
                <p>Yth. Calon Peserta Didik,</p>
                <p style="font-size: 18px; font-weight: bold; margin: 5px 0 20px;">Ananda {student_name}</p>
                
                <p>Berdasarkan hasil seleksi administrasi dan verifikasi data yang telah dilakukan oleh Panitia PPDB SMK Pertiwi Kuningan, dengan ini kami memberitahukan bahwa Anda dinyatakan:</p>
                
                <div class="status-box">
                    <div class="status-title">LULUS SELEKSI / DITERIMA</div>
                    <p class="status-text">Selamat Bergabung di SMK Pertiwi Kuningan!</p>
                </div>
                
                <div class="details-box">
                    <div class="details-row">
                        <div class="details-label">NISN</div>
                        <div class="details-value">: {nisn}</div>
                    </div>
                    <div class="details-row">
                        <div class="details-label">Kompetensi Keahlian</div>
                        <div class="details-value">: {major}</div>
                    </div>
                    <div class="details-row">
                        <div class="details-label">Tahun Ajaran</div>
                        <div class="details-value">: {datetime.now().year}/{datetime.now().year + 1}</div>
                    </div>
                </div>
                
                <div class="steps-box">
                    <h3>Langkah Selanjutnya:</h3>
                    <p>Wajib melakukan <strong>Daftar Ulang</strong> dengan membawa berkas asli ke Sekretariat PPDB:</p>
                    <div class="step-item">
                        <strong>1. Dokumen Persyaratan</strong><br>
                        Membawa bukti pendaftaran, Ijazah/SKL asli, KK, dan Akte Kelahiran.
                    </div>
                    <div class="step-item">
                        <strong>2. Waktu Pelaksanaan</strong><br>
                        Senin - Sabtu, Pukul 08.00 - 14.00 WIB.
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 35px;">
                    <a href="https://wa.me/6281234567890?text=Assalamualaikum,%20saya%20{student_name}%20(NISN:{nisn})%20ingin%20konfirmasi%20daftar%20ulang" class="button">
                        Konfirmasi Daftar Ulang via WhatsApp
                    </a>
                </div>
            </div>
            <div class="footer">
                <p><strong>SMK PERTIWI KUNINGAN</strong><br>
                Jl. Siliwangi No. 26A, Kasturi, Kuningan, Jawa Barat<br>
                Telp: (0232) 871146 | Website: smkpertiwi.sch.id</p>
                <p style="margin-top: 10px;"><em>Email ini dibuat secara otomatis oleh sistem.</em></p>
            </div>
        </div>
    </body>
    </html>
    """

def create_rejection_email(student_name: str, nisn: str) -> str:
    """Create rejection notification email HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%); color: white; padding: 40px 20px; text-align: center; }}
            .logo-text {{ font-size: 24px; font-weight: bold; margin: 0; }}
            .content {{ background: #ffffff; padding: 40px; }}
            .status-box {{ background: #fef2f2; border: 2px solid #ef4444; padding: 20px; border-radius: 8px; text-align: center; margin: 25px 0; }}
            .status-title {{ color: #ef4444; font-size: 20px; font-weight: bold; margin: 0 0 5px 0; text-transform: uppercase; }}
            .status-text {{ font-size: 16px; margin: 0; }}
            .footer {{ background: #f1f5f9; text-align: center; padding: 20px; font-size: 12px; color: #64748b; }}
            .button {{ display: inline-block; background: #64748b; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 10px; }}
            .button:hover {{ background: #475569; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-text">SMK PERTIWI KUNINGAN</div>
                <p style="margin: 10px 0 0; opacity: 0.9;">Panitia Penerimaan Peserta Didik Baru</p>
            </div>
            <div class="content">
                <p>Yth. Calon Peserta Didik,</p>
                <p style="font-size: 18px; font-weight: bold; margin: 5px 0 20px;">Ananda {student_name}</p>
                
                <p>Terima kasih atas kepercayaan Anda mendaftar di SMK Pertiwi Kuningan. Panitia PPDB telah melakukan verifikasi berkas dan seleksi administrasi terhadap data yang Anda kirimkan.</p>
                
                <p>Berdasarkan hasil seleksi tersebut, dengan berat hati kami sampaikan bahwa Anda dinyatakan:</p>
                
                <div class="status-box">
                    <div class="status-title">TIDAK DITERIMA</div>
                    <p class="status-text">Mohon maaf, Anda belum memenuhi kriteria seleksi.</p>
                </div>
                
                <p>Keputusan ini bersifat mutlak. Jangan berkecil hati, kegagalan adalah kesuksesan yang tertunda. Kami mendoakan kesuksesan Anda di tempat pendidikan yang lain.</p>
                
                <div style="text-align: center; margin-top: 35px;">
                    <a href="https://wa.me/6281234567890?text=Assalamualaikum,%20saya%20{student_name}%20(NISN:{nisn})%20ingin%20konsultasi%20hasil%20seleksi" class="button">
                        Konsultasi dengan Admin
                    </a>
                </div>
            </div>
            <div class="footer">
                <p><strong>SMK PERTIWI KUNINGAN</strong><br>
                Jl. Siliwangi No. 26A, Kasturi, Kuningan, Jawa Barat<br>
                Telp: (0232) 871146 | Website: smkpertiwi.sch.id</p>
            </div>
        </div>
    </body>
    </html>
    """

async def send_email_async(
    to_email: str,
    subject: str,
    html_content: str,
    to_name: Optional[str] = None
) -> bool:
    """
    Send email asynchronously using Gmail SMTP.
    Returns True if successful, False otherwise.
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((EMAIL_CONFIG['from_name'], EMAIL_CONFIG['from_email']))
        msg['To'] = formataddr((to_name or to_email, to_email))
        msg['Subject'] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Send email in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _send_email_sync, msg, to_email)
        
        logger.info(f"Email sent successfully to {to_email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def _send_email_sync(msg: MIMEMultipart, to_email: str):
    """Synchronous email sending (called in thread pool)"""
    with smtplib.SMTP(EMAIL_CONFIG['host'], EMAIL_CONFIG['port']) as server:
        server.starttls()  # Enable TLS
        server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
        server.send_message(msg)

# Convenience functions for specific email types
async def send_registration_email(student_email: str, student_name: str, nisn: str, major: str) -> bool:
    """Send registration confirmation email"""
    subject = "✅ Konfirmasi Pendaftaran PPDB - SMK Pertiwi Kuningan"
    html = create_registration_email(student_name, nisn, major)
    return await send_email_async(student_email, subject, html, student_name)

async def send_acceptance_email(student_email: str, student_name: str, nisn: str, major: str) -> bool:
    """Send acceptance notification email"""
    subject = "🎉 SELAMAT! Anda Diterima di SMK Pertiwi Kuningan"
    html = create_acceptance_email(student_name, nisn, major)
    return await send_email_async(student_email, subject, html, student_name)

async def send_rejection_email(student_email: str, student_name: str, nisn: str) -> bool:
    """Send rejection notification email"""
    subject = "Pemberitahuan Hasil Seleksi PPDB - SMK Pertiwi Kuningan"
    html = create_rejection_email(student_name, nisn)
    return await send_email_async(student_email, subject, html, student_name)
