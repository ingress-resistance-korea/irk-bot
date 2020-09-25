import telegram
from telegram import Update


def get_data(update: Update):
    message: telegram.Message = update.effective_message
    message = message.to_dict()
    from_user: telegram.User = update.effective_user
    from_user = from_user.to_dict()
    chat: telegram.Chat = update.effective_chat
    chat = chat.to_dict()
    data = {
        'telegram_chat': chat,
        'telegram_message': message,
        'telegram_user': from_user,
    }
    return data
