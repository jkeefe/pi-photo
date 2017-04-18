# Notes in and about progress

Started with discussion here: https://www.raspberrypi.org/forums/viewtopic.php?t=51555&p=399904

## Setting to run at startup

by klinstifen » Fri Aug 02, 2013 7:41 pm
To make the program run at bootup, you need to edit /etc/rc.local. At the end of the file you would add a line like the following:

`python /home/pi/myTakePicture.py &`

Don't forget the ampersand! Your program will most likely contain an infinite loop while it waits for the GPIO high and the ampersand ensures that /etc/rc.local is running your python script in the background which will allow you to login and debug if necessary.

## On pushbutton

by Odog1996 » Fri Aug 02, 2013 9:24 pm
Hi,
Thanks very much for your help guys, I have managed to get it to work so when I press the switch a photo is taken then a light is shown on the little board that the camera has finished. Here is the code I used so anyone wishing to recreate this can do so. My trigger is a simple push to make switch with a 10K pull down resistor attached from 3V3 to pin 11 and the LED is from pin 12 to ground, through a 150ohm resistor.

```python
#!/usr/bin/env python

import sys, os, time
import RPi.GPIO as GPIO

GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

image_num = 1

GPIO.output(12, False)

while True:
   if GPIO.input(11):
      strImage = str(image_num)
           os.system("raspistill -t 1000 -hf -vf -o image" + strImage + ".jpg")
      image_num = image_num + 1
           GPIO.output(12, True)
           time.sleep(3)
           GPIO.output(12, False)
```

