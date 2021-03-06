#!/usr/bin/env python

# from http://raspberrywebserver.com/gpio/using-interrupt-driven-gpio.html

import time
import RPi.GPIO as GPIO

GREEN_LED = 24
RED_LED = 22
BUTTON_GPIO_PIN = 23
time_stamp = 0

# handle the button event
def buttonEventHandler (pin):
    
    global time_stamp
    time_now = time.time()
    
    # see if this new press is at least 1 second since the last
    if (time_now - time_stamp) > 1:
    
        print "button pressed!"

        # turn the red LED on
        GPIO.output(RED_LED, GPIO.HIGH)

        time.sleep(3)

        # turn the red LED off
        GPIO.output(RED_LED, GPIO.LOW)

    time_stamp = time_now

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
