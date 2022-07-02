#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to handle '(my_)chat_member' updates.
Greets new users & keeps track of which chats the bot is in.

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

and

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.


Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

"""

import logging
from typing import Tuple, Optional

from telegram import (Update, Chat, ChatMember, ParseMode, ChatMemberUpdated,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
    ChatMemberHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)




def extract_status_change(
        chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
            old_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
            new_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member


def track_chats(update: Update, context: CallbackContext) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s started the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    else:
        if not was_member and is_member:
            logger.info("%s added the bot to the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


def show_chats(update: Update, context: CallbackContext) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    update.effective_message.reply_text(text)


def greet_chat_members(update: Update, context: CallbackContext) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        update.effective_chat.send_message(
            f"{member_name} was added by {cause_name}. Welcome!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        update.effective_chat.send_message(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
            parse_mode=ParseMode.HTML,
        )


"""""
Begining of code 2
"""""


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
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5244306869:AAFrJqdmrIpAbKx_HuSWBlhhYVsJEeIuShI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # for code 2 it starts here
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
    # for code 2, it ends here

    # Keep track of which chats the bot is in
    dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the Bot
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
