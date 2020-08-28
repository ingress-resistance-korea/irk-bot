from uuid import uuid4


def get_intel_screenshot(queue, update, context):
    location_name = ' '.join(context.args)
    message = update['message']
    from_user = message['from_user']
    chat_data = {
        'date': str(message['date']),
        'chat_id': message['chat_id'],
        'from_user': {
            'username': from_user['username'],
            'language_code': from_user['language_code'],
            'id': from_user['id'],
            'first_name': from_user['first_name'],
            'last_name': from_user['last_name'],
            'is_bot': from_user['is_bot'],
        }
    }
    queue.request_intel(event_id=str(uuid4()), client_type='telegram', location_name=location_name, chat_data=chat_data)
    update.message.reply_markdown('잠시만 기다려주세요')
