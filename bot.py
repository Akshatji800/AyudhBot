import logging
import tweepy
import tweepy
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
http_api = environ['http_api']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
tweets = []
dt = date.today() - timedelta(1)
userID = "ayudh_india"


def city(update, context,*args):
    try:
        city=context.args[0]
    except:
        update.message.reply_text("Hey, User I also need the name of a place after /place. Let me give you an example: /place mumbai")
    update.message.reply_text("The city has been set as:"+city+"\nEnter /count for number of tweets")
    f = open("city.txt", "w")
    f.write(city)
    f.close()


def numberOfTweets(update: Update, _: CallbackContext) -> None:
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
    update.message.reply_text('Select maximum number of tweets: ', reply_markup=reply_markup)


def scraper(city):
    tweets = api.user_timeline(screen_name=userID, 
                           count=100,
                           include_rts = False,
                           tweet_mode = 'extended'
                          )

    tweet_handler={}
    fetched_tweets= []

    for tweet in tweets:
        tweet_handler[tweet.id_str]= tweet.full_text.encode("utf-8").decode("utf-8")

    for k,v in tweet_handler.items():
        if city.lower() in v.lower():
            fetched_tweets.append(k)
    return fetched_tweets


def button(update: Update, _: CallbackContext) -> None:

    query = update.callback_query
    
    f = open("city.txt", "r")
    city=f.read()
    f.close()

    bot = telegram.Bot(token=http_api)  
    query.answer()

    if(city=='%20'or city==''):
        city='India'

    tweet_ids=scraper(city)
    counter=0
    for i in range(len(tweet_ids)):
        counter= counter+1
        links= 'https://twitter.com/ayudh_india/status/'+tweet_ids[i]
        bot.sendMessage(update.effective_user.id,text=links)
        if counter==int(query.data):
            break
    
    bot.sendMessage(update.effective_user.id,text="Number of Tweets found: " + str(counter))

    

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /city CITY NAME to enter the city name.\nUse /numberOfTweets to choose number of tweets")

def bot_intro(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("HI, User I am ayudhfightscovidBot 'Helping Ayudh to fight and help people in Covid times'. To use me just type /place <PLACE NAME> and then type /count and choose the number of tweets you want from the options available ")

def main() -> None:
    
    updater = Updater(http_api)
    updater.dispatcher.add_handler(CommandHandler('start', bot_intro))
    updater.dispatcher.add_handler(CommandHandler('city', city))
    updater.dispatcher.add_handler(CommandHandler('count', numberOfTweets))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    f = open("city.txt", "w")
    f.write(' ')
    f.close()
    main()