import urllib3

from telebot import TeleBot

import db


class MediaHandler(object):

    def __init__(self, user_id: int, link: str, caption: str = None,
                 media_type: str = 'photo'):
        self._user_id = user_id
        self._link = link
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

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', self._link)
        media = resp.data

        actions = {
            'document': admin_bot.send_document,
            'photo': admin_bot.send_photo,
            'voice': admin_bot.send_voice
        }
        send_media = actions.get(self._media_type)

        for operator in operators:
            send_media(operator, media, caption=caption, parse_mode='HTML')
        resp.release_conn()
