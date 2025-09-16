#!/usr/bin/env python3
"""
Debug email functionality
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_gmail_connection():
    """Test direct Gmail SMTP connection"""
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    print(f"Testing Gmail SMTP connection...")
    print(f"Username: {username}")
    print(f"Password: {'***' if password else 'NOT SET'}")

    if not username or not password:
        print("❌ Email credentials not found in .env file")
        return False

    try:
        # Test SMTP connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print("✅ TLS connection established")

        # Test authentication
        server.login(username, password)
        print("✅ Authentication successful")

        # Test sending a simple email
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = username  # Send to self for testing
        msg['Subject'] = "Rent Hunting AI - Email Test"

        body = "This is a test email from the Rent Hunting AI system."
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(username, [username], msg.as_string())
        print("✅ Test email sent successfully")

        server.quit()
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 This might be because:")
        print("   - Two-factor authentication is enabled (need App Password)")
        print("   - 'Less secure app access' is disabled")
        print("   - Password is incorrect")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_app_password_format():
    """Check if password looks like a Gmail App Password"""
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        return False

    # Gmail App Passwords are typically 16 characters without spaces
    # But they're often entered with spaces like "abcd efgh ijkl mnop"
    clean_password = password.replace(" ", "")

    if len(clean_password) == 16 and clean_password.isalnum():
        print("✅ Password format looks like a Gmail App Password")
        return True
    elif " " in password and len(password.replace(" ", "")) == 16:
        print("⚠️  Password has spaces - Gmail App Passwords usually don't need spaces")
        return True
    else:
        print("⚠️  Password doesn't look like a standard Gmail App Password format")
        print(f"   Length: {len(password)} characters")
        print("   Gmail App Passwords are typically 16 alphanumeric characters")
        return False

def main():
    print("🔍 Debugging Email Configuration")
    print("=" * 50)

    # Check if we have an App Password format
    check_app_password_format()
    print()

    # Test the connection
    success = test_gmail_connection()

    if not success:
        print("\n🔧 Troubleshooting Tips:")
        print("1. Make sure 2FA is enabled on your Gmail account")
        print("2. Generate an App Password at: https://myaccount.google.com/apppasswords")
        print("3. Use the App Password (not your regular Gmail password)")
        print("4. Ensure 'Less secure app access' is not required")
        print("5. Check that your account allows SMTP access")

if __name__ == "__main__":
    main()