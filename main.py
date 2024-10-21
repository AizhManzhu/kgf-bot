import json
import logging
import urllib3
import telebot
import md5util
from datetime import datetime
from os import getenv

logsPath = getenv('LOGS_PATH', 'logs')
# token = getenv('TELEGRAM_TOKEN')
# domain = getenv('DOMAIN')
token = '7253504314:AAELtP09h-QxzZB12nKNo3a8qHTEf4TYvhk'
domain = 'http://127.0.0.1:8000/api'
logger = telebot.logger
logging.basicConfig(filename=logsPath + '/{:%Y-%m-%d}.log'.format(datetime.now()), level=logging.WARN,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(token, parse_mode='html')
main_menu_text = "На главную"


@bot.message_handler(commands=['start'])
def welcome(message_data):
    vip_member_id = 0
    vip_hash = ''
    utm = ''
    result = message_data.text.split(" ")
    if len(result) > 1:
        data = result[1].split("-")
        if data:
            if len(data) > 1:
                vip_member_id = data[0]
                vip_hash = data[0]+data[1]
            else:
                utm = data
        else:
            utm = result[1]
    else:
        utm = ''
    http = urllib3.PoolManager()
    encoded_body = json.dumps({
        'hash': hash_darling(message_data.chat.id),
        'telegram_id': message_data.chat.id,
        # 'utm': utm,
        'vip_member_id': vip_member_id,
        'vip_hash': vip_hash,
        'date': message_data.date
    })
    result = http.request('POST', domain + '/start',
                          headers={'Content-Type': 'application/json'},
                          body=encoded_body)
    if result.status == 404:
        logger.log(msg=result.data, level=logging.WARN)
        bot.send_message(chat_id=message_data.chat.id, text='Oops... Bot is unavailable:(')


@bot.message_handler(content_types=['text'])
def message(message_data):
    http = urllib3.PoolManager()
    encoded_body = json.dumps({
        'hash': hash_darling(message_data.chat.id),
        'telegram_id': message_data.chat.id,
        'message': message_data.text,
        'date': message_data.date
    })
    result = http.request('POST', domain + '/v1/message',
                          headers={'Content-Type': 'application/json'},
                          body=encoded_body)
    if result.status != 200:
        logger.setLevel(logging.WARN)
        logger.log(msg=result.data, level=logging.WARN)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    http = urllib3.PoolManager()
    encoded_body = json.dumps({
        'hash': hash_darling(call.message.chat.id),
        'telegram_id': call.message.chat.id,
        'callback': call.data,
        'message_id': call.message.id,
    })
    result = http.request('POST', domain + '/save-callback',
                          headers={'Content-Type': 'application/json'},
                          body=encoded_body)
    if result.status == 404:
        logger.setLevel(logging.WARN)
        logger.log(msg=result.data, level=logging.WARN)


def find_member(message_data):
    http = urllib3.PoolManager()
    encoded_body = json.dumps({
        'hash': hash_darling(message_data.chat.id),
        'telegram_id': message_data.chat.id,
        'name': message_data.text
    })
    result = http.request('POST', domain + '/get-member',
                          headers={'Content-Type': 'application/json'},
                          body=encoded_body)
    if result.status == 404:
        logger.setLevel(logging.WARN)
        logger.log(msg=result.data, level=logging.WARN)


def hash_darling(telegram_id):
    return md5util.Md5Util.get_data_md5({"token": token, "slash": '/', "chat_id": telegram_id},
                                        ["chat_id", 'slash', "token"])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
