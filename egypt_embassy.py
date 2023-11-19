import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize the SMTP server for sending email notifications
def send_email_notification(subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = ""  # Add you Email here
    smtp_password = "" # Add generated pass code here 
    sender_email = ""  # Add you Email here
    receiver_email = ""  # Add you Email here

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    body = message
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def check_availability():
    chrome_options = Options()
    # You can add more options as required
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('start-maximized') 
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome()
    driver.get("https://egyptianconsulateindubai.as.me/schedule.php")

    try:
        time.sleep(5)  # Wait for the page to load
        message_element = driver.find_element(By.XPATH, '//*[contains(text(), "No times are available")]')
        if message_element:
            print("No new available times.")
            # send_email_notification("New Availability Alert","No new available times.")
        else:
            send_email_notification("New Availability Alert", "New time slots might be available on the website.")
    except NoSuchElementException:
        send_email_notification("New Availability Alert", "New time slots might be available on the website.")
    finally:
        driver.quit()

# Continuously check every 10 minutes
while True:
    check_availability()
    # print("Waiting 10 minutes before the next check...")

    time.sleep(300)  # Wait for 5 minutes (300 seconds) before checking again



