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

## Photo testing

Basic instructions:
https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md

Full documentation:
https://www.raspberrypi.org/documentation/hardware/camera/README.md

`raspistill -t 1000 -hf -vf -o test.jpg`

## Google Vision API setup

Went through this long checklist:
https://cloud.google.com/vision/docs/quickstart#set_up_a_google_cloud_vision_api_project

Then set up the python sdk here:
https://cloud.google.com/vision/docs/reference/libraries#client-libraries-install-python

https://cloud.google.com/sdk/docs/

Picked Ubuntu
Followed the instrutions

Sigh

to complete next step, had to do `sudo apt-get install apt-transport-https`

did: `sudo apt-get install google-cloud-sdk`

then: `gcloud auth application-default login`

NOTE: The above ^ command opens the default browser and then you have to log in with the same Google account as the whole google vision api setup. This also means you can't do this via ssh, but actually have to have a monitor and keyboard connected to the pi.

OK, that worked.

Next: `gcloud init`

Also ^ needs browser access.

## Got Python Version Working

- Trying to use Anaconda really messed me up. Deleting those notes above.
- My attempt to try the node verision instead was thwarted by some bug / problem in the node package that won't resolve the "config" info I'm passing to it. :-/
- So back to python on the base level of the pi, which worked.

Key reference:
https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html

Some combination of this worked:

Had to remove everything in `/usr/local/lib/python2.7/dist-packages/*` so

`sudo rm -rf /usr/local/lib/python2.7/dist-packages/*`

** Next: `pip install --upgrade google-api-python-client`
** Next: `sudo pip install --upgrade google-cloud`

I was having a lot of X module not found ... had to go into ....
Now: `sudo apt-get install python-dev`

I was able to get the Pi to process the information from a photo, using the example code here:
https://cloud.google.com/vision/docs/reference/libraries#client-libraries-install-python

## Pi -> AWS

My plan is to have the Pi process the image and send the relevant info to a JSON file on S3.

### AWS Command-Line Interface (client-libraries-install-python)

AWS CLI install described here: https://iotbytes.wordpress.com/aws-iot-cli-on-raspberry-pi/

- Logged in to AWS (using my own account, fwiw)
- Went to IAM
- Created a new policy `AccessMediaBucket`
```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": "arn:aws:s3:::*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*"
                ],
                "Resource": "arn:aws:s3:::media.johnkeefe.net"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*"
                ],
                "Resource": "arn:aws:s3:::media.johnkeefe.net/*"
            }
        ]
    }
```
- Created a new group with that policy `MediaBucketAccess`
- Created a new user `pi-3-vision-bot` in that group
- Got the Access and Secret keys

`sudo pip install awscli`

### AWS Python Software Development Kit (SDK)

Info here: https://boto3.readthedocs.io/en/latest/guide/quickstart.html

`sudo pip install boto3`

`aws configure`

Entered the Access and Secret keys above
Use region `us-east-1` for lambda/Alexa
Used `json` format

Also went into `~/.aws/credentials` and copied the same creds under the key name `pi-3-vision-bot`





