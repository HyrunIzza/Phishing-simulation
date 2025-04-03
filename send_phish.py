import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_phishing_email(target_email, fake_link):
    sender_email = "hyrunizza.19@gmail.com@gmail.com"  # Use a test account
    password = "kgge pjpp sryk pwwq"  # Gmail App Password
    
    msg = MIMEMultipart()
    msg['From'] = "security@yourcompany.com"  # Spoofed sender
    msg['To'] = target_email
    msg['Subject'] = "URGENT: Password Reset Required!"
    
    body = f"""
    <html>
      <body>
        <p>Dear User,</p>
        <p>We detected unusual activity on your account. Immediate password reset is required.</p>
        <p><a href="{fake_link}">Click here to reset your password</a></p>
        <p>If you did not request this, please ignore this email.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, target_email, msg.as_string())
        print(f"[+] Phishing email sent to {target_email}!")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    target_email = "test@example.com"  # Replace with test email
    fake_login_page = "http://localhost:5000/fake_login"  # Local fake page
    send_phishing_email(target_email, fake_login_page)
