import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


one = 16
two = 22

shcp = 11
stcp = 13
sin  = 15
mclr = 7

arr = [1,1,1,1,1,1,1,0]

GPIO.setup(one,GPIO.OUT)
GPIO.setup(two,GPIO.OUT)
GPIO.setup(shcp,GPIO.OUT)
GPIO.setup(stcp,GPIO.OUT)
GPIO.setup(sin,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)

def myclock (pin):
    GPIO.output(pin,0)
    time.sleep(0.001)
    GPIO.output(pin,1)
i=0
j=0
k=1


 
    
while (i<40):
    j= i%8
    print "iiiiiiiiiiiii : ",i
    print"j is : ",j
    GPIO.output(sin,arr[j])
    print "aar[j]is : ",arr[j]
    myclock(shcp)
    myclock(stcp)
    #time.sleep(1)
    i=i+1
   
GPIO.output(one,1)
GPIO.output(two,1)
time.sleep(5)
GPIO.output(one,0)
GPIO.output(two,0)
   

while (k==1):    
    GPIO.output(29,0)
    GPIO.output(29,1)
