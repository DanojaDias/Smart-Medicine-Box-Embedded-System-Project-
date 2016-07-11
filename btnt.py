import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Initialize pins appropriately use physical numbering system of Raspberry pi
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
b_one =7
b_two = 10
b_three =11
b_four = 12
b_five = 13

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Initialize pins output/input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GPIO.setup(b_one,GPIO.IN)
GPIO.setup(b_two,GPIO.IN)
GPIO.setup(b_three,GPIO.IN)
GPIO.setup(b_four,GPIO.IN)
GPIO.setup(b_five,GPIO.IN)

while True:
    if(GPIO.input(b_one) ==True):
        print("on")
    else:
        print("off")
    time.sleep(.5)
        

GPIO.cleanup()
