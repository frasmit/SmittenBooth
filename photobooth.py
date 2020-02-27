#!/usr/bin/env python

import os
import sys
import time
from picamera import PiCamera
import RPi.GPIO as GPIO
from PIL import Image

camera = PiCamera()
waiting = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# GPIO output is inverted. Using relay in normally closed circuit mode and applying voltage breaks the circuit
GPIO.setup(14, GPIO.OUT, initial=1)
GPIO.setup(15, GPIO.OUT, initial=1)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

localFileDir = os.path.dirname(os.path.abspath(__file__))
image_path = localFileDir + '/includes/images/'  # Location of ready and countdown images
photo_path = localFileDir + '/photos/'  # Where photos will be stored

# Initial Setup
if not os.path.exists(photo_path):
    os.makedirs(photo_path)

# overlay images
img1 = Image.open(image_path + '1.png')
img2 = Image.open(image_path + '2.png')
img3 = Image.open(image_path + '3.png')
img4 = Image.open(image_path + '4.png')
img5 = Image.open(image_path + '5.png')
img6 = Image.open(image_path + 'ready.png')

# Camera Settings
previewBrightness = 50  # Lighter than normal to offset the alpha distortion
photoBrightness = 50  # Darker than preview since there is no alpha
camera.resolution = (1360, 768) 
camera.framerate = 30
camera.hflip = False
camera.awb_mode = 'fluorescent'
camera.exposure_mode = 'auto'
camera.meter_mode = 'spot'
camera.saturation = 15
camera.ISO = 800

##### Sub-routines #####

# Turns on Camera Preview as well as button light.
def previewStart():
    GPIO.output(15, 0)
    camera.resolution = (1360, 768) 
    camera.framerate = 30
    camera.hflip = True
    camera.awb_mode = 'fluorescent'
    camera.exposure_mode = 'auto'
    camera.meter_mode = 'spot'
    camera.saturation = 15
    camera.ISO = 800
    camera.start_preview()


def previewStop():
    camera.stop_preview()


# btnSate should be False before Countdown is called
# and should end up False after Countdown complete:
def doCountdown():
    i = 6
    btnState = False
    while i > 0:
        l = 'img{}'.format(i)
        btnState = not btnState
        GPIO.output(15, btnState)
        o = camera.add_overlay(eval(l).tobytes(), size=eval(l).size)
        o.alpha = 128
        o.layer = 3
        i -= 1
        time.sleep(1)
        camera.remove_overlay(o)


def lightOn():
    GPIO.output(14, 0)


def lightOff():
    GPIO.output(14, 1)


def takePhoto():
    # Manually setting button light to off
    GPIO.output(15, 1)

    # Grab the capture time
    time_stamp = time.strftime('%Y_%m_%dT%H_%M_%S', time.gmtime())
    path = photo_path + '%s.jpg' % time_stamp

    # Setup camera options
    camera.resolution = (1800, 1200) 
    camera.framerate = 30
    camera.hflip = False
    camera.awb_mode = 'fluorescent'
    camera.exposure_mode = 'auto'
    camera.meter_mode = 'spot'
    camera.saturation = 15
    camera.ISO = 800
  
    # Take the photo
    camera.capture(path, use_video_port=False)

    return path

    camera.close()


##### Start Photobooth #####
previewStart()


##### Main Loop #####
while True:
    checkButton= GPIO.input(23)
    if waiting == True:
        if checkButton == GPIO.HIGH:
            waiting = False
            doCountdown()
            lightOn()
            takePhoto()
            lightOff()
            previewStart()
    if waiting == False:
        if checkButton == GPIO.LOW:
            waiting = True
    time.sleep(0.1)
