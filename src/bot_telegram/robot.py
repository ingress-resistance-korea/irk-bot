import time
from typing import Type

import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from src.bot_telegram.commands.intel import get_intel_screenshot
from src.bot_telegram.commands.help import get_documents
from src.bot_telegram.commands.irk import get_irk_community_guide
from src.shared.constants import INTEL_RESPONSE_TELEGRAM

from src.shared.logger import getLogger
from src.configs.settings import TELEGRAM_TOKEN
from src.shared.queue import BotQueue
from src.shared.types import IntelResult


class Robot(object):
    def __init__(self):
        self.logger = getLogger('bot-telegram')
        self.queue = BotQueue()
        self.client = telegram.Bot(TELEGRAM_TOKEN)
        self.updater = Updater(TELEGRAM_TOKEN, use_context=True)

    def run(self):
        start_handler = CommandHandler('start', self.help_command)
        self.updater.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help_command)
        self.updater.dispatcher.add_handler(help_handler)

        intel_handler = CommandHandler('intel', self.intel_command)
        self.updater.dispatcher.add_handler(intel_handler)

        link_handler = CommandHandler('link', self.not_supported_command)
        self.updater.dispatcher.add_handler(link_handler)

        irk_comm_handler = CommandHandler('irk', self.irk_comm_command)
        self.updater.dispatcher.add_handler(irk_comm_handler)

        subscribe_handler = CommandHandler('subscribe', self.not_supported_command)
        self.updater.dispatcher.add_handler(subscribe_handler)

        message_handler = MessageHandler(Filters.text, self.get_message)
        self.updater.dispatcher.add_handler(message_handler)

        self.updater.start_polling(timeout=1)
        while True:
            self.receive_events()
            time.sleep(0.3)

    # message reply function
    @staticmethod
    def get_message(bot, update: Update):
        if str(update.message.text).startswith('/'):
            update.message.reply_text("지원하지 않는 명령어입니다.")
        else:
            update.message.reply_text("답장 기능이 제공되지 않습니다.")

    # commands
    def intel_command(self, update: Update, context: CallbackContext):
        get_intel_screenshot(self.queue, update, context)

    def irk_comm_command(self, update: Update, _: CallbackContext):
        get_irk_community_guide(self.queue, update)

    def help_command(self, update: Update, _: CallbackContext):
        get_documents(self.queue, update)

    @staticmethod
    def not_supported_command(update: Update, context: CallbackContext):
        update.message.reply_text("준비중인 기능입니다.")

    def receive_events(self):
        response = self.queue.receive_response_intel(INTEL_RESPONSE_TELEGRAM)
        if response:
            self.send_intel_response(response)
        pass

    def send_intel_response(self, response):
        chat_id = response['chat']['id']
        result = self._parse_result(response['result'])
        if not result.success:
            self.client.send_message(chat_id=chat_id, text=result.error_message)
        text = '%s\n`%s`\n%s' % (result.address, result.timestamp, result.url)
        self.client.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def _parse_result(result: dict) -> Type[IntelResult]:
        parsed_result = IntelResult

        parsed_result.success = result['success']
        parsed_result.url = result['url']
        parsed_result.address = result['address']
        parsed_result.error_message = result['error_message']
        parsed_result.timestamp = result['timestamp']
        return parsed_result

