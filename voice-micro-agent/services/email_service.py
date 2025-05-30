import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import settings

def send_thank_you_email(user_name, user_email, blood_group):
    """Send thank you email to user"""
    try:
        if not settings.GMAIL_ADDRESS or not settings.GMAIL_APP_PASSWORD:
            print("Email credentials not found")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = settings.GMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = "Thank You for Connecting with Prerit Foundation"
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Prerit Foundation</h2>
                </div>
                <div class="content">
                    <p>नमस्ते {user_name} जी,</p>
                    <p>प्रीरित फाउंडेशन से जुड़ने के लिए आपका हार्दिक धन्यवाद!</p>
                    <p>हमने आपकी निम्नलिखित जानकारी हमारे डेटाबेस में सुरक्षित कर ली है:</p>
                    <ul>
                        <li><strong>नाम:</strong> {user_name}</li>
                        <li><strong>ईमेल:</strong> {user_email}</li>
                        {'<li><strong>रक्त समूह:</strong> ' + blood_group + '</li>' if blood_group else ''}
                    </ul>
                    <p>हैप्पी यादव जी और हमारी टीम जल्द ही आपसे संपर्क करेगी।</p>
                    <p>---------------------------------------</p>
                    <p>Dear {user_name},</p>
                    <p>Thank you for connecting with Prerit Foundation!</p>
                    <p>We have securely stored your information. Happy Yadav and our team will contact you soon.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Prerit Foundation. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Thank you email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False