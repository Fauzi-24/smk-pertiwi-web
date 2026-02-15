"""
Quick Email Test with Better Error Handling
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_gmail_connection():
    """Test Gmail SMTP connection"""
    
    email_user = os.getenv('EMAIL_USER', 'ozieefauzi@gmail.com')
    email_pass = os.getenv('EMAIL_PASSWORD', '')
    
    print("="*60)
    print("GMAIL SMTP CONNECTION TEST")
    print("="*60)
    print(f"\nEmail: {email_user}")
    print(f"Password length: {len(email_pass)} characters")
    print(f"Password (masked): {'*' * len(email_pass)}")
    
    if not email_pass or email_pass == 'YOUR_GMAIL_APP_PASSWORD_HERE':
        print("\n❌ ERROR: Email password not set!")
        return False
    
    print("\n🔌 Connecting to Gmail SMTP...")
    print(f"   Host: smtp.gmail.com")
    print(f"   Port: 587")
    
    try:
        # Create SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(0)  # Set to 1 for verbose output
        
        print("✅ Connected to SMTP server")
        
        # Start TLS
        print("🔐 Starting TLS encryption...")
        server.starttls()
        print("✅ TLS started")
        
        # Login
        print(f"🔑 Logging in as {email_user}...")
        server.login(email_user, email_pass)
        print("✅ Login successful!")
        
        # Test email
        test_to = "fauziiii7888@gmail.com"
        print(f"\n📧 Sending test email to {test_to}...")
        
        msg = MIMEMultipart()
        msg['From'] = formataddr(('SMK Pertiwi Kuningan', email_user))
        msg['To'] = test_to
        msg['Subject'] = "✅ TEST EMAIL - SMK Pertiwi System"
        
        body = """
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2 style="color: #2563eb;">✅ Email System Test Berhasil!</h2>
            <p>Halo! Ini adalah email test dari sistem PPDB SMK Pertiwi Kuningan.</p>
            <p>Jika kamu menerima email ini, berarti <strong>email notification system sudah berfungsi dengan baik!</strong> 🎉</p>
            <hr>
            <p style="color: #666; font-size: 12px;">
                Email ini dikirim otomatis dari sistem testing.<br>
                SMK Pertiwi Kuningan - {email_user}
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        server.send_message(msg)
        
        print("✅ Email sent successfully!")
        print(f"\n📬 Check inbox at: {test_to}")
        print("   (Also check spam/junk folder)")
        
        server.quit()
        print("\n🎉 TEST PASSED - Email system working!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR!")
        print(f"   Error: {e}")
        print("\n💡 Possible solutions:")
        print("   1. Check if App Password is correct")
        print("   2. Make sure 2-Step Verification is enabled")
        print("   3. Generate new App Password")
        print("   4. Check if @ in email is correct: ozieefauzi@gmail.com")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"   Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("\n")
    success = test_gmail_connection()
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TEST FAILED - See errors above")
    print("="*60 + "\n")
