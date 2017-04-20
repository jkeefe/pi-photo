#!/usr/bin/env python

# from http://raspberrywebserver.com/gpio/using-interrupt-driven-gpio.html

import time
import RPi.GPIO as GPIO

LED_GPIO_PIN = 22
BUTTON_GPIO_PIN = 23


# handle the button event
def buttonEventHandler (pin):
    print "handling button event"

    # turn the green LED on
    GPIO.output(LED_GPIO_PIN,True)

    time.sleep(1)

    # turn the green LED off
    GPIO.output(LED_GPIO_PIN,False)



# main function
def main():

    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 23 as an input
    # and set up pins 24 and LED_GPIO_PIN as outputs
    GPIO.setup(BUTTON_GPIO_PIN,GPIO.IN)
    GPIO.setup(LED_GPIO_PIN,GPIO.OUT)

    # tell the GPIO library to look out for an 
    # event on pin BUTTON_GPIO_PIN and deal with it by calling 
    # the buttonEventHandler function
    GPIO.add_event_detect(BUTTON_GPIO_PIN,GPIO.FALLING)
    GPIO.add_event_callback(BUTTON_GPIO_PIN,buttonEventHandler,100)

    # turn off LED
    GPIO.output(LED_GPIO_PIN,False)

    GPIO.cleanup()



if __name__=="__main__":
    main()
