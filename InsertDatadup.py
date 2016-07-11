import MySQLdb
import datetime
import threading
import time
from threading import Thread, current_thread
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class InsertData(threading.Thread):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Initialize pins appropriately use physical numbering system of Raspberry pi
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        one = 15
        two = 16
        stcp = 7
        shcp = 11
        sin = 13
        red = 23
        green = 40
        buz = 18

        boxopen=0
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           7-segment mapping 2D array
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        arr=[[0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 0]]
        
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
                #           Clean used pins and clear variables
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                GPIO.cleanup()

    

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Display 5 seven segment digits in this python function
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def display(self,a,b,c,d,e):
                print InsertData.toDisplay
                GPIO.setmode(GPIO.BOARD)
                self.init()
                a1 = a // 10
                a2 = a % 10

                b1 = b // 10
                b2 = b % 10

                c1 = c // 10
                c2 = c % 10

                d1 = d // 10
                d2 = d % 10

                e1 = e // 10
                e2 = e % 10

                self.setN2(e2, e1);
                self.setN2(d2, d1);
                self.setN2(c2, c1);
                self.setN2(b2, b1);
                self.setN2(a2, a1);

                GPIO.output(self.two,1)
                time.sleep(0.001)
                GPIO.output(self.two,0)

                self.setN1(e2);
                self.setN1(d2);
                self.setN1(c2);
                self.setN1(b2);
                self.setN1(a2);

                GPIO.output(self.two, 1)
                time.sleep(0.001)
                GPIO.output(self.two, 0)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           setN1 function
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def setN1(self,n):
                for i in range(8):
                        if n is 0:
                                GPIO.output(self.sin,0)
                        else:
                                GPIO.output(self.sin,self.arr[n][i])
                        self.Timer(self.shcp)
                        self.Timer(self.stcp)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           setN2 function
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def setN2(self,a,b):
                for i in range(8):
                        if a==0 and b==0:
                                GPIO.output(self.sin,0)
                        else:
                        
                                GPIO.output(self.sin,self.arr[a][i])
                        self.Timer(self.shcp)
                        self.Timer(self.stcp)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Custom timer function
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def Timer(self,p):
                GPIO.output(p,0)
                time.sleep(0.001)
                GPIO.output(p,1)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Initialize pins output/input
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def init(self):
                GPIO.setup(self.one,GPIO.OUT)
                GPIO.setup(self.two,GPIO.OUT)
                GPIO.setup(self.stcp,GPIO.OUT)
                GPIO.setup(self.shcp,GPIO.OUT)
                GPIO.setup(self.sin,GPIO.OUT)
                GPIO.setup(self.green,GPIO.OUT)
                GPIO.setup(self.red,GPIO.OUT)
                GPIO.setup(self.buz,GPIO.OUT)

        def warningalert(self):
                self.blinkr()
                self.buzz()
                return
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           blink red led
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def blinkr(self):
                GPIO.output(self.red,1)
                time.sleep(0.5)
                GPIO.output(self.red,0)
                time.sleep(0.5)
                return

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           blink green led
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def blinkg(self):
                GPIO.output(self.green,1)
                time.sleep(2)
                return
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #           Cbuzzer alert
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def buzz(self):
                GPIO.output(self.buz,1)
                time.sleep(0.1)
                GPIO.output(self.buz,0)
                time.sleep(0.1)
                GPIO.output(self.buz,1)
                time.sleep(0.1)
                GPIO.output(self.buz,0)
                time.sleep(0.1)
                GPIO.output(self.buz,1)
                time.sleep(.1)
                return




                        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#           Normal alert
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def normalAlert(self):
                GPIO.output(self.buz,1)
                time.sleep(0.4)
                GPIO.output(self.buz,0)
                time.sleep(0.6)
                GPIO.output(self.buz,1)
                time.sleep(0.4)
                GPIO.output(self.buz,0)
                time.sleep(0.6)
                GPIO.output(self.buz,1)
                time.sleep(.4)
                GPIO.output(self.buz,0)
                time.sleep(0.6)
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
                                print 'found'
                                InsertData.isalerting=1
                                
                                t2=Thread(target=self.Box)
                                t2.start()
                                time.sleep(1)
                                self.normalAlert()
                                t1=Thread(target=self.display,args=(InsertData.toDisplay[0],InsertData.toDisplay[1],InsertData.toDisplay[2],InsertData.toDisplay[3],InsertData.toDisplay[4]))
                                t1.start()
                                #self.display(InsertData.toDisplay[0],InsertData.toDisplay[1],InsertData.toDisplay[2],InsertData.toDisplay[3],InsertData.toDisplay[4])
                                #alert call
                                #display function must be called with array toDisplay.
                                #GPIO.cleanup()
                                found=0
                        
                except:
                        print "Error: the database is being rolled back"
                        #global db
                        #db.rollback() 
                return
        def detectBox(self):
                InsertData.boxopen=1
                return 3

        
        def Box(self):        
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
                        

                        while (t2-t1)%5==0 and InsertData.boxopen ==0:
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
                                print "hello"
                                ackArray[boxid-1]=1
                                self.blinkg()
                        
                        print boxes
                        print ackArray
                        y=0
                        for y in range(0,5):
                                print y
                                if boxes[y][0]!=ackArray[y]:
                                        print y
                                        y=y-1
                                        break
                                
                                        

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

#insert.addRemove("1;2;1;0;0;0")
#insert.isRightTime('03:10:00')

#print insert.getPillsCount(1)
#t1=Thread(target=everyFive,args=("Thread",))

#insert=InsertData(name="checkTime")
#insert.starts()
#insert.start()
#insert.close()
insert.start()




        
