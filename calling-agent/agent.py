from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import os
import urllib.parse
import sys
from googletrans import Translator
import google.generativeai as genai
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set console encoding to UTF-8 to properly display Hindi characters
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
translator = Translator()

# Setup Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = os.getenv("TO_NUMBER")

client = Client(account_sid, auth_token)

# Function to load data from the text file
def load_knowledge_base_data():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return "Knowledge base not found or could not be loaded."

# Setup Gemini API
def setup_gemini():
    # You'll need to add your API key to your .env file
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in .env file")
        return False
    genai.configure(api_key=api_key)
    return True

# Initialize Gemini
gemini_available = setup_gemini()

# Function to translate Hindi text to English
def translate_to_english(text):
    try:
        # Detect language and translate to English if not already English
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return f"{text} (translation failed)"

def format_email(email_text):
    """Format spoken email text into standard email format"""
    try:
        # Common patterns to clean up
        email_text = email_text.lower()
        
        # Extract the domain part if it exists
        domain = ""
        if "gmail" in email_text:
            domain = "gmail.com"
        elif "yahoo" in email_text:
            domain = "yahoo.com"
        elif "hotmail" in email_text:
            domain = "hotmail.com"
        # Add more domains as needed
        
        # Clean up common speech patterns
        email_text = email_text.replace("at the rate", "@")
        email_text = email_text.replace("एट द रेट", "@")
        email_text = email_text.replace("at", "@")
        email_text = email_text.replace("dot", ".")
        email_text = email_text.replace("डॉट", ".")
        
        # Remove spaces
        email_text = email_text.replace(" ", "")
        
        # Remove common punctuation
        for char in ["!", "?", ",", ";"]:
            email_text = email_text.replace(char, "")
        
        # If no @ symbol and we have a domain, add it
        if "@" not in email_text and domain:
            email_text = email_text + "@" + domain
        
        return email_text
    except Exception as e:
        print(f"Email formatting error: {e}")
        return email_text

def format_blood_group(blood_text):
    """Format spoken blood group text into standard format"""
    try:
        blood_text = blood_text.lower()
        
        # Map common blood group patterns
        if "a" in blood_text or "ए" in blood_text:
            blood_type = "A"
        elif "b" in blood_text or "बी" in blood_text:
            blood_type = "B"
        elif "ab" in blood_text or "एबी" in blood_text:
            blood_type = "AB"
        elif "o" in blood_text or "ओ" in blood_text:
            blood_type = "O"
        else:
            blood_type = blood_text
            
        # Check for positive/negative
        if "positive" in blood_text or "पॉजिटिव" in blood_text:
            return blood_type + "+"
        elif "negative" in blood_text or "नेगेटिव" in blood_text:
            return blood_type + "-"
        else:
            return blood_type
    except Exception as e:
        print(f"Blood group formatting error: {e}")
        return blood_text

# Function to send an email to the user
def send_thank_you_email(user_name, user_email, blood_group):
    try:
        # Your Gmail credentials
        sender_email = os.getenv("GMAIL_ADDRESS")  # Add this to your .env file
        app_password = os.getenv("GMAIL_APP_PASSWORD")  # Add this to your .env file
        
        if not sender_email or not app_password:
            print("Email credentials not found in .env file")
            return False
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = "Thank You for Connecting with Prerit Foundation"
        
        # Email body with Hindi and English content
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
                    <p>हैप्पी यादव जी और हमारी टीम जल्द ही आपसे संपर्क करेगी। आपके सहयोग के लिए पुनः धन्यवाद।</p>
                    <p>---------------------------------------</p>
                    <p>Dear {user_name},</p>
                    <p>Thank you for connecting with Prerit Foundation!</p>
                    <p>We have securely stored your following information in our database:</p>
                    <ul>
                        <li><strong>Name:</strong> {user_name}</li>
                        <li><strong>Email:</strong> {user_email}</li>
                        {'<li><strong>Blood Group:</strong> ' + blood_group + '</li>' if blood_group else ''}
                    </ul>
                    <p>Happy Yadav and our team will contact you soon. Thank you once again for your cooperation.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Prerit Foundation. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach the HTML body to the email
        msg.attach(MIMEText(body, 'html'))
        
        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        
        print(f"Thank you email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Function to save user data to CSV
def save_user_data_to_csv(name, email, blood_group):
    try:
        # Check if file exists to determine if we need to write headers
        file_exists = False
        try:
            with open("user_data.csv", "r") as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False
        
        # Open file in append mode
        with open("user_data.csv", "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # If file doesn't exist, write header row
            if not file_exists:
                writer.writerow(["Name", "Email", "Blood Group", "Registration Date"])
            
            # Write the user data
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([name, email, blood_group, current_datetime])
            
        print(f"User data saved to CSV: {name}, {email}, {blood_group}")

        # Send thank you email to the user
        if '@' in email:  # Basic validation to ensure email looks valid
            send_thank_you_email(name, email, blood_group)
            print(f"Thank you email sent to {email}")
        else:
            print(f"Invalid email format: {email}, email not sent")
        return True
    except Exception as e:
        print(f"Error saving user data to CSV: {e}")
        return False

# Get response from Gemini for general questions
async def get_gemini_response(question):
    try:
        # Set up a model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create a prompt that instructs Gemini to answer in Hindi
        prompt = f"""
        Answer the following question in Hindi language. Keep the answer concise (2-3 sentences maximum).
        If you don't know the answer, just say you don't have that information in Hindi.
        
        Question: {question}
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "मुझे इस सवाल का जवाब नहीं मिला। कृपया बाद में पुनः प्रयास करें।"

# Get responses from Gemini based on the knowledge base
async def get_knowledge_base_response(question):
    """Get Gemini response using data.txt as knowledge base"""
    try:
        # Set up a model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load knowledge base content
        knowledge_base = load_knowledge_base_data()
        
        # Create a prompt that instructs Gemini to use only the knowledge base
        prompt = f"""
        You are a helpful AI assistant for Coding Ninjas Club created by Happy Yadav.
        Use ONLY the following information to answer the user's question.
        If the answer isn't found in the provided information, politely say you don't have that information.
        Always answer in Hindi language. Keep the answer concise (2-3 sentences maximum).
        
        KNOWLEDGE BASE INFORMATION:
        {knowledge_base}
        
        USER QUESTION: {question}
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting knowledge base response: {e}")
        return "मुझे इस सवाल का जवाब नहीं मिला। कृपया बाद में पुनः प्रयास करें।"