from typing import Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from config import SETTINGS, logger, END_CONDITION


@logger.catch()
def button(update: Update, context: CallbackContext) -> Any:
    query = update.callback_query
    data = query.data

    try:
        board = SETTINGS[data]['keyboard']

        if len(board) == 1 and isinstance(board, list):
            data = board[0]
            board = SETTINGS[data]['keyboard']

        if 'end' in SETTINGS[data].keys():
            END_CONDITION[query.from_user.id] = data

        if isinstance(board, list):
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(SETTINGS[key]['title'], callback_data=key)]
                                             for key in board])
        else:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(key, callback_data=value)]
                                             for key, value in board.items()])

        query.edit_message_text(text=SETTINGS[data]['title'], reply_markup=keyboard)
    except KeyError:
        query.edit_message_text(text=SETTINGS[data]['title'])

        if 48 > int(data[1:]) > 16:
            return 'feedback'
        else:
            return -1


# updater.dispatcher.add_handler(CallbackQueryHandler(button))
