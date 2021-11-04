"""Программа-сервер"""

import socket
import sys
import json
from lesson_5.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from lesson_5.common.utils import get_message, send_message
import argparse
import logging
import lesson_5.logs.server_logs_config

LOG_MAIN = logging.getLogger('server')


def process_client_msg(client_message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param client_message: сообщение от клиента в виде словаря
    :return: ответ сервера в виде словаря
    """
    if ACTION in client_message and client_message[ACTION] == PRESENCE and TIME in client_message \
            and USER in client_message and client_message[USER][ACCOUNT_NAME] == 'Vadim':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def server_main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    """
    print('Сервер старт ...')
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    arg_parser.add_argument('-a', type=str, default='')

    args = arg_parser.parse_args()

    # Загружаем порт для прослушки

    try:
        listen_port = args.p
        if not (1024 < listen_port < 65535):
            raise ValueError
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        LOG_MAIN.critical(f'Ошибка порта {args.listen_port}: {args.error}. Соединение закрывается.')
        sys.exit(1)

    # Загружаем адрес для прослушки

    address_listen = args.a

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((address_listen, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)
    LOG_MAIN.info(f'Запущен сервер. Порт подключений: {listen_port}, адрес прослушивания: {address_listen}')

    while True:
        client, client_address = transport.accept()
        LOG_MAIN.info(f'Установлено соединение с клиентом {client_address}')
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            LOG_MAIN.debug(f'Получено сообщение {message_from_client} от клиента {client_address}')
            response = process_client_msg(message_from_client)
            send_message(client, response)
            LOG_MAIN.info(f'Отправлено сообщение {response} клиенту {client_address}')
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            LOG_MAIN.error(f'Не удалось декодировать сообщение клиента {client_address}.')
            client.close()


if __name__ == '__main__':
    server_main()