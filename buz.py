import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

red = 40
buz = 36
stcp = 11
shcp = 13
sin = 16

one=16
two=18

GPIO.setup(red,GPIO.OUT)
GPIO.setup(buz,GPIO.OUT)
GPIO.setup(one,GPIO.OUT)
GPIO.setup(two,GPIO.OUT)
GPIO.setup(shcp,GPIO.OUT)
GPIO.setup(stcp,GPIO.OUT)
GPIO.setup(sin,GPIO.OUT)

def warningalert():
    blink()
    buzz()
    return

def blink():
    GPIO.output(red,1)
    time.sleep(0.5)
    GPIO.output(red,0)
    time.sleep(0.5)
    return

def buzz():
    GPIO.output(buz,1)
    time.sleep(0.1)
    GPIO.output(buz,0)
    time.sleep(0.1)
    GPIO.output(buz,1)
    time.sleep(0.1)
    GPIO.output(buz,0)
    time.sleep(0.1)
    GPIO.output(buz,1)
    time.sleep(.1)
    return

def buzz1():
    GPIO.output(buz,1)
    time.sleep(0.4)
    GPIO.output(buz,0)
    time.sleep(0.6)
    GPIO.output(buz,1)
    time.sleep(0.4)
    GPIO.output(buz,0)
    time.sleep(0.6)
    GPIO.output(buz,1)
    time.sleep(.4)
    GPIO.output(buz,0)
    time.sleep(0.6)
    return

def myclock (pin):
    GPIO.output(pin,0)
    time.sleep(0.001)
    GPIO.output(pin,1)
    

    
i=0
GPIO.setwarnings(False)


GPIO.output(one,1)
GPIO.output(two,0)


while (i<15):
    warningalert()
    i=i+1
    
GPIO.output(buz,0)
print "seg"    
GPIO.cleanup()    
