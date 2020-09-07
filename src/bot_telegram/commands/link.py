from telegram import Update
from telegram.ext import CallbackContext

from src.bot_telegram.constantcs import LINK_HELP_MESSAGE_TELEGRAM
from src.shared.utils.calc_link_distance import calculate_link_distance


def get_link_distance(update: Update, callback: CallbackContext):
    args = callback.args
    if not len(args):
        result = LINK_HELP_MESSAGE_TELEGRAM
    elif len(args) == 1:
        result = calculate_link_distance(args[0])
    else:
        result = calculate_link_distance(args[0], args[1])
    update.message.reply_markdown(result)

