from telebot import TeleBot
from telebot.types import Message

import db


class TextHandler(object):

    def __init__(self, message: Message):
        self._user_id = message.from_user.id
        self._text = message.text
        self._client_name = db.get_client_name(self._user_id)

    def handle_text(self):
        self._forward_message_to_admin()

    def _forward_message_to_admin(self):
        token = db.get_client_bot_token(self._user_id)
        admin_bot = TeleBot(token)
        operators = db.get_operators(self._user_id)
        response = f'<b>{self._client_name}</b>\n\n{self._text}'
        for operator in operators:
            admin_bot.send_message(
                operator,
                response,
                parse_mode='HTML'
             )
