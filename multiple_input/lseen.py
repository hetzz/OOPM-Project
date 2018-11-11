import datetime

try :
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import threading
import time

lastseendict = {}

db = None
cursor = None
query = ""
stop = False

t1 = None
def dbupdate():
    global query
    while not stop:
        if query != "":
            querycp = query[:]
            print(query)
            query = ""

            cursor.execute(querycp)
            db.commit()
        time.sleep(2)
    print('ending sql thread')


def to_store_or_not(name):
    if lastseendict.get(name, None)!= None:
        diff = datetime.datetime.now() - lastseendict[name][-1][0]
        c = divmod(diff.days * 86400 + diff.seconds, 60)
        if c[0] >= 1:
            return True
        else:
            return False
    return True

def store(name):
    global query
    if to_store_or_not(name):
        print(lastseendict.get(name, []))
        if lastseendict.get(name, None) == None:
            lastseendict[name] = [(datetime.datetime.now(), 'Matunga')]
        else:
            lastseendict[name].append((datetime.datetime.now(), 'Matunga'))
        query += "INSERT INTO `finds` (`Name`, `Location`, `Time`) VALUES ('"+name+"', 'Matunga', '"+str(lastseendict[name][-1][0])[:-7]+"');"


        print('stored', lastseendict)
        return True
    return False

def openconnection(onLAN = True):
    global db
    global cursor
    global query
    if onLAN:
        db = pymysql.connect("192.168.15.151","root","@kshayps9","oopmproj" )
    else:
        db = pymysql.connect("db4free.net","akshay_07cf","@kshayps9","oopmproj" )
    cursor = db.cursor()
    # cursor.execute("SET time_zone = '+5:30'")
    db.commit()
    dbclosed = False
    query = ""
    global t1
    t1 = threading.Thread(target=dbupdate, args=[])
    t1.start()

def closeconnection():
    global stop
    global query
    while query != "" :
        time.sleep(0.5)
    stop = True
    query = ""
    print(stop)
    t1.join()
    db.close()
    print('closed db')
