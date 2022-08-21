import os
import sys
import datetime
import configparser
from time import sleep
path = os.path.dirname(os.path.abspath(__file__)).replace('src', 'helper')
sys.path.append(path)
import database as db
from checker import checker

try:
    import telebot
    from telebot import types
except ImportError:
    os.system('pip install pyTelegramBotAPI')


parser = configparser.ConfigParser()
parser.read('config.ini')

TOKEN = parser.get('config', 'token')
if TOKEN.startswith('0123456789:ABCD'):
    print("Please set your token in config.ini")
    exit()
bot = telebot.TeleBot(TOKEN)

def patrol(repeating: int = 2):
    for many in range(repeating):
        for i in range(len(db.readidindb())):
            database_id = db.read_db_id()[i][0]
            trackingcode = db.readcode(database_id)
            userid_in_db = db.read_userid(database_id, trackingcode)
            # send a notification if there is a new status
            if checker.check(userid_in_db, trackingcode) == True:
                def usernewupdate():
                    try:
                        bot.send_message(chat_id=userid_in_db, text=f'Your shipment has been updated! \n\nTrackingcode: {trackingcode} \n\nStatus: {db.read_newstatus(userid_in_db, trackingcode)}')
                    except:
                        try:
                            bot.send_message(chat_id=userid_in_db, text=f'Your shipment has been updated! \n\nTrackingcode: {trackingcode} \n\nStatus: {db.read_newstatus(userid_in_db, trackingcode)}')
                        except Exception as e:
                            print(e, "error sending message")
                usernewupdate()
                print("Send Notification successfully")
                
            elif checker.check(userid_in_db, trackingcode) == 'arrived':
                db.delete_by_code(userid_in_db, trackingcode)
                print("Deleted")

            elif db.get_expirationdate(userid_in_db, trackingcode) <= db.get_creationdate(userid_in_db, trackingcode):
                print ('Deleted')
                db.delete_by_code(userid_in_db, trackingcode)
            elif checker.check(userid_in_db, trackingcode) == False:
                print("Nothing New", str(datetime.datetime.now().strftime("%m/%d %H:%M")), trackingcode)
                pass


# function to loop through the database and send a notification if there is a new status
def patrol_loop():   
    while True:
        patrol()
        sleep(7200)

patrol_loop()