#The soil sensor test
#Title:SoilSensor
#Description:You can test if the soil is wet or dry
#Name: Liu Yutong
#Student ID:202283890002
#Course & Year:Iot/2022
#Date:19/4/25

import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print ("Water Detected!")
	else:
		print ("Water Detected!")

# let us know when the pin goes HIGH or LOW.
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) 
# assign function to GPIO PIN, Run function on change
GPIO.add_event_callback(channel, callback) 

# infinite loop
while True:
	time.sleep(0)
