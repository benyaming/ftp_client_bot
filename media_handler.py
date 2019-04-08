import urllib3

from telebot import TeleBot

import db


# class PhotoHandler(object):
#
#     def __init__(self, user_id: int, link: str, caption: str):
#         self._user_id = user_id
#         self._link = link
#         self._client_name = db.get_client_name(self._user_id)
#         self._caption = caption
#
#     def handle_photo(self):
#         self._forward_photo_to_admin()
#
#     def _forward_photo_to_admin(self):
#         token = db.get_client_bot_token(self._user_id)
#         admin_bot = TeleBot(token)
#         operators = db.get_operators(self._user_id)
#         if self._caption:
#             caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._client_name}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         resp = connection_pool.request('GET', self._link)
#
#         for operator in operators:
#             admin_bot.send_photo(operator, resp.data, caption,
#                                  parse_mode='HTML')
#         resp.release_conn()
#
#
# class DocumentHandler(object):
#
#     def __init__(self, user_id: int, link: str, caption: str = None):
#         self._user_id = user_id
#         self._link = link
#         self._client_name = db.get_client_name(self._user_id)
#         self._caption = caption
#
#     def handle_document(self):
#         self._forward_document_to_admin()
#
#     def handle_voice(self):
#         self._forward_voice_to_admin()
#
#     def _forward_document_to_admin(self):
#         token = db.get_client_bot_token(self._user_id)
#         admin_bot = TeleBot(token)
#         operators = db.get_operators(self._user_id)
#         if self._caption:
#             caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._client_name}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         resp = connection_pool.request('GET', self._link)
#
#         for operator in operators:
#             admin_bot.send_document(operator, resp.data, caption=caption,
#                                     parse_mode='HTML')
#         resp.release_conn()
#
#     def _forward_voice_to_admin(self):
#         token = db.get_client_bot_token(self._user_id)
#         admin_bot = TeleBot(token)
#         operators = db.get_operators(self._user_id)
#         caption = f'<b>{self._client_name}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         resp = connection_pool.request('GET', self._link)
#
#         for operator in operators:
#             admin_bot.send_voice(operator, resp.data, caption, parse_mode='HTML',)
#         resp.release_conn()


class MediaHandler(object):

    def __init__(self, user_id: int, link: str, caption: str = None):
        self._user_id = user_id
        self._link = link
        self._client_name = db.get_client_name(self._user_id)
        self._caption = caption

    def handle_media(self, media_type: str = 'photo'):
        token = db.get_client_bot_token(self._user_id)
        admin_bot = TeleBot(token)
        operators = db.get_operators(self._user_id)
        if self._caption:
            caption = f'<b>{self._client_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._client_name}</b>'

        connection_pool = urllib3.PoolManager()
        media = connection_pool.request('GET', self._link).data

        actions = {
            'docunemt': admin_bot.send_document,
            'photo': admin_bot.send_photo,
            'voice': admin_bot.send_voice
        }
        send_media = actions.get(media_type)

        for operator in operators:
            send_media(operator, media, caption=caption, parse_mode='HTML')
        media.release_conn()
