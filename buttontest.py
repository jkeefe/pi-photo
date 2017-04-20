#!/usr/bin/env python

# from http://raspberrywebserver.com/gpio/using-interrupt-driven-gpio.html

import time
import RPi.GPIO as GPIO

LED_GPIO_PIN = 24
BUTTON_GPIO_PIN = 23


# handle the button event
def buttonEventHandler (pin):
    print "handling button event"

    # turn the green LED on
    GPIO.output(LED_GPIO_PIN, GPIO.HIGH)

    time.sleep(15)

    # turn the green LED off
    GPIO.output(LED_GPIO_PIN, GPIO.HIGH)



# main function
def main():

    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 23 as an input
    # and set up pins 24 and LED_GPIO_PIN as outputs
    GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_GPIO_PIN, GPIO.OUT)

    # tell the GPIO library to look out for an 
    # event on pin BUTTON_GPIO_PIN and deal with it by calling 
    # the buttonEventHandler function
    GPIO.add_event_detect(BUTTON_GPIO_PIN, GPIO.BOTH, buttonEventHandler)

    # turn off LED
    GPIO.output(LED_GPIO_PIN, LOW)

    # make the LED flash
    while True:
        GPIO.output(LED_GPIO_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_GPIO_PIN, GPIO.LOW)
        time.sleep(1)

    GPIO.cleanup()

if __name__=="__main__":
    main()
