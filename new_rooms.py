import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client

def send_whatsapp(status=None):

    # Twilio credentials
    account_sid = '###################################'
    auth_token = '###########################################3'
    client = Client(account_sid, auth_token)

    # Your WhatsApp number and the Twilio WhatsApp number
    to_whatsapp_number = '###########################'
    from_whatsapp_number = '###########################'

    # Send the message
    message = client.messages.create(
        body="https://www.stwdo.de/wohnen/aktuelle-wohnangebote",
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

def send_email(state):
    # Email account credentials
    from_email = "###############"
    from_password = ""
    to_email = "################"

    subject = "Room Availability Notification"

    if state == 'success':
        message = "NEW ROOMS!! -> <a href='https://www.stwdo.de/wohnen/aktuelle-wohnangebote'>website</a>!"
    elif state == 'failure':
        message = "Nothing changed :("

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    # msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(message, 'html'))
    # Send the email
    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP('mail.gmx.net', 587)
        server.starttls()
        print("Logging in...")
        server.login(from_email, from_password)
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def check_new_listings():
    options = ChromeOptions()
    options.add_argument('--headless')  # Set Chrome to run in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Check if there are new rooms in Dortmund
        select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'tx_openimmo_list[tx_openimmo_list][city]'))
        )

        options = select.find_elements(By.TAG_NAME, 'option')
        dortmund_available = False
        for option in options:
            value = option.get_attribute('value')
            disabled = option.get_attribute('disabled')
            if value == 'Dortmund' and not disabled:
                dortmund_available = True
                break

        page_source = driver.page_source
        # TODO: Remove later
        # This also returns true if it not for dortmund
        if 'leider haben wir aktuell keine' not in page_source:
            return True

        if not dortmund_available:
            return False
        return True

    finally:
        driver.quit()

def show_notification(state):
    root = tk.Tk()
    root.title("Update")

    window_width = 400 * 2
    window_height = 200 * 2
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    root.resizable(False, False)

    if state == 'success':
        message = "A new room is available in Dortmund.\nCheck the website!"
    elif state == 'failure':
        message = "Nothing changed :( "


    label = tk.Label(root, text=message, padx=20, pady=20)
    label.pack(expand=True)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=10)

    root.mainloop()

url = 'https://www.stwdo.de/wohnen/aktuelle-wohnangebote'

def main():
    if check_new_listings():
        # send_email("success")
        show_notification("success")
        send_whatsapp("success")
    else:
        # send_email("failure")
        # show_notification("failure")
        # send_whatsapp("failure")
        print(f"No room @ {datetime.now()}")

if __name__ == '__main__':
    main()