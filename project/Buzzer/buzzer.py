import os 
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(33,GPIO.OUT)

#loop_count=0

def morsecode ():

	GPIO.output(33,GPIO.HIGH)
	time.sleep(.1) 
	GPIO.output(33,GPIO.HIGH)
	time.sleep(.1) 
	GPIO.output(33,GPIO.HIGH)
	time.sleep(.1) 
	GPIO.output(33,GPIO.HIGH)
	time.sleep(.1) 

os.system('clear')

#print "Morse Code"
#loop_count = 1000

while True:
	print "Morse Code"
	morsecode();
	
