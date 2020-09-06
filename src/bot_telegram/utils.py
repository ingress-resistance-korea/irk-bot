import telegram


def get_data(update):
    message: telegram.Message = update.effective_message
    message = message.to_dict()
    from_user: telegram.User = update.effective_user
    from_user = from_user.to_dict()
    chat: telegram.Chat = update.effective_chat
    chat = chat.to_dict()
    data = {
        'chat': chat,
        'message': message,
        'user': from_user,
    }
    return data
