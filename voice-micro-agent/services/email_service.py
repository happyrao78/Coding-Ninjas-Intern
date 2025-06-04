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
        msg["From"] = settings.GMAIL_ADDRESS
        msg["To"] = user_email
        msg["Subject"] = "Thank You for Connecting with Sankalpiq Foundation"

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
                    <h2>Sankalpiq Foundation</h2>
                </div>
                <div class="content">
                    
                    <p>Dear {user_name},</p>
                    <p>Email: {user_email}</p>
                    <p>Blood Group: {blood_group}</p>
                    <p>Thank you for connecting with Sankalpiq Foundation!</p>
                    <p>We have securely stored your information.Our team will contact you soon.</p>
                    <p>If you have any questions, feel free to reach out to us at <a href="https://sankalpiq.co.in">sankalpiq.co.in</a>
                       </p>
                    <p>Best regards,<br>Sankalpiq Foundation Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 Sankalpiq Foundation. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Thank you email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
