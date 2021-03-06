#!/usr/bin/env python

# To make the program run at bootup, you need to edit /etc/rc.local. 
# At the end of the file you would add a line like the following:
#    `python /home/pi/pi-photo/take_a_picture.py &`
# Don't forget the ampersand! This program contains an infinite loop
# while it waits for the GPIO high and the ampersand ensures that /etc/rc.local 
# is running your python script in the background which will 
# allow you to login and debug if necessary.

from __future__ import absolute_import

import time
import RPi.GPIO as GPIO
import io
import os
import sys
import json
import boto3

# Let's use Amazon S3
s3 = boto3.client('s3')

# Import the Google Cloud client library
from google.cloud import vision

# Constants are here
GREEN_LED = 24
RED_LED = 22
BUTTON_GPIO_PIN = 23

# Global variable here
time_stamp = 0
last_time_taken = 0


# handle what happens when button is pushed
def buttonEventHandler (pin):
    
    global time_stamp
    global last_time_taken
    
    time_now = time.time()
    
    # see if this new press is at least 1 seconds since the last button push
    if (time_now - time_stamp) > 1:
    
        print ("button pressed!")
        
        time_stamp = time_now
        
        image_file_name = "/home/pi/pi-photo/photos/latest.jpg"
        json_file = "/home/pi/pi-photo/data/vision.json"

        # turn the red LED on
        GPIO.output(RED_LED, GPIO.HIGH)

        # take a picture
        print ("taking a picture")
        os.system("raspistill -t 500 -w 1000 -h 1000 -e jpg -q 100 -hf -o " + image_file_name)
        print ("picture taken")
        
        # quickly flash the RED LED to acknowledge the picture has been taken
        GPIO.output(RED_LED, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(RED_LED, GPIO.HIGH)

        # Instantiates a Google Vision API client
        vision_client = vision.Client()

        print ("ready to send to google")

        # The name of the image file to analyze
        # file_name = os.path.join(
        #     os.path.dirname(__file__),
        #     image_file)

        # Loads the image into memory
        with io.open(image_file_name, 'rb') as image_file:
            content = image_file.read()
            image = vision_client.image(
                content=content)

        # Performs label detection on the image file
        print ("Sending to Google Vision API")
        labels = image.detect_labels()
        label_list = []

        print('Labels:')
        for label in labels:
            print(label.description)
            label_list.append(label.description)
            
        print(label_list)

        # build the labels object
        data = {"labels" : label_list}

        # dump it to a file as json
        with open(json_file, 'wb') as outfile:
            json.dump(data, outfile)

        # upload that file to s3
        s3.upload_file(
            json_file, 'media.johnkeefe.net', 'vision.json',
            ExtraArgs={'ACL': 'public-read'}
        )

        # turn the red LED off
        GPIO.output(RED_LED, GPIO.LOW)

    time_stamp = time.time()

# main function
def main():

    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 23 as an input
    # and set up pins 24 and GREEN_LED as outputs
    GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)
    
    # setting up a variable for detecting bounces!
    time_stamp = time.time()

    # tell the GPIO library to look out for an 
    # event on pin BUTTON_GPIO_PIN and deal with it by calling 
    # the buttonEventHandler function
    GPIO.add_event_detect(BUTTON_GPIO_PIN, GPIO.FALLING, buttonEventHandler)

    # turn off LEDs
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)

    # make the green LED flash to indicate all is well
    while True:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(GREEN_LED, GPIO.LOW)
        time.sleep(2)

if __name__=="__main__":
    main()
