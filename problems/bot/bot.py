#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
from bs4 import BeautifulSoup
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Привет! Я буду присылать тебе случайные цитатки с bash.im!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(get_quote())


def get_quote():
    r = requests.get(f'http://bash.im/random')
    soup = BeautifulSoup(r.text)
    quote = soup.find('div', {"class" : "quote"})
    result = []
    for line in quote.strings:
        print(line)
        line = line.strip()
        if len(line) > 0:
        	result.append(line)
    print(result)
    return ' '.join(result[:2]) + '\n'.join(result[2:])

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("589200803:AAHT-dOuHnMxDAJ4XyHBJeMvAtiBI0ZCeoI")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
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