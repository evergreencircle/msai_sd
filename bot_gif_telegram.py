
import telegram
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram import Update
from telegram import User
from telegram import Message
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from pony.orm import *
import requests
import json


# bot initialization
bot = telegram.Bot(token='5259186766:AAEJbHxJs0P0_uhO3aOA1UMDnP4KRvHTdKA')
updater = Updater(token='5259186766:AAEJbHxJs0P0_uhO3aOA1UMDnP4KRvHTdKA', use_context=True)
dispatcher = updater.dispatcher


# db part
db = Database()

class Person(db.Entity):
    userId = Required(int)
    inter = Required(str)


db.bind(provider='sqlite', filename='/tmp/database.sqlite', create_db=True)

db.generate_mapping(create_tables=True)

set_sql_debug(True)

@db_session
def add_theme(userId1, inter1):
    Person(userId=userId1, inter=inter1)

@db_session
def get_stat(userId1):
    lst1 = []
    persons = select(p for p in Person if p.userId == int(userId1))
    if len(persons) == 0:
        return 0
    else:   
        for p in persons:
            lst1.append(str(p.inter))
        return lst1



# set the apikey and limit for GIF API
def findGIF(lmt, search):
    apikey = "FIGH2RB8TW1A"  # test value
    search_term = search

# get the top 8 GIFs for the search term
    r = requests.get(
    "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt, ))

    if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    lstLink = []
    for key in range(lmt):
        lstLink.append(top_8gifs['results'][key]['media'][0]['tinygif']['url'])
    return(lstLink)




def start(update: Update, context: CallbackContext):
    msg1 = "Hello! This Gif bot. \n \n"
    msg2 = "To get GIFs, type: \n"
    msg3 = "/get (theme) (number of gifs).\n"
    msg0 = "Number of gifs must be less than 4\n"
    msg4 = "Example: /get exciting 4 \n \n"
    msg5 = "To get  history of your queries, type: \n"
    msg6 = "/myhistory  \n"
    context.bot.send_message(chat_id=update.effective_chat.id, text= msg1 + msg2 + msg3 + msg4 + msg5 + msg6)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



def get(update: Update, context: CallbackContext):
    text_caps = context.args
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Wait few seconds, please.")
    msg1 = 'Sorry, the format of /get is wrong. \n'
    msg2 = 'Type /get, then theme as one word, quantity as an integer number less than 6 \n'
    msg3 = "Example: /get fun 4 \n \n"
    msg = msg1 + msg2 + msg3 
    try:
        if str(type(text_caps[0])) == "<class 'str'>" and str(type(int(text_caps[1]))) == "<class 'int'>" and (0 < int(text_caps[1]) < 6) and len(text_caps) == 2 :
            theme = text_caps[0]
            number = text_caps[1]
            userId = update.effective_user.id
            add_theme(int(update.effective_user.id), str(theme))
            lst = findGIF(int(number), str(theme))
            for link in lst:
                context.bot.send_animation(chat_id=update.effective_chat.id, animation = str(link))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text= msg)
    except: 
        context.bot.send_message(chat_id=update.effective_chat.id, text= msg)

get_handler = CommandHandler('get', get)
dispatcher.add_handler(get_handler)



def myhistory(update: Update, context: CallbackContext):
    text_caps = context.args
    userId = update.effective_user.id
    persons = get_stat(update.effective_user.id)
    if persons == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text= 'You have no previous queries')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Your prevous queries:")
        for theme in persons:
            context.bot.send_message(chat_id=update.effective_chat.id, text= theme)  
    
myhistory_handler = CommandHandler('myhistory', myhistory)
dispatcher.add_handler(myhistory_handler)




def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, only commands /get and /myhistory are allowed")

echo_handler = MessageHandler(Filters.text | Filters.command, echo)
dispatcher.add_handler(echo_handler)




updater.start_polling()






