import time

import telegram
from telegram import Update, ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from src.bot_telegram.commands.intel import get_intel_screenshot, get_intel_screenshot_by_position
from src.bot_telegram.commands.help import get_documents
from src.bot_telegram.commands.irk import get_irk_community_guide
from src.bot_telegram.commands.link import get_link_distance
from src.bot_telegram.utils import get_data
from src.shared.constants import INTEL_RESPONSE_TELEGRAM

from src.shared.logger import getLogger, LogstashLogger
from src.configs.settings import TELEGRAM_TOKEN
from src.shared.parser import parse_intel_result
from src.shared.queue import BotQueue


class Robot(object):
    def __init__(self):
        self.logger = getLogger('bot-telegram')
        self.queue = BotQueue()
        self.client = telegram.Bot(TELEGRAM_TOKEN)
        self.updater = Updater(TELEGRAM_TOKEN, use_context=True)
        self.logstash = LogstashLogger('telegram')

    def run(self):
        start_handler = CommandHandler('start', self.help_command)
        self.updater.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help_command)
        self.updater.dispatcher.add_handler(help_handler)

        intel_short_handler = CommandHandler('i', self.intel_command)
        self.updater.dispatcher.add_handler(intel_short_handler)

        intel_handler = CommandHandler('intel', self.intel_command)
        self.updater.dispatcher.add_handler(intel_handler)

        link_handler = CommandHandler('link', self.link_command)
        self.updater.dispatcher.add_handler(link_handler)

        link_short_handler = CommandHandler('l', self.link_command)
        self.updater.dispatcher.add_handler(link_short_handler)

        irk_comm_handler = CommandHandler('irk', self.irk_comm_command)
        self.updater.dispatcher.add_handler(irk_comm_handler)

        subscribe_handler = CommandHandler('subscribe', self.not_supported_command)
        self.updater.dispatcher.add_handler(subscribe_handler)

        location_handler = MessageHandler(Filters.location, self.get_location)
        self.updater.dispatcher.add_handler(location_handler)

        message_handler = MessageHandler(Filters.text, self.get_message)
        self.updater.dispatcher.add_handler(message_handler)

        self.updater.start_polling()
        while True:
            self.receive_events()
            time.sleep(0.3)

    # message reply function
    def get_message(self, update: Update, callback: CallbackContext):
        self.logstash.irk_chat(get_data(update))

    def get_location(self, update: Update, context: CallbackContext):
        self.logstash.irk_request(get_data(update))
        get_intel_screenshot_by_position(self.queue, update, context)

    # commands
    def intel_command(self, update: Update, context: CallbackContext):
        self.logstash.irk_request(get_data(update))
        get_intel_screenshot(self.queue, update, context)

    def irk_comm_command(self, update: Update, _: CallbackContext):
        self.logstash.irk_request(get_data(update))
        get_irk_community_guide(self.queue, update)

    def help_command(self, update: Update, _: CallbackContext):
        self.logstash.irk_request(get_data(update))
        get_documents(self.queue, update)

    def link_command(self, update: Update, context: CallbackContext):
        self.logstash.irk_request(get_data(update))
        get_link_distance(update, context)

    def not_supported_command(self, update: Update, context: CallbackContext):
        self.logstash.irk_request(get_data(update))
        update.message.reply_text("준비중인 기능입니다.")

    def receive_events(self):
        response = self.queue.receive_response_intel(INTEL_RESPONSE_TELEGRAM)
        if response:
            self.logstash.irk_response(response)
            self.send_intel_response(response)
        pass

    def send_intel_response(self, response):
        chat_id = response['extra']['telegram_chat']['id']
        message_id = response['extra']['telegram_message']['message_id']
        result = parse_intel_result(response['result'])
        if result.success:
            text = '%s\n`%s`\n%s' % (result.address, result.timestamp, result.intel_url)
            file = open(result.file_path, 'rb')
            self.client.send_photo(chat_id=chat_id, photo=file, caption=text, reply_to_message_id=message_id ,parse_mode=ParseMode.MARKDOWN)
            file.close()
        else:
            self.client.send_message(chat_id=chat_id, reply_to_message_id=message_id, text=result.error_message)
