import psycopg2

from client_bot.settings import db_parameters_string


def check_auth(client_id: int) -> bool:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT exists (SELECT 1 FROM clients ' \
                '               WHERE tg_id = %s LIMIT 1);'
        cur.execute(query, (client_id,))
        return cur.fetchone()[0]


def get_client_name(client_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT client_name FROM clients ' \
                'WHERE tg_id = %s'
        cur.execute(query, (client_id,))
        return cur.fetchone()[0]


def get_operator_type(client_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT worker FROM clients ' \
                'WHERE tg_id = %s'
        cur.execute(query, (client_id,))
        return cur.fetchone()[0]


def get_operators(client_id: int) -> list:
    with psycopg2.connect(db_parameters_string) as conn:
        operator_type = get_operator_type(client_id)
        cur = conn.cursor()
        query = 'SELECT tg_id FROM operators ' \
                'WHERE op_type = %s'
        cur.execute(query, (operator_type,))
        operators = [int(i[0]) for i in cur.fetchall()]
        return operators


def get_client_bot_token(user_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT bot_token FROM clients ' \
                'WHERE tg_id = %s'
        cur.execute(query, (user_id,))
        token = cur.fetchone()[0]
        return token
