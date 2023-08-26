import json

import telebot

from settings import tg_token, tg_users_filepath

bot = telebot.TeleBot(tg_token, threaded=False)


def get_users():
    users = []
    try:
        with open(tg_users_filepath) as f:
            str_users = f.read()
            if str_users:
                users = json.loads(str_users)
    except FileNotFoundError:
        with open(tg_users_filepath, 'w'):
            pass
    return users


def save_users(users):
    with open(tg_users_filepath, 'w') as f:
        json.dump(users, f)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.chat.username

    users = get_users()

    if chat_id not in users:
        users.append(chat_id)
        save_users(users)
        msg = "Уведомления о предстоящих боях будут приходить за пару минут до начала"
    else:
        msg = "Уведомления уже включены"

    bot.send_message(chat_id, msg)


def send_message_to_all_users(msg):
    users = get_users()
    for chat_id in users.copy():
        try:
            bot.send_message(chat_id, msg)
        except telebot.apihelper.ApiTelegramException:
            users.remove(chat_id)
            save_users(users)


# bot.polling()
