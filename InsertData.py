import MySQLdb
import datetime
import threading
import time
from threading import Thread, current_thread
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class InsertData(threading.Thread):
        
        db = None
        curs = None
        isalerting = 0
        toDisplay=[0,0,0,0,0]
        
        def starts(self):
                global db
                db=MySQLdb.connect("localhost","root","123","MedicineBox")
                global curs
                curs=db.cursor()
                GPIO.setwarnings(False)

        def close(self):
                global curs
                curs.close()

                global db
                db.close()
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Initialize pins output/input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def init(self):
                GPIO.setup(self.stcp,GPIO.OUT)
                GPIO.setup(self.shcp,GPIO.OUT)
                GPIO.setup(self.sin,GPIO.OUT)
                GPIO.setup(self.green,GPIO.OUT)
                GPIO.setup(self.red,GPIO.OUT)
                GPIO.setup(self.buz,GPIO.OUT)
                GPIO.setup(self.one,GPIO.IN)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Custom timer function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def Timer(self,p):
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
        def display(self,a,b,c,d,e):
                print 'displaying'
                ary = [e,d,c,b,a]
                for j in range (5):
                        for i in range(8):
                            GPIO.output(self.sin,arr[ary[j]][i])
                            Timer(self.shcp)
                for i in range (40):
                        Timer(self.stcp)


       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           blink red led
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def blinkR(self):
                GPIO.output(self.red,1)
                time.sleep(0.5)
                GPIO.output(self.red,0)
                time.sleep(0.5)
                return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Normal alert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def alertN(self):
                for i in range (2):
                        GPIO.output(self.buz,1)
                        time.sleep(0.5)
                        GPIO.output(self.buz,0)
                        time.sleep(0.5)
                return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Warning alert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def alertW(self):
                for i in range (3):
                        GPIO.output(self.buz,1)
                        time.sleep(0.1)
                        GPIO.output(self.buz,0)
                        time.sleep(0.3)
                GPIO.output(self.buz,0)
                time.sleep(0.4)
                return
    


        


        def run(self):
                self.starts()
                self.init()
                while True:
                        ctime=datetime.datetime.now().strftime('%H:%M:%S')                        
                        self.isRightTime(ctime)
                        #time.sleep(5000)
                self.close()     
                        
                        
                
        def isRightTime(self,currentTime):
                
                try:
                        time.sleep(1)
                        
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
                                        InsertData.toDisplay[i]=durations[0][1]
                                        
                                      
                                
                                else:
                                        storedTime = storedTime + dt1
                                        
                                        if storedTime == currentTime:
                                                found=1
                                                InsertData.toDisplay[i]=durations[0][1]
                                                
                                        
                                        else:
                                                storedTime = storedTime + dt1
                                                if storedTime==currentTime:
                                                        
                                                        found=1
                                                        InsertData.toDisplay[i]=durations[0][1]
                                                        
                                i=i+1                
                        if found==1:
                                print InsertData.toDisplay
                                InsertData.isalerting=1
                                opens=openBox(name="detectbox")
                                opens.start()
                                
                                time.sleep(1)
                                self.normalAlert()
                                t1=Thread(target=self.display,args=(InsertData.toDisplay[0],InsertData.toDisplay[1],InsertData.toDisplay[2],InsertData.toDisplay[3],InsertData.toDisplay[4]))
                                t1.start()
                                #self.display(InsertData.toDisplay[0],InsertData.toDisplay[1],InsertData.toDisplay[2],InsertData.toDisplay[3],InsertData.toDisplay[4])
                                #alert call
                                #display function must be called with array toDisplay.
                                GPIO.cleanup()
                                found=0
                        
                except:
                        print "Error: the database is being rolled back"
                        #global db
                        #db.rollback() 
                return

class openBox(threading.Thread):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Turn on green led
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       # green = 33

        
        #def blinkG(self):
              #  GPIO.output(self.green,1)
              #  time.sleep(5)
              #  return
        
        
        def detectBox(self):
                openBox.boxopen=1
                return 5

        def run(self):
        
                while True:
                        self.ackOrWarning()
                
        def ackOrWarning(self):      
                
                db=MySQLdb.connect("localhost","root","123","MedicineBox")
                
                curs=db.cursor()
                today = datetime.datetime.now().strftime("%A")[:3]
                curs.execute('SELECT '+today+' FROM MedicineBox')
                boxes=curs.fetchall()
                       
                boxid=0
                ackArray=[0,0,0,0,0]
                t1=time.time()
                while True:
                        t2=time.time()
                        

                        while (t2-t1)%5==0 and openBox.boxopen ==0:
                                print 'alert'
                                self.normalAlert()
                                
                                #alert must be called
                                
                        boxid = self.detectBox()
                        #warnalert=0
                        if boxes[boxid-1][0]==0: #and warnalert==0:
                                #warnalert=1
                                print 'warning alert'
                                self.warningalert()
                                #Warning alert must be called

                        elif boxes[boxid-1][0]==1:
                                ackArray[boxid-1]=1
                        

                        y=0
                        for y in range(0,5):
                                if boxes[y][0]!=ackArray[y]:
                                        break;
                                else:
                                        print 'hello'
                                       # self.blinkG()

                        if y==4:
                                print 'okay'
                                #InsertData.toDisplay       ack must be sent and set InsertData.toDisplay to 0
                                break

                        if t2-t1>3600:
                                #set InsertData.toDisplay to 0
                                break

                        
                curs.close()
                db.close()
                       
                exit()
                        
                        

insert=InsertData(name="check Time")
insert.start()




        
