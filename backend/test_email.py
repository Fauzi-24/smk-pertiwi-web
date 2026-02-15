"""
Email System Test Script
Test email templates and sending functionality
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services import email_service
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

def print_section(title):
    print(f"\n{'─'*60}")
    print(f"📧 {title}")
    print('─'*60)

def preview_email_template(template_name, html_content):
    """Preview email template in console"""
    print_section(f"Template Preview: {template_name}")
    
    # Extract key parts from HTML
    import re
    
    # Extract title
    title_match = re.search(r'<h1>(.*?)</h1>', html_content, re.DOTALL)
    if title_match:
        print(f"📌 Title: {title_match.group(1).strip()}")
    
    # Extract subject line (from greeting)
    greeting_match = re.search(r'Yth\. <strong>(.*?)</strong>', html_content)
    if greeting_match:
        print(f"👤 To: {greeting_match.group(1).strip()}")
    
    # Show template size
    print(f"📏 Template Size: {len(html_content)} characters")
    print(f"✅ Template Generated Successfully!")
    
    # Save to file for viewing
    filename = f"preview_{template_name.lower().replace(' ', '_')}.html"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"💾 Saved preview to: {filepath}")
    print(f"   Open in browser to see full email!")

async def test_email_templates():
    """Test all email template generation"""
    print_separator("EMAIL TEMPLATE GENERATION TEST")
    
    # Test data
    student_name = "Fauzi Ahmad"
    nisn = "1234567890"
    major = "Teknik Komputer dan Jaringan"
    
    print("\n🧪 Testing with sample data:")
    print(f"   Name: {student_name}")
    print(f"   NISN: {nisn}")
    print(f"   Major: {major}")
    
    # Test 1: Registration Email
    try:
        html = email_service.create_registration_email(student_name, nisn, major)
        preview_email_template("Registration Confirmation", html)
    except Exception as e:
        print(f"❌ Registration email failed: {e}")
    
    # Test 2: Acceptance Email
    try:
        html = email_service.create_acceptance_email(student_name, nisn, major)
        preview_email_template("Acceptance Notification", html)
    except Exception as e:
        print(f"❌ Acceptance email failed: {e}")
    
    # Test 3: Rejection Email
    try:
        html = email_service.create_rejection_email(student_name, nisn)
        preview_email_template("Rejection Notification", html)
    except Exception as e:
        print(f"❌ Rejection email failed: {e}")

async def test_email_sending():
    """Test actual email sending"""
    print_separator("EMAIL SENDING TEST")
    
    # Check if credentials are configured
    email_user = os.getenv('EMAIL_USER', '')
    email_password = os.getenv('EMAIL_PASSWORD', '')
    
    print(f"\n🔐 Email Configuration:")
    print(f"   Host: {os.getenv('EMAIL_HOST', 'smtp.gmail.com')}")
    print(f"   Port: {os.getenv('EMAIL_PORT', '587')}")
    print(f"   User: {email_user}")
    print(f"   Password: {'✅ Set' if email_password and email_password != 'YOUR_GMAIL_APP_PASSWORD_HERE' else '❌ NOT SET'}")
    
    if not email_password or email_password == 'YOUR_GMAIL_APP_PASSWORD_HERE':
        print("\n⚠️  Gmail App Password not configured!")
        print("   Set EMAIL_PASSWORD in backend/.env to test sending")
        print("\n📝 To setup:")
        print("   1. Go to https://myaccount.google.com/security")
        print("   2. Enable 2-Step Verification")
        print("   3. Generate App Password")
        print("   4. Update EMAIL_PASSWORD in .env")
        return
    
    # Initialize email service
    try:
        email_service.set_email_credentials(email_user, email_password)
        print("\n✅ Email service initialized!")
    except Exception as e:
        print(f"\n❌ Failed to initialize email service: {e}")
        return
    
    # Test email
    test_email = "fauziiii7888@gmail.com"
    student_name = "Fauzi (Test Student)"
    nisn = "9999999999"
    major = "Teknik Komputer dan Jaringan"
    
    print(f"\n📧 Sending test email to: {test_email}")
    print(f"   Student: {student_name}")
    print(f"   NISN: {nisn}")
    
    # Try sending registration email
    try:
        print("\n📤 Sending registration confirmation email...")
        success = await email_service.send_registration_email(
            student_email=test_email,
            student_name=student_name,
            nisn=nisn,
            major=major
        )
        
        if success:
            print("✅ Registration email sent successfully!")
            print(f"   Check inbox at: {test_email}")
            print("   (Check spam folder if not in inbox)")
        else:
            print("❌ Failed to send registration email")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*17 + "EMAIL SYSTEM TEST" + " "*24 + "║")
    print("║" + " "*14 + "SMK Pertiwi Kuningan" + " "*25 + "║")
    print("╚" + "═"*58 + "╝")
    
    # Run template tests
    await test_email_templates()
    
    # Run sending test
    await test_email_sending()
    
    print_separator("TEST COMPLETE")
    print("\n✅ All tests completed!")
    print("\n📁 Preview HTML files saved in current directory")
    print("   Open them in browser to see email design")
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
