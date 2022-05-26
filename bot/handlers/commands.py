from datetime import datetime
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, \
    Filters
import requests

from bot.handlers.callbacks import button
from bot.config import updater, SETTINGS, logger, END_CONDITION, PHOTO_PATH
from web_api.db_api.db import session, FeedBacks


@logger.catch()
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(SETTINGS['start'], parse_mode='HTML')


@logger.catch()
def help_command(update: Update, context: CallbackContext) -> None:
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(SETTINGS[key]['title'], callback_data=key)]
                                     for key in SETTINGS['A2']['keyboard']])

    update.message.reply_text(SETTINGS['A2']['title'], reply_markup=keyboard)


@logger.catch()
def download_file(link: str) -> Any:
    file_name = str(datetime.now())
    photo = requests.get(link)

    try:
        with open(f'{PHOTO_PATH}{file_name}.jpg', 'wb') as file:
            file.write(photo.content)
            return file_name
    except Exception as error:
        logger.error(error)
        return False


@logger.catch()
def feedback(update: Update, context: CallbackContext) -> Any:
    username = update.message.from_user.username
    tg_id = update.message.from_user.id
    caption = update.message.caption

    try:
        if len(update.message.photo):
            photo_link = context.bot.getFile(update.message.photo[-1].file_id).file_path
            photo = download_file(photo_link)
            if not photo:
                raise FileNotFoundError

            record = FeedBacks(
                tg_id=tg_id,
                username='None' if username is None else username,
                feedback='' if caption is None else caption,
                end=END_CONDITION[tg_id],
                photo=photo
            )
        else:
            record = FeedBacks(
                tg_id=tg_id,
                username='None' if username is None else username,
                feedback=update.message.text,
                end=END_CONDITION[tg_id]
            )
    except KeyError as error:
        logger.error(error)
        return update.message.reply_text(SETTINGS['error'])

    try:
        session.add(record)
        session.commit()
    except Exception as error:
        logger.error(error)
        return update.message.reply_text(SETTINGS['error'])

    END_CONDITION.pop(tg_id)
    update.message.reply_text(SETTINGS['success'])
    return -1


conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button)],
    states={
        'feedback': [MessageHandler(Filters.text, feedback),
                     MessageHandler(Filters.photo, feedback)]
    },
    fallbacks=[]
)
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
