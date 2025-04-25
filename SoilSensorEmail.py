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
from datetime import datetime, timedelta

# Sensor Configuration
SENSOR_PIN = 4  # GPIO4 (BCM mode)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Email Configuration
FROM_EMAIL = "3269076158@qq.com"
APP_PASSWORD = "mkvrgpibmyhedaib"  # QQ Mail Authorization Code
TO_EMAIL = "liuyutongstudy@outlook.com"

# Time Configuration (UTC+8 for Beijing Time)
UTC_OFFSET = timedelta(hours=8)


def get_beijing_time():
    """Get current Beijing time (UTC+8)"""
    utc_time = datetime.utcnow()
    return utc_time + UTC_OFFSET


def check_moisture():
    """Check soil moisture and return status"""
    try:
        is_wet = GPIO.input(SENSOR_PIN)
        return "Soil is moist, no watering needed." if is_wet else "Soil is dry, water immediately!"
    except Exception as e:
        print(f"Sensor read failed: {e}")
        return "Sensor status unknown"


def send_email(status):
    """Send status email"""
    try:
        msg = EmailMessage()
        msg.set_content(f"Plant Status Report:\n{status}")
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"Plant Monitoring Report - {get_beijing_time().strftime('%Y-%m-%d %H:%M')}"

        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {e}")


def should_run_task():
    """Check if current time is within 09:00-18:00 Beijing time"""
    current_time = get_beijing_time()
    return 9 <= current_time.hour <= 18


def get_next_run_time():
    """Calculate next run time (09:00, 12:00, 15:00, 18:00 Beijing time)"""
    now = get_beijing_time()

    # Find the next target hour
    target_hours = [9, 12, 15, 18]
    for hour in target_hours:
        if now.hour < hour or (now.hour == hour and now.minute == 0):
            next_run = datetime(now.year, now.month, now.day, hour, 0) - UTC_OFFSET
            if next_run > now:
                return next_run

    # If all today's times passed, schedule for tomorrow 09:00
    tomorrow = now + timedelta(days=1)
    next_run = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0) - UTC_OFFSET
    return next_run


if __name__ == "__main__":
    try:
        print("Plant monitoring system started (Press Ctrl+C to exit)")
        next_run = get_next_run_time()

        while True:
            current_utc_time = datetime.utcnow()

            # Check if it's time to run the task
            if current_utc_time >= next_run and should_run_task():
                status = check_moisture()
                send_email(status)
                print(f"{get_beijing_time().strftime('%H:%M')} Check completed")

                # Schedule next run
                next_run = get_next_run_time()

            # Sleep for 30 seconds to reduce CPU usage
            time.sleep(30)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        GPIO.cleanup()
