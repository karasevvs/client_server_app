"""Программа-клиент"""

import sys
import json
import socket
import time
from lesson_5.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT
from lesson_5.common.utils import get_message, send_message
import argparse
import lesson_5.errors_user as errors_user
import logging

LOG_MAIN = logging.getLogger('client')


def create_presence_msg(port=DEFAULT_PORT, acc_name='Vadim'):
    """
    Функция генерирует запрос о присутствии клиента
    :param acc_name: логин (имя аккауната)
    :param port: порт клиента
    :return: сообщение-запрос о присутствии клиента (словарь)
    """
    message_output = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: acc_name
        }
    }
    return message_output


def server_process_answer(message_server):
    """
    Функция разбирает ответ сервера
    :param server_message: ответ сервера
    :return: код ответа сервера (строка)
    """
    if RESPONSE in message_server:
        if message_server[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message_server[ERROR]}'
    raise ValueError


def client_main():
    """
    Загружаем параметы коммандной строки
    """

    for_parse = argparse.ArgumentParser()
    for_parse.add_argument('port', nargs='?', type=int, default=DEFAULT_PORT)
    for_parse.add_argument('address', nargs='?', type=str, default=DEFAULT_IP_ADDRESS)

    args_parse = for_parse.parse_args()

    try:
        server_port = args_parse.port
        server_address = args_parse.address
        if not (1024 < server_port < 65535):
            raise errors_user.PortError
    except errors_user.PortError as port_error:
        LOG_MAIN.critical(f'Ошибка порта {args_parse.server_port}: {port_error}')
        sys.exit(1)

    # Инициализация сокета и обмен

    trans_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trans_port.connect((server_address, server_port))
    message_to_server = create_presence_msg(server_port)
    send_message(trans_port, message_to_server)
    LOG_MAIN.info(f'Сообщение отправлено {message_to_server[ACTION]} '
             f'от пользователя {message_to_server[USER][ACCOUNT_NAME]} '
             f'для сервера {server_address}')
    try:
        answer = server_process_answer(get_message(trans_port))
        print(f"Ответ => {answer}")
    except json.JSONDecodeError:
        LOG_MAIN.error(f'Не удалось декодировать сообщение сервера: {server_address}')
    except errors_user.IncorrectDataRecivedError as incorrect_data:
        LOG_MAIN.error(f'Принято некорректное сообщение от удалённого компьютера. {server_address}: {incorrect_data}')



if __name__ == '__main__':
    client_main()
