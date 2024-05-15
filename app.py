import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')
SUBJECT = 'Daily Report'
REPORT = 'This is your daily report.'

def send_email():
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = SUBJECT

    # Attach the body with the msg instance
    body = f"Hello,\n\n{REPORT}\n\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain'))

    # Create the SMTP server session
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Start TLS for security
    server.login(EMAIL, PASSWORD)  # Log in to the server

    # Send the email
    text = msg.as_string()
    server.sendmail(EMAIL, TO_EMAIL, text)
    
    # Close the SMTP server session
    server.quit()

    print(f"Email sent to {TO_EMAIL} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule the task
schedule.every().day.at("09:00").do(send_email)

if __name__ == "__main__":
    print("Starting the email scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)
