import urllib3

from telebot import TeleBot

import db


class PhotoHandler(object):

    def __init__(self, user_id: int, link: str, caption: str):
        self._user_id = user_id
        self._link = link
        self._client_name = db.get_client_name(self._user_id)
        self._caption = caption

    def handle_photo(self):
        self._forward_photo_to_admin()

    def _forward_photo_to_admin(self):
        token = db.get_client_bot_token(self._user_id)
        admin_bot = TeleBot(token)
        operators = db.get_operators(self._user_id)
        if self._caption:
            caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._client_name}</b>'

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', self._link)

        for operator in operators:
            admin_bot.send_photo(operator, resp.data, caption,
                                 parse_mode='HTML')
        resp.release_conn()


class DocumentHandler(object):

    def __init__(self, user_id: int, link: str, caption: str):
        self._user_id = user_id
        self._link = link
        self._client_name = db.get_client_name(self._user_id)
        self._caption = caption

    def handle_document(self):
        self._forward_document_to_admin()

    def _forward_document_to_admin(self):
        token = db.get_client_bot_token(self._user_id)
        admin_bot = TeleBot(token)
        operators = db.get_operators(self._user_id)
        if self._caption:
            caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._client_name}</b>'

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', self._link)

        for operator in operators:
            admin_bot.send_document(operator, resp.data, caption=caption,
                                    parse_mode='HTML')
        resp.release_conn()
