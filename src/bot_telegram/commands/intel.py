from uuid import uuid4

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from src.bot_telegram.constantcs import INTEL_HELP_MESSAGE_TELEGRAM
from src.bot_telegram.utils import get_data
from src.shared.constants import INTEL_RESPONSE_TELEGRAM
from src.shared.queue import BotQueue


def get_intel_screenshot(queue: BotQueue, update: Update, context: CallbackContext):
    location = ' '.join(context.args)

    # send help information
    if not len(location):
        update.message.reply_markdown(INTEL_HELP_MESSAGE_TELEGRAM)
        return

    bot_message = update.message.reply_markdown('잠시만 기다려주세요')
    extra = get_data(update)
    extra['telegram_bot_message_id'] = bot_message.message_id
    queue.send_request_intel(event_id=str(uuid4()), response_event_to=INTEL_RESPONSE_TELEGRAM, location=location,
                             extra=extra)


def get_intel_screenshot_by_position(queue: BotQueue, update: Update, context: CallbackContext):
    message = update.message
    latitude, longitude = (message.location.latitude, message.location.longitude)
    bot_message = update.message.reply_markdown('잠시만 기다려주세요')
    extra = get_data(update)
    extra['telegram_bot_message_id'] = bot_message.message_id
    queue.send_request_intel_by_position(event_id=str(uuid4()), response_event_to=INTEL_RESPONSE_TELEGRAM,
                                         latitude=latitude, longitude=longitude, extra=extra)
