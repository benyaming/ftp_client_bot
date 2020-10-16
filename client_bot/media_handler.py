import os

from telebot import TeleBot

from client_bot import db


class MediaHandler(object):

    def __init__(self, user_id: int, fn: str, caption: str = None,
                 media_type: str = 'photo'):
        self._user_id = user_id
        self._fn = fn
        self._client_name = db.get_client_name(self._user_id)
        self._caption = caption
        self._media_type = media_type

    def handle_media(self):
        token = db.get_client_bot_token(self._user_id)
        admin_bot = TeleBot(token)
        operators = db.get_operators(self._user_id)
        if self._caption:
            caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._client_name}</b>'

        actions = {
            'document': admin_bot.send_document,
            'photo': admin_bot.send_photo,
            'voice': admin_bot.send_voice
        }
        send_media = actions.get(self._media_type)

        with open(self._fn, 'rb') as media:
            for operator in operators:
                send_media(operator, media, caption=caption, parse_mode='HTML')
                media.seek(0)
        os.remove(self._fn)
