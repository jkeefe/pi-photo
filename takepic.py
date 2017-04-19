#!/usr/bin/env python

# See NOTES.md for code credit!

import sys, os, time
import RPi.GPIO as GPIO

GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

image_num = 1

GPIO.output(12, False)

while True:
   if GPIO.input(11):
      strImage = str(image_num)
           os.system("raspistill -t 1000 -hf -vf -o image" + image_file + ".jpg")
      image_num = image_num + 1
           GPIO.output(12, True)
           time.sleep(3)
           GPIO.output(12, False)