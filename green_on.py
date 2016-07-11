#!/usr/bin/python
import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarning(False)

green = 12

GPIO.setup(green,GPIO.OUT)
print "green led on"
while 1:
	GPIO.output(green,1)
	time.sleep(1)
	GPIO.output(green,0)
	time.sleep(1)
