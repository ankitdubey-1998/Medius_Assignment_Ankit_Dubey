# send_submission.py
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # read .env file for credentials

# ---------- UPDATE / create a .env file with these ----------
# SENDER_EMAIL=your.email@gmail.com
# SENDER_APP_PASSWORD=your_app_password_or_smtp_password
# -----------------------------------------------------------

SENDER = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SENDER_APP_PASSWORD")

TO = "tech@themedius.ai"
CC = "hr@themedius.ai"
SUBJECT = "Python (Selenium) Assignment - Ankit Dubey"  # change name
BODY = """Hello,

Please find attached:
1. Confirmation screenshot (filled via code)
2. Source code (GitHub repo link included in body)
3. Brief documentation (document attached or in repo)
4. Resume (attached)
5. Links to past projects/work samples (in repo or below)
6. I confirm availability to work full time (10am to 7pm) for next 3-6 months.

GitHub repo:https://github.com/ankitdubey-1998/Medius_Assignment_Ankit_Dubey.git

Regards,
Ankit Dubey
"""

# Attach files (put correct paths)
attachments = [
    ("output/confirmation.png", "image/png"),
    
    
]

def send_email():
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = TO
    msg["Cc"] = CC
    msg.set_content(BODY)

    for path, mime in attachments:
        if not os.path.exists(path):
            print("Warning: attachment not found:", path)
            continue
        with open(path, "rb") as f:
            data = f.read()
        maintype, subtype = mime.split("/")
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))

    # Use Gmail SMTP as example - if you use Gmail, generate an App Password and use it here
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)
    print("Email sent to", TO, "cc", CC)

if __name__ == "__main__":
    send_email()
