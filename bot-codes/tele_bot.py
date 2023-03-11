from telegram import Poll,ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext,
    PollHandler,
)
from api import apiView
from fetch import QuizQuestion

import logging
import logging.config
import os
from telegram import *
import requests
import json

import time
import datetime

def main_handler(update, context):
    logging.info(f"update : {update}")

    if update.message is not None:
        user_input = get_text_from_message(update)
        logging.info(f"user_input : {user_input}")

        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")


def help_command_handler(update, context):
    update.message.reply_text("Type /start")


def poll_handler(update, context):
    scorecard=0
    user_answer = get_answer(update)
    
    logging.info(f"correct option {is_answer_correct(update)}")
    # add_typing(update, context)
    # add_text_message(update, context, f"Correct answer is {update.poll.options[update.poll.correct_option_id]['text']}")

def answer_counter(update,context):
    counter=0
    if is_answer_correct(update)==True:
        counter=counter+1
    return counter

def start_command_handler(update, context):
    update.message.reply_text("Please enter the number of questions you want to answer(1-10) in the format /quiz<space>number of questions")
    

    
def quiz_command_handler(update,context):
    try:
        Number_of_questions=int(context.args[0])
        for i in range (0,Number_of_questions):
            dict=apiView.apiCall()
            add_typing(update, context)
            add_quiz_question(update,context,dict)
            add_typing(update, context)
            time.sleep(0.5)
    except:
        add_text_message(update, context, f"Please provide the correct format")





def add_quiz_question(update, context ,dict):
    
    message = context.bot.send_poll(
        chat_id=get_chat_id(update, context),
        question=dict[2],
        options=dict[1],
        type=Poll.QUIZ,
        correct_option_id=dict[3],
        open_period=8,
        is_anonymous=True,
        
    )

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    context.bot_data.update({message.poll.id: message.chat.id})


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(0.7)




def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update, context), text=message)

def get_text_from_message(update):
    return update.message.text



def get_answer(update):
    answers = update.poll.options

    ret = ""

    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text

    return ret


def is_answer_correct(update):
    answers = update.poll.options

    ret = False
    counter = 0

    for answer in answers:
        if answer.voter_count == 1 and update.poll.correct_option_id == counter:
            ret = True
            break
        counter = counter + 1

    return ret


# extract chat_id based on the incoming object
def get_chat_id(update, context):
  chat_id = -1

  if update.message is not None:
    chat_id = update.message.chat.id
  elif update.callback_query is not None:
    chat_id = update.callback_query.message.chat.id
  elif update.poll is not None:
    chat_id = context.bot_data[update.poll.id]

  return chat_id


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN,
                  use_context=True)
    dispatcher = updater.dispatcher
   
    dispatcher.add_handler(CommandHandler("help", help_command_handler))
    dispatcher.add_handler(CommandHandler("start", start_command_handler))
    dispatcher.add_handler(CommandHandler("quiz",quiz_command_handler))

    # message handler
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))



    # suggested_actions_handler
    dispatcher.add_handler(
        CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True)
    )

    # quiz answer handler
    dispatcher.add_handler(PollHandler(poll_handler, pass_chat_data=True, pass_user_data=True))

    # log all errors
    dispatcher.add_error_handler(error)

   
    
    # updater.start_webhook(
    #     listen="0.0.0.0",
    #     port=int(DefaultConfig.PORT),
    #     url_path=DefaultConfig.TELEGRAM_TOKEN,
    #     webhook_url=DefaultConfig.WEBHOOK_URL+DefaultConfig.TELEGRAM_TOKEN
    # )

    # logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    updater.start_polling()
    logging.info(f"Start polling mode")

    updater.idle()



class DefaultConfig:
    PORT = int(os.environ.get("PORT", 8443))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "6049110046:AAHX0wlv39PRwEJRSIXAfZVIWDDoJwxwlZw")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://webhook.site/c09aeb51-af69-446b-93c7-a6d96c5d52d4")

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )


if __name__ == "__main__":

    # Enable logging
    DefaultConfig.init_logging()

    main()
