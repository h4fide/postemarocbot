import os
import sqlite3
from api import Tracker
from datetime import date, timedelta

databasepath = r'./db.db'
conn = sqlite3.connect(databasepath, check_same_thread=False)
c = conn.cursor()


def createtable():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT,
         userid INTEGER, firstname TEXT, code TEXT, currentstatus TEXT,
          newstatus TEXT, title TEXT, creationdate TEXT, expirationdate TEXT)""")
        conn.commit()
    except:
        pass

def checkindb(userid, trackingcode):
    c.execute("SELECT * FROM data WHERE (userid = ?  AND code = ?)", (userid, trackingcode))
    entry = c.fetchone()
    if entry is None:
        return True
    else:
        return False

def getidindb(userid, i):
    c.execute("SELECT * FROM data WHERE userid = '{}'".format(userid))
    return c.fetchall()[i][0]

def delete_by_id(id):
    c.execute(f"DELETE FROM data WHERE id={id}" )
    conn.commit()

def delete_by_code(id_in_db, codebyid):
    c.execute(f"DELETE FROM data WHERE userid = {id_in_db} AND code = '{codebyid}'")
    conn.commit()

def archive(userid):
    c.execute("SELECT * FROM data WHERE userid = '{}'".format(userid))
    return c.fetchall()

def creationdate():
    current_date = date.today().isoformat()   
    return current_date

def expirydate():
    return (date.today()+timedelta(days=50)).isoformat()
        
def createindb(usercode, title):
    status= Tracker.LastStatus(usercode.text)
    userid = int(usercode.from_user.id)
    firstname= usercode.from_user.first_name
    trackingcode = usercode.text
    params = (userid, firstname, trackingcode, status, status, title, creationdate(), expirydate())
    c.execute("SELECT * FROM data WHERE (userid = ?  AND code = ?)", (userid, trackingcode))
    entry = c.fetchone()
    if entry is None:
        c.execute("INSERT INTO data VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        conn.commit()
        print("New Entry Added") 
    else:
        print("Entry Found")
        
def checkindb(userid, trackingcode):
    c.execute("SELECT * FROM data WHERE (userid = ?  AND code = ?)", (userid, trackingcode))
    entry = c.fetchone()
    if entry is None:
        return True
    else:
        return False

# userid in the database 
def readidindb():
    c.execute("SELECT userid FROM data")   
    readid = c.fetchall()
    return readid

# trackingcode in the database
def trackindb():
    c.execute("SELECT code FROM data")   
    track = c.fetchall()
    return track

# status in the database
def statusindb(userid, trackingcode):
    c.execute(f"SELECT currentstatus FROM data WHERE userid = '{userid}' AND code = '{trackingcode}'")   
    status = c.fetchall()
    return status

# printing the status in the database
def readcode(userid):
    c.execute(f"SELECT code FROM data WHERE userid = '{userid}'")
    return c.fetchone()[0]

# check if the status is the same as the status in the database
def get_creationdate(userid, trackingcode):
    c.execute(f"SELECT creationdate FROM data WHERE userid = '{userid}' AND code = '{trackingcode}'")
    return c.fetchone()[0]

def get_expirationdate(userid, trackingcode):
    c.execute(f"SELECT expirationdate FROM data WHERE userid = '{userid}' AND code = '{trackingcode}'")
    return c.fetchone()[0]

# checker
def read_currentstatus(userid,tcode):
    c.execute(f"SELECT userid, code, currentstatus FROM data WHERE userid = '{userid}' AND code = '{tcode}'")   
    readstatus = c.fetchone()[2]
    return readstatus

def read_newstatus(userid, tcode):
    c.execute(f"SELECT userid, code, newstatus FROM data WHERE userid = '{userid}' AND code = '{tcode}'")   
    readnewstatus = c.fetchone()[2]
    return readnewstatus

def create_newtstatus(laststatut, userid, tcode):
    c.execute(f"UPDATE data SET newstatus = '{laststatut}' WHERE userid = '{userid}' AND code = '{tcode}' ")
    conn.commit()

def create_currentstatus(laststatut, userid, tcode):
    c.execute(f"UPDATE data SET currentstatus = '{laststatut}' WHERE userid = '{userid}' AND code = '{tcode}' ")
    conn.commit()

