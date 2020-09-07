from uuid import uuid4

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from src.bot_telegram.utils import get_data
from src.shared.constants import INTEL_RESPONSE_TELEGRAM, INTEL_HELP_MESSAGE
from src.shared.queue import BotQueue


def get_intel_screenshot(queue: BotQueue, update: Update, context: CallbackContext):
    location = ' '.join(context.args)

    # send help information
    if not len(location):
        update.message.reply_markdown(INTEL_HELP_MESSAGE)
        return

    data = get_data(update)
    queue.send_request_intel(event_id=str(uuid4()), response_event_to=INTEL_RESPONSE_TELEGRAM, location=location,
                             data=data)
    update.message.reply_markdown('잠시만 기다려주세요')


def get_intel_screenshot_by_position(queue: BotQueue, update: Update, context: CallbackContext):
    message = update.message
    latitude, longitude = (message.location.latitude, message.location.longitude)
    data = get_data(update)
    queue.send_request_intel_by_position(event_id=str(uuid4()), response_event_to=INTEL_RESPONSE_TELEGRAM,
                                         latitude=latitude, longitude=longitude, data=data)
    update.message.reply_markdown('잠시만 기다려주세요')
