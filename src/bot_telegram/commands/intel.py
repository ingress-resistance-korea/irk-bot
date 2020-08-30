from uuid import uuid4

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from src.shared.constants import INTEL_RESPONSE_TELEGRAM
from src.shared.queue import BotQueue


def get_intel_screenshot(queue: BotQueue, update: Update, context: CallbackContext):
    location = ' '.join(context.args)
    message: telegram.Message = update.effective_message
    message = message.to_dict()
    from_user: telegram.User = update.effective_user
    from_user = from_user.to_dict()
    chat: telegram.Chat = update.effective_chat
    chat = chat.to_dict()
    queue.send_request_intel(event_id=str(uuid4()), response_event_to=INTEL_RESPONSE_TELEGRAM, location=location, chat=chat, message=message, user=from_user)
    update.message.reply_markdown('잠시만 기다려주세요')
