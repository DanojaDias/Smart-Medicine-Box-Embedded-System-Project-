import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


one = 16
two = 18

shcp = 11
stcp = 13
sin  = 15


GPIO.setup(one,GPIO.OUT)
GPIO.setup(two,GPIO.OUT)
GPIO.setup(shcp,GPIO.OUT)
GPIO.setup(stcp,GPIO.OUT)
GPIO.setup(sin,GPIO.OUT)

arr = [[0,1,1,1,1,1,1,0],
       [0,1,1,0,0,0,0,0],
       [1,1,0,1,1,0,1,0],
       [1,1,1,1,0,0,1,1],
       [0,1,1,0,0,1,1,0],
       [1,0,1,1,0,1,1,0],
       [1,0,1,1,1,1,1,0],
       [1,1,1,0,0,0,0,0],
       [1,1,1,1,1,1,0,0],
       [1,1,1,1,0,1,1,0],
       [0,0,0,0,0,0,0,0]];

def myclock (pin):
    GPIO.output(pin,0)
    time.sleep(0.001)
    GPIO.output(pin,1)

def display(a,b,c,d,e):
    an1 = a/10
    an2 = a%10

    bn1 =b/10
    bn2 =b%10

    cn1 =c/10
    cn2 =c%10
    print "cn2 : ",cn2

    dn1 =d/10
    dn2 =d%10

    en1 =e/10
    en2 =e%10
    
    v=1
    while v==1 :
        set2(en1,en2)
        set2(dn1,dn2)
        set2(cn1,cn2)
        set2(bn1,bn2)
        set2(an1,an2)

        GPIO.output(one,1)
        GPIO.output(two,0)
        time.sleep(15)

        #GPIO.output(one,0)
        #GPIO.output(two,0)

'''
        ##set1(en1)
        #set1(dn1)
        set1(bn1)
        set1(bn1)
        set1(an1)

        GPIO.output(one,1)
        GPIO.output(two,0)
        #time.sleep(1)

        GPIO.output(one,0)
        #GPIO.output(two,0)
'''

def set2(a,b):
    print "b at set2 ",b
    i=0
    if (a==0 and b==0):
        while (i<8):
            GPIO.output(sin,arr[10][i])
            myclock(shcp)
            myclock(stcp)
            i=i+1
    else :
        while (i<8):
            GPIO.output(sin,arr[b][i])
            myclock(shcp)
            myclock(stcp)
            print "inside print a",a," b ",b
            i=i+1


def set1(b):
    i=0
    while (i<8) :
        if (b==0):
            GPIO.output(sin,arr[10][i])
            myclock(shcp)
            myclock(stcp)
        else:
            GPIO.output(sin,arr[b][i])
            myclock(shcp)
            myclock(stcp)            
        i=i+1
        



display(1,2,3,4,5)


print "done"

GPIO.cleanup()
