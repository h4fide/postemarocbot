import os
import sys
path = os.path.dirname(os.path.abspath(__file__)).replace('src', 'helper')
sys.path.append(path)
import configparser
import database as db
from api import Tracker

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
    TOKEN = os.environ['TOKEN']
    
bot = telebot.TeleBot(TOKEN)

#creat table if not exists 
db.createtable()

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Submit your Tracking Code to view all available delivery information! \n
Commands:\n/start \n/help \n/notifyme \n/mycodes
""")


@bot.message_handler(commands=['notifyme'])
def notifyme(message):
    bot.send_message(message.chat.id, 'Send your trackingcode i will save it and notify you when gets updated')
    bot.register_next_step_handler(message, notifycode)

def notifycode(code):
    global tcode
    tcode = code
    lenth = int(len(code.text))
    try:
        if lenth >= 9 and lenth <= 26 and ' ' not in str(code.text) and code.text.isupper() and code.text[0].isalpha() and '''!()[]{};:'"\,<>./?@#$%^&*_~''' not in code.text:
            laststatut = Tracker.LastStatus(code.text)
            if laststatut == 'Envoi livré':
                bot.reply_to(code, 'Your shipment has been delivered! \n I can send you a notification its been delivered')
            else:
                if db.checkindb(code.from_user.id, code.text) == True:
                    bot.send_message(code.chat.id, 'Add Title To Your TrackingCode \n(e.g. Watch, Phone, etc...)')
                    bot.register_next_step_handler(code, save)
                else:
                    bot.send_message(code.chat.id, 'Your tracking code is already saved')
        else:
            bot.reply_to(code,"Invalid Tracking Number ❌")
    except Exception as e:
        bot.reply_to(code, 'Error, please try again')
        print('error' + str(e))
def save(title):
    try:
        db.createindb(tcode, title.text)
        bot.send_message(title.chat.id, f'Title saved: {title.text} \nYour code : {tcode.text}')
        print(f'title saved: {title.text} \nYour code is: {tcode.text}')
        bot.reply_to(title, f"OK. {title.from_user.first_name} I will notify you when it gets updated")
    except Exception as e:
        bot.send_message(title.chat.id, 'Error, please try again')
        print('error' + str(e))

@bot.message_handler(commands=['mycodes'])
def archive(message):
    try:
        if len(db.archive(message.from_user.id)) == 0:
            bot.send_message(message.chat.id, 'You have no saved codes')        
        else :
            bot.reply_to(message, "You have {} trackingcode".format(len(db.archive(message.from_user.id))))
        for i in range(len(db.archive(message.from_user.id))):
            idrow = db.getidindb(message.from_user.id, i)+ 375
            start_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            btn1= telebot.types.InlineKeyboardButton('Delete 🗑', callback_data='back')
            start_markup.add(btn1)
            bot.send_message(message.chat.id, f"TRACKINGCODE: {db.archive(message.from_user.id)[i][3]}\nTITLE: {db.archive(message.from_user.id)[i][6]}\nID: {idrow}",reply_markup=start_markup )
            if i == len(db.archive(message.from_user.id)):
                break
    except:
        bot.reply_to(message, "Error, please try again")

@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_callback(call: types.CallbackQuery):
    try:    
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text='Done ✔', reply_markup=None)
        ids = []
        for id in call.message.text.split('\n'):
            ids.append(id.strip().split(':'))
        id = int(ids[2][1])-375
        db.delete_by_id(id)
        bot.answer_callback_query(call.id, "Your trackingcode has been deleted")
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text='Error, please try again', reply_markup=None)


def infos(id, tcode):
    listkeys = ['Code', 'Product name', 'Deposit date',
     'Destination', 'Delivery date', 'Weight', 'Recipient',
      'Latest status', 'Deposit local', 'Id statut', 'Code sitebam',
       'Price', 'Deligard'] 
    listkeys2 = ['code_bordereau', 'libelle_produit', 'date_depot',
     'destination', 'date_livraison', 'poids', 'destinataire',
      'dernier_statut', 'lieu_depot', 'id_statut', 'code_sitebam',
       'mtt_crbt', 'delaigarde'] 

    status = Tracker.PackageInfo(tcode)
    list = []
    for i in range(len(listkeys)):
        ret = status[listkeys2[i]]
        if ret == 'Neant' or ret == "" or ret == '.':
            ret = 'Not Available'
        list.append(ret)
    returninfo = f"{listkeys[0]}: {list[0]}\n{listkeys[1]}: {list[1]}\n{listkeys[2]}: {list[2]}\n{listkeys[3]}: {list[3]}\n{listkeys[4]}: {list[4]}\n{listkeys[5]}: {list[5]}\n{listkeys[6]}: {list[6]}\n{listkeys[7]}: {list[7]}\n{listkeys[8]}: {list[8]}\n{listkeys[9]}: {list[9]}\n{listkeys[10]}: {list[10]}\n{listkeys[11]}: {list[11]}\n{listkeys[12]}: {list[12]}" 
    bot.send_message(id, f"Your package is in the following status:\n{returninfo}")

@bot.message_handler(func=lambda message: True)
def tracking(code):
    try:
        print(code.text)
        lenth = int(len(code.text))
        if lenth >= 9 and lenth <= 26 and ' ' not in str(code.text) and code.text.isupper() and code.text[0].isalpha() and '''!()[]{};:'"\,<>./?@#$%^&*_~''' not in code.text:
            laststatus= str(Tracker.LastStatus(code.text))
            if laststatus == 'Envoi livré':
                bot.reply_to(code, 'Your shipment has been delivered! \nDelivery date: ' + str(Tracker.PackageInfo(code.text)['date_livraison']))
                infos(code.chat.id , code.text)
            elif laststatus == 'Info unavailable':
                bot.reply_to(code, 'Info Unavailable At The Moment')
                bot.send_message(code.chat.id, 'It seems that your shipment is not registered in the system yet \nI will keep you updated just use \nthe /notifyme command')
            else:
                bot.reply_to(code, laststatus)
                infos(code.chat.id , code.text)
        
        else:
            bot.reply_to(code,"Invalid Tracking Number ❌")
    except:
        bot.send_message(code.chat.id,"Something went wrong please try again ")


if __name__ == '__main__':
    bot.infinity_polling()