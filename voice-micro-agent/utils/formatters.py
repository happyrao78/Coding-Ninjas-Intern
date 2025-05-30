def format_email(email_text):
    """Format spoken email text into standard email format"""
    try:
        email_text = email_text.lower()
        
        domain = ""
        if "gmail" in email_text:
            domain = "gmail.com"
        elif "yahoo" in email_text:
            domain = "yahoo.com"
        elif "hotmail" in email_text:
            domain = "hotmail.com"
        
        email_text = email_text.replace("at the rate", "@")
        email_text = email_text.replace("एट द रेट", "@")
        email_text = email_text.replace("at", "@")
        email_text = email_text.replace("dot", ".")
        email_text = email_text.replace("डॉट", ".")
        email_text = email_text.replace(" ", "")
        
        for char in ["!", "?", ",", ";"]:
            email_text = email_text.replace(char, "")
        
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
            
        if "positive" in blood_text or "पॉजिटिव" in blood_text:
            return blood_type + "+"
        elif "negative" in blood_text or "नेगेटिव" in blood_text:
            return blood_type + "-"
        else:
            return blood_type
    except Exception as e:
        print(f"Blood group formatting error: {e}")
        return blood_text
