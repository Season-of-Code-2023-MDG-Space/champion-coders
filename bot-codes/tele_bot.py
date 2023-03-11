from telegram import Poll,ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    PollHandler,
)

from fetch import QuizQuestion
import api
import logging
import logging.config
import os
import telegram
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
    logging.info(f"question : {update.poll.question}")
    logging.info(f"correct option : {update.poll.correct_option_id}")
    logging.info(f"option #1 : {update.poll.options[0]}")
    logging.info(f"option #2 : {update.poll.options[1]}")
    logging.info(f"option #3 : {update.poll.options[2]}")

    user_answer = get_answer(update)
    logging.info(f"correct option {is_answer_correct(update)}")

    add_typing(update, context)
    add_text_message(update, context, f"Correct answer is {user_answer}")


def start_command_handler(update, context):
    update.message.reply_text("Please enter the number of questions you want to answer")

    
    # b=int(input())
    # for i in range (0,b):
   
    dict=QuizQuestion.questions()
    add_typing(update, context)
            

    add_quiz_question(update,context,dict)



def add_quiz_question(update, context ,dict):
    
    message = context.bot.send_poll(
        chat_id=get_chat_id(update, context),
        question=dict[0],
        options=dict[4],
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
    time.sleep(1)

def no_of_questions(user_input):
    s=user_input
    return s


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
    print('Welcome,Please use /start command to start me')
    dispatcher.add_handler(CommandHandler("help", help_command_handler))
    dispatcher.add_handler(CommandHandler("start", start_command_handler))

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

   
    
    updater.start_polling()
    logging.info(f"Start polling mode")

    updater.idle()



class DefaultConfig:
    PORT = int(os.environ.get("PORT", 3978))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "6049110046:AAGDMulUlNMrL-DCf2Qy2LLorYDCA6DQ4zQ")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

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