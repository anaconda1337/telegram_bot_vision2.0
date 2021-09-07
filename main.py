#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from secrets import token_urlsafe
import pygsheets
import random
import time
import logging
import urllib.request
from lxml import html
from timeit import default_timer as timer
from datetime import timedelta
from past.builtins import raw_input
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import sys

gc = pygsheets.authorize(service_file='D:\\actual projects\\telegram_bot_vision2.0\\telegram_bot_vision2.0\\client_secret_pygsheet.json')
TOKEN = ('1901516841:AAEe0PXhD962So1JtSS9qUPUppPc_lALRTs')
DEBUG_MODE = True

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


counter_var = 0
domain_tld = ('.com', '.bg', '.org', '.info', '.net',)


def hello(update, context):
    start = timer()
    counter(update, context)
    list = ('Namaste!' , 'Greetings!' , 'Hallo!' , 'Holla!')
    update.message.reply_text(random.choice(list))
    stop_timer(start, timer())


def help(update, context):
    start = timer()
    counter(update, context)
    update.message.reply_text("""
    Vision can do:
    - hi - greetings;
    - help - commands list.
    - check - tasks counter;
    - execute url (example: google.com)
    - time - it shows current date & time;
    - location - it shows your current location;
    - joke - stun you with random joke;
    """)
    stop_timer(start, timer())


def check(update, context):
    start = timer()
    counter(update, context)
    update.message.reply_text(f"Tasks done: " + str(counter_var))
    stop_timer(start, timer())


def open_web(update, context):
    start = timer()
    counter(update, context)
    update.message.text.startswith("https://")
    update.message.text.startswith("http://")
    if update.message.text.startswith("https://") is False or update.message.text.startswith("http://") is False:
        update.message.text = "https://" + update.message.text
    update.message.reply_text(update.message.text)
    os.startfile(update.message.text)
    stop_timer(start, timer())


def time(update, context):
    start = timer()
    counter(update, context)
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    update.message.reply_text("Current time: " + current_time)
    from datetime import date
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    update.message.reply_text("Current date: " + current_date)
    stop_timer(start, timer())


def location(update, context):
    start = timer()
    counter(update, context)
    import urllib.request
    import json
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        update.message.reply_text(data)
    stop_timer(start, timer())


def random_joke(update, context):
    start = timer ()
    counter(update, context)
    import pyjokes
    joke = pyjokes.get_joke(language='en', category='chuck')
    update.message.reply_text(joke)
    stop_timer(start, timer())


def counter(update, context):
    global counter_var
    counter_var += 1
    print(f'Functions counter is: {counter_var}')
    sh = gc.open('Vision')
    wks = sh[0]
    wks.update_value("E2", counter_var)


def stop_timer(start_time, end_time):
    parent_function = sys._getframe(1).f_code.co_name
    time_delta = (end_time - start_time)
    if DEBUG_MODE: print(f'Function [{parent_function}] executed in {time_delta}')
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    from datetime import date
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    print('-------------------------------------------------------------------')
    sh = gc.open('Vision')
    wks = sh[0]
    wks.insert_rows(row=1, number=1, values=[time_delta, parent_function, current_time, current_date])


def save_data(metric_name, metric_value):
    return True


def echo(update, context):
    """Echo the user message."""
    print(f'User with ID: {update.message.from_user.id} has executed a function')

    if update.message.text.lower() == 'hi':
        hello(update, context)
        return

    if update.message.text.lower() == "help":
        help(update, context)
        return

    if update.message.text.lower() == "check":
        check(update, context)
        return

    if update.message.text.endswith(domain_tld):
        open_web(update, context)
        return

    if update.message.text.lower() == "time":
        time(update, context)
        return

    if update.message.text.lower() == "location":
        location(update, context)
        return

    if update.message.text.lower() == "joke":
        random_joke(update, context)
        return

    else:
        update.message.reply_text(f"""Unknown command: {update.message.text}
You also may be unauthorised user.""")
        update.message.reply_text("input your 4 digits key: ****")
        print("unauthorised user")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
