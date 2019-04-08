from json import dumps

import telebot
from telebot.types import Message
from flask import request, Flask

import db
import settings
import text_handler
import document_handler


WEBHOOK_HOST = settings.BOT_HOST
WEBHOOK_PORT = settings.BOT_PORT
ssl_cert = '/hdd/certs/webhook_cert.pem'
ssl_cert_key = '/hdd/certs/webhook_pkey.pem'
base_url = f'{WEBHOOK_HOST}:{WEBHOOK_PORT}'
route_path = f'/{settings.URI}/'

bot = telebot.TeleBot(settings.USER_BOT_TOKEN)

app = Flask(__name__)


@app.route(route_path, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok'


def report(message: Message):
    report_bot = telebot.TeleBot(settings.REPORT_BOT_TOKEN)
    formatted_message = dumps(message.json, indent=2)
    report_msg = f'<b>Попытка доступа в клиентский бот!</b>\n\n<code>' \
                 f'{formatted_message}</code>'
    report_bot.send_message(5979588, report_msg, parse_mode='HTML')


def check_auth(func):
    def wrapper(message):
        if db.check_auth(message.from_user.id):
            return func(message)
        else:
            response = '`Доступ запрещен. Обратитесь к администратору`'
            bot.send_message(message.from_user.id, response,
                             parse_mode='Markdown')
            report(message)
    return wrapper


@bot.message_handler(commands=['start'])
@check_auth
def handle_start(message):
    bot.send_message(
        message.from_user.id,
        'Welcome!'
    )


@bot.message_handler(func=lambda message: True, content_types=['text'])
@check_auth
def handle_text_message(message: Message):
    text_handler.TextHandler(message).handle_text()


@bot.message_handler(func=lambda message: True, content_types=['photo'])
@check_auth
def handle_text_message(message: Message):
    file_id = message.photo[-1].file_id
    link = f'https://api.telegram.org/file/bot{settings.USER_BOT_TOKEN}/' \
           f'{bot.get_file(file_id).file_path}'
    caption = message.caption
    document_handler.PhotoHandler(message.from_user.id, link,
                                  caption).handle_photo()


@bot.message_handler(func=lambda message: True, content_types=['document'])
@check_auth
def handle_text_message(message: Message):
    file_id = message.document.file_id
    link = f'https://api.telegram.org/file/bot{settings.USER_BOT_TOKEN}/' \
           f'{bot.get_file(file_id).file_path}'
    caption = message.caption
    document_handler.DocumentHandler(message.from_user.id, link,
                                     caption).handle_document()


@bot.message_handler(func=lambda message: True, content_types=['voice'])
@check_auth
def handle_voice_message(message: Message):
    file_id = message.voice.file_id
    link = f'https://api.telegram.org/file/bot{settings.USER_BOT_TOKEN}/' \
           f'{bot.get_file(file_id).file_path}'
    document_handler.DocumentHandler(message.from_user.id, link).handle_voice()


ignoring_types = ['sticker', 'audio', 'video', 'video_note', 'location', 'contact', '']


@bot.message_handler(func=lambda message: True, content_types=ignoring_types)
@check_auth
def handle_text_message(message: Message):
    response = '<code>Бот не поддерживает отправку сообщений такого ' \
               'типа. Пожалуйста, отправьте текст, фото или документ.</code>'
    bot.send_message(message.from_user.id, response, parse_mode='HTML')


if __name__ == '__main__':
    if settings.IS_SERVER:
        bot.remove_webhook()
        bot.set_webhook(
            url=f'{base_url}{route_path}',
            certificate=open(ssl_cert, 'r')
        )

    else:
        bot.remove_webhook()
        bot.polling(True, timeout=50)
