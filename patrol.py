import os
try:
    import telebot
except ImportError:
    os.system("pip install pyTelegramBotAPI ")
from checker import checker
from time import sleep
import datetime
import database as db


# telegram bot token
TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

def patrol(repeating: int = 3):
    for many in range(repeating):
        for i in range(len(db.readidindb())):
            codebyid = db.readcode(db.readidindb()[i][0])
            id_in_db = db.readidindb()[i][0]
            # send a notification if there is a new status
            if checker.check(id_in_db, codebyid) == True:
                def usernewupdate():
                    try:
                        bot.send_message(chat_id=id_in_db, text=f'Your shipment has been updated! \n\nTrackingcode: {codebyid} \n\nStatus: {db.read_newstatus(id_in_db, codebyid)}')
                    except:
                        try:
                            bot.send_message(chat_id=id_in_db, text=f'Your shipment has been updated! \n\nTrackingcode: {codebyid} \n\nStatus: {db.read_newstatus(id_in_db, codebyid)}')
                        except Exception as e:
                            print(e, "error sending message")
                usernewupdate()
                print("Send Notification successfully")
                
            elif checker.check(id_in_db, codebyid) == 'arrived':
                    # c.execute(f"DELETE FROM data WHERE userid = {id_in_db} AND code = '{codebyid}'")
                    # conn.commit()
                    print("Deleted")

            elif db.get_expirationdate(id_in_db, codebyid) <= db.get_creationdate(id_in_db, codebyid):
                print ('Delete')
                db.delete_by_code(id_in_db, codebyid)
            elif checker.check(id_in_db, codebyid) == False:
                print("Nothing New", str(datetime.datetime.now().strftime("%m/%d %H:%M")), codebyid)



while True:
    patrol(2)
    sleep(7200) #repeating every 2 hours