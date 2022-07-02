
# This program is a copy right software.

"""
A Bot to handle University shuttle business in a University using natural language processing.
However, the locations can be modified to preferred institution.

Dataset:
The dataset for this bot is in this source code. Like the destination and the bot responses.

Usage:
Example of a shuttle management bot using different python modules.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

"""


import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# GENDER, PHOTO, LOCATION, BIO = range(4)

GENDER, DESTINATION, LOCATION, BIO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    # Starts the conversation and asks the user about their gender.
    reply_keyboard = [['Student', 'Non-Student', 'Pilot']]

    update.message.reply_text(
        'Hi! This is Covenant university Shuttle management system chatbot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'please select if you are "student, non-student or a pilot?"',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Student, Non-student or pilot?'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    #  Stores gender and asks the user about their destination.
    user = update.message.from_user
    logger.info("Gender of %s %s: %s", user.first_name, user.last_name, update.message.text)
    reply_keyboard = [['EIE', 'CST', 'Others']]
    # if statement
    client_firstname = user.first_name
    client_lastname = user.last_name
    if client_firstname == str():
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
        )
    else:
        pass
    # new command
    update.message.reply_text(
        'Thank you! Now I would like to know where you are heading to.'
        'Send /cancel to stop talking to me.\n\n'
        'Are you going to EIE, CST, or other places?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='EIE, CST or other places?'
        ),
    )
    return DESTINATION


def destination(update: Update, context: CallbackContext) -> int:
    #  Stores destination and asks the user about their location.
    user = update.message.from_user
    logger.info("Destination of %s %s: %s", user.first_name, user.last_name, update.message.text)
    update.message.reply_text(
        'Excellent! Now, send me your location using telegram please, or send /skip if you don\'t want to.'
    )
    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    # Stores the location and asks for some info about the user.
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s %s: %f / %f", user.first_name, user.last_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Shuttle arrives  (at x time) . \n You can write a comment or a suggestion on CUSMS or click on /cancel to '
        'stop '
        'talking to me '
    )
    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    # Skips the location and asks for info about the user.
    user = update.message.from_user
    logger.info("User %s %s did not send a location.", user.first_name, user.last_name)
    update.message.reply_text(
        'Ok. Shuttle will arrive (at x time). \n Do you need something else (yes or no).'
    )
    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    # Stores the info about the user and ends the conversation.
    user = update.message.from_user
    logger.info("Bio of %s %s: %s", user.first_name, user.last_name, update.message.text)
    update.message.reply_text('Thank you! If you need any assistance for a shuttle ride, always chat me up.')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    # Cancels and ends the conversation.
    user = update.message.from_user
    logger.info("User %s %s %s canceled the conversation.", user.first_name, user.first_name, user.last_name)
    update.message.reply_text(
        "You're blessed! If you need any assistance for shuttle ride, always chat me up.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, DESTINATION, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Student|Non-Student|Pilot)$'), gender)],
            DESTINATION: [MessageHandler(Filters.regex('^(EIE|CST|Others)$'), destination)],
            #   PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
