import MySQLdb
import datetime
import time

db = None
curs = None

def starts():
    global db
    db=MySQLdb.connect("localhost","root","123","MedicineBox")
    global curs
    curs=db.cursor()

def close():
    global curs
    curs.close()
    global db
    db.close()


def insertData(Id,Pills,start,Duration,Mon,Tue,Wed,Thu,Fri,Sat,Sun):
    try:
        curs.execute("""UPDATE MedicineBox SET NumberOfPills=%s,StartingTime=%s,TimeDuration=%s,
                               Mon=%s,Tue=%s,Wed=%s,Thu=%s,Fri=%s,Sat=%s,Sun=%s Where BoxId=%s """,(Pills,start,Duration,Mon,Tue,Wed,Thu,Fri,Sat,Sun,Id))
               # curs.execute("""UPDATE MedicineBox SET NumberOfPills=%s Where BoxId=%s """,(Pills,Id))
        db.commit()

    except:
        print "Error: the database is being rolled back"
        db.rollback()


def addRemovePills(Id,addRemove,number):
        
        #if it add addRemove=1 else addRemove=0
       
    try:
        curs.execute("""SELECT NumberOfPills FROM MedicineBox
                                     WHERE BoxId=%s""",(Id))
        [int(record[0]) for record in curs.fetchall()]
               
        currentPills=record[0]

        totalPills=0
        if addRemove == 1:
            totalPills = currentPills + number

        elif addRemove == 0:
            totalPills = currentPills - number

        curs.execute("""UPDATE MedicineBox SET NumberOfPills=%s Where BoxId=%s """,(totalPills,Id))
        db.commit()
        
    except:
        print "Error: the database is being rolled back"
        db.rollback()

def getPillsCount(Id):
       

    try:
        curs.execute("""SELECT NumberOfPills FROM MedicineBox
                                     WHERE BoxId=%s""",(Id))

        [int(record[0]) for record in curs.fetchall()]
               
        return record[0]

               
    except:
        print "Error: the database is being rolled back"
        db.rollback()

def split1(stri):
    a = stri.split(';')
    insertData(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10])

def addRemove(stri):
    a=stri.split(';')
    addRemovePills(1,int(a[0]),int(a[1]))
    addRemovePills(2,int(a[0]),int(a[2]))
    addRemovePills(3,int(a[0]),int(a[3]))
    addRemovePills(4,int(a[0]),int(a[4]))
    addRemovePills(5,int(a[0]),int(a[5]))

starts()
split1("1;2;18:27:00;6;1;1;1;1;1;1;1")
#split1("3;2;18:27:00;6;1;1;1;1;1;1;1")
#addRemove("1;2;1;0;0;0")
close()





