#The combination of send_email and SoilSensor
#Title:SoilSensorEmail
#Description:You will get email reprot from Pi every 3 house to check if soil is wet or dry
#Name: Liu Yutong
#Student ID:202283890002
#Course & Year:Iot/2022
#Date:22/4/25

import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Sensor Configuration
SENSOR_PIN = 4  # GPIO4 (BCM mode)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Email Configuration
FROM_EMAIL = "3269076158@qq.com"
APP_PASSWORD = "mkvrgpibmyhedaib"  # QQ Mail Authorization Code
TO_EMAIL = "liuyutongstudy@outlook.com"

def check_moisture():
    """Check soil moisture status"""
    try:
        # Read sensor state (0=dry, 1=wet)
        is_wet = GPIO.input(SENSOR_PIN)
        return "Soil is moist. No watering needed." if is_wet else "Soil is dry! Water plant immediately!"
    except Exception as e:
        print(f"Sensor read error: {e}")
        return "Sensor status unknown"

def send_email(status):
    """Send plant status email"""
    try:
        msg = EmailMessage()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg.set_content(f"Plant Status Report ({current_time} Beijing Time):\n{status}")
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = "Plant Watering Alert"

        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {e}")

def main_loop():
    """Main monitoring loop"""
    # Immediate first check
    status = check_moisture()
    send_email(status)
    
    # Hourly checks
    while True:
        print(f"Next check at: {datetime.now().strftime('%H:%M')} (waiting 1 hour)")
        time.sleep(3600)  # 1 hour = 3600 seconds
        status = check_moisture()
        send_email(status)

if __name__ == "__main__":
    try:
        print("Plant Monitoring System Started (Press Ctrl+C to exit)")
        main_loop()
    except KeyboardInterrupt:
        print("\nSystem terminated")
    finally:
        GPIO.cleanup()
