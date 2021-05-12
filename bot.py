import logging
import os
import tweepy
from tweepy import OAuthHandler
from os import environ
import telegram
from datetime import date, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

access_token = environ['access_token']
access_token_secret = environ['access_token_secret']
consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
http_api = '1861020319:AAF8FdbUufg4Gxo_1k5xXUgn2h4Q34m7Yoo'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
tweets = []
dt = date.today() - timedelta(1)
userID = "ayudh_india"

def menu(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("5", callback_data=5),
            InlineKeyboardButton("10", callback_data=10),
        ],
        [
            InlineKeyboardButton("15", callback_data=15),
            InlineKeyboardButton("20", callback_data=20)
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose one of the following :', reply_markup=reply_markup)

def scraper(city)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name=userID, 
                           count=100,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )

fetched_tweets= []
i=0
while (i<100):
    dict= dict.append({tweet.id_str,tweet.full_text.encode("utf-8").decode("utf-8")})
    i= i+1
for k,v in dict.items():
    if(v.find(city)):
        fetched_tweets.append(k)
        
        

def city(update, context,*args):
    city=context.args[0]
    update.message.reply_text("The city has been set as:"+city+"\nEnter /menu for the options")
    f = open("city.txt", "w")
    f.write(city)
    f.close()

def scrapetweets(city):
    
    new_search = "verified "+ city
    link=[]

    for tweet in tweepy.Cursor(api.search, q=new_search, lang="en",count=100,since=dt).items(int(data[0])):

        try: 
            data = [tweet.id]
            link.append(f"https://twitter.com/ayudh_india"+str(data[0]))
        
        except tweepy.TweepError as e:
            print(e.reason)
            continue

        except StopIteration:
            break

    return link

def button(update: Update, _: CallbackContext) -> None:

    query = update.callback_query
    
    f = open("city.txt", "r")
    city=f.read()
    f.close()

    bot = telegram.Bot(token=http_api)  
    query.answer()

    if(city=='%20'or city==''):
        city='India'

    link=scrapetweets(city,str(query.data))
    
    if (len(link)>0):
        bot.sendMessage(update.effective_user.id,text=f"{len(link)} 𝐫𝐞𝐜𝐞𝐧𝐭 𝐭𝐰𝐞𝐞𝐭𝐬 𝐚𝐫𝐞:\n")
    else:
        bot.sendMessage(update.effective_user.id,text=f"𝐒𝐨𝐫𝐫𝐲, 𝐍𝐨 𝐫𝐞𝐜𝐞𝐧𝐭 𝐭𝐰𝐞𝐞𝐭𝐬 𝐰𝐞𝐫𝐞 𝐟𝐨𝐮𝐧𝐝\n")

    for i in link:
        bot.sendMessage(update.effective_user.id,text=i)

    
    search=f"https://twitter.com/ayudh_india/search?q=verified%20"+city+":retweets&f=live"
    
    bot.sendMessage(update.effective_user.id,text="𝐓𝐨 𝐯𝐢𝐞𝐰 𝐚𝐥𝐥 𝐭𝐡𝐞 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐜𝐥𝐢𝐜𝐤 𝐭𝐡𝐢𝐬 𝐥𝐢𝐧𝐤:\n")
    bot.sendMessage(update.effective_user.id,text=search)

    
    
    

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /city CITY NAME to enter the city name.\nUse /menu to start using the covid resource bot")


def main() -> None:
    

    updater = Updater(http_api)
    updater.dispatcher.add_handler(CommandHandler('city', city))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    f = open("city.txt", "w")
    f.write(' ')
    f.close()
    main()

