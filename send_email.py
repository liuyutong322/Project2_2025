#The email send test
#Title:send_email
#Description:You can send email from Pi to your email
#Name: Liu Yutong
#Student ID:202283890002
#Course & Year:Iot/2022
#Date:20/4/25

import smtplib
from email.message import EmailMessage

# Set the sender email and password and recipient email
from_email_addr = "3269076158@qq.com"
from_email_pass = "mkvrgpibmyhedaib"
to_email_addr = "liuyutongstudy@outlook.com"

# Create a message object
msg = EmailMessage()

# Set the email body
body = "Hello from Raspberry Pi"
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set your email subject
msg['Subject'] = 'TEST EMAIL'

# Connecting to server and sending email
# Edit the following line with your provider's SMTP server details
server = smtplib.SMTP_SSL('smtp.qq.com', 465)

# Comment out the next line if your email provider doesn't use TLS
# server.starttls()

# Login to the smtp server
server.login(from_email_addr, from_email_pass)

# Send the message
server.send_message(msg)
print('Email sent')

# Disconnect from the Server
server.quit()
