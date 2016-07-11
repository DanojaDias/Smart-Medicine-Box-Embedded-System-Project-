import MySQLdb
import datetime
import threading
import time
from threading import Thread, current_thread
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Initialize pins appropriately use physical numbering system of Raspberry pi
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

stcp = 12  # 7seg
shcp = 11  # 7seg
sin = 13   # 7seg

red = 29   # alert
green = 33 # alert
buz = 40   # alert
one = 38   # box
two = 37   # box
three = 36   # box
four = 35   # box
five = 32   # box

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Initialize pins output/input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GPIO.setup(stcp,GPIO.OUT)
GPIO.setup(shcp,GPIO.OUT)
GPIO.setup(sin,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(buz,GPIO.OUT)
GPIO.setup(one,GPIO.IN)
GPIO.setup(two,GPIO.IN)
GPIO.setup(three,GPIO.IN)
GPIO.setup(four,GPIO.IN)
GPIO.setup(five,GPIO.IN)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Custom timer function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Timer(p):
    GPIO.output(p,0)
    time.sleep(0.001)
    GPIO.output(p,1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           7-segment mapping 2D array
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
arr=[[0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 0]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Display 5 seven segment digits in this python function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def display(a,b,c,d,e):
    GPIO.setmode(GPIO.BOARD)
    print 'displaying'
    ary = [e,d,c,b,a]
    for j in range (5):
        for i in range(8):
            GPIO.output(sin,arr[ary[j]][i])
            Timer(shcp)
    for i in range (40):
        Timer(stcp)

    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#          Check Open boxes function 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def openBoxes():
    op=""
    if GPIO.input(one):
        op=op+"1"
    else:
        op=op+"0"
    if GPIO.input(two):
        op=op+"1"
    else:
        op=op+"0"
    if GPIO.input(three):
        op=op+"1"
    else:
        op=op+"0"
    if GPIO.input(four):
        op=op+"1"
    else:
        op=op+"0"
    if GPIO.input(five):
        op=op+"1"
    else:
        op=op+"0"
    return op


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Testing functions in this script
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def opbox(boxes):
    if '1' in boxes:
        return boxes.index("1")+1
    else:
        return 0
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Turn on green led
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def blinkG():
    GPIO.output(green,1)
    time.sleep(5)
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           blink red led
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def blinkR():
    GPIO.output(red,1)
    time.sleep(0.5)
    GPIO.output(red,0)
    time.sleep(0.5)
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Normal alert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def alertN():
    print 'alerting'
    for i in range (30):
        GPIO.output(buz,1)
        time.sleep(0.5)
        GPIO.output(buz,0)
        time.sleep(0.5)
    
    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Warning alert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def alertW():
    for i in range (3):
        GPIO.output(buz,1)
        time.sleep(0.1)
        GPIO.output(buz,0)
        time.sleep(0.3)
    GPIO.output(buz,0)
    time.sleep(0.4)
    return



    

boxopen=0      
db = None
curs = None
isalerting = 0
toDisplay=[0,0,0,0,0]
        
        
def starts():
    global db
    db=MySQLdb.connect("localhost","root","123","MedicineBox")
    global curs
    curs=db.cursor()
    GPIO.setwarnings(False)

def close():
    global curs
    curs.close()

    global db
    db.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Clean used pins and clear variables
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GPIO.cleanup()

def isRightTime(currentTime):
                
    try:
        #time.sleep(1)
                        
        today = datetime.datetime.now().strftime("%A")[:3]
                        
        curs.execute('SELECT '+today+' FROM MedicineBox')
        boxes=curs.fetchall()
                
                
        curs.execute("""SELECT StartingTime FROM MedicineBox""")
        results = curs.fetchall()          
        i=0
        found=0
                        
        for r in results:
                        
            if boxes[i][0]==0:
                i=i+1
                continue
                                
            storedTime=r[0]
                               
            curs.execute("""SELECT TimeDuration,NumberOfPills From MedicineBox WHERE BoxId=%s""",(i+1))
            durations = curs.fetchall()
                                
            duration=str(durations[0][0])+':00:00'
                                
            d1=datetime.datetime.strptime(duration,'%H:%M:%S')
            dt1=datetime.timedelta(hours=d1.hour,minutes=d1.minute,seconds=d1.second)

            if int(currentTime[:2])<10:
                currentTime=currentTime[1:]
                                
            if str(storedTime) == currentTime:                               
                found=1                                                    
                toDisplay[i]=durations[0][1]
                                        
                                      

            else:
                storedTime = storedTime + dt1
                if storedTime == currentTime:                                                
                    found=1
                    toDisplay[i]=durations[0][1]
                                                
                                        
                else:
                    storedTime = storedTime + dt1
                    if storedTime==currentTime:
                                               
                        found=1
                        toDisplay[i]=durations[0][1]
                                                        
            i=i+1                

        if found==1:
            print toDisplay
            isalerting=1
                                     
            time.sleep(1)
            t3=Thread(target=alertN)
            t3.daemon=True
            t3.start()
            t1=Thread(target=display,args=(toDisplay[0],toDisplay[1],toDisplay[2],toDisplay[3],toDisplay[4]))
            t1.daemon=True
            t1.start()
            t2=Thread(target=runalways)
            t2.daemon=True
            t2.start()
                                #self.display(InsertData.toDisplay[0],InsertData.toDisplay[1],InsertData.toDisplay[2],InsertData.toDisplay[3],InsertData.toDisplay[4])
                                #alert call
                                #display function must be called with array toDisplay.
            
            found=0
                        
    except:
        print "Error: the database is being rolled back"
        GPIO.cleanup()
                        #global db
                        #db.rollback() 
        return


def detectBox():
    
    a=opbox(openBoxes())
    if a!=0:
        global boxopen
        boxopen=1
        return a

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Testing functions in this script
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def opbox(boxes):
    if '1' in boxes:
        return boxes.index("1")+1
    else:
        return 0

def runalways():
    while True:
        ackOrWarning()
                
def ackOrWarning():      
    today = datetime.datetime.now().strftime("%A")[:3]
    curs.execute('SELECT '+today+' FROM MedicineBox')
    boxes=curs.fetchall()
    print boxes                   
    boxid=0
    ackArray=[0,0,0,0,0]
    t1=time.time()
    while True:
        t2=time.time()                      

        while (t2-t1)%5==0 and boxopen ==0:
            print 'alert'
            alertN()
                                                           
        boxid = detectBox()
                        #warnalert=0
        if boxid > 0:
            if boxes[boxid-1][0]==0: #and warnalert==0:
                                #warnalert=1
                print 'warning alert'
                alertW()
                                #Warning alert must be called

            elif boxes[boxid-1][0]==1:
                ackArray[boxid-1]=1
                        

        y=0
        for y in range(0,5):
            if boxes[y][0]!=ackArray[y]:
                break;
            else:
                blinkG()

        if y==4:
            print 'okay'
                                #InsertData.toDisplay       ack must be sent and set InsertData.toDisplay to 0
            break

        if t2-t1>3600:
                                #set InsertData.toDisplay to 0
            break

                        
    #curs.close()
    #db.close()
                       
    exit()



starts()
while True:
    ctime=datetime.datetime.now().strftime('%H:%M:%S')                        
    isRightTime(ctime)
    #time.sleep(5000)
   
