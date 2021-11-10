"""Программа-сервер"""

import socket
import sys
import json
from lesson_7.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE, MESSAGE_TEXT, MESSAGE, PORT
from lesson_7.common.utils import get_message, send_message
import argparse
import logging
import lesson_7.errors_user as errors_user
from lesson_7.decos import Log
import select
from collections import deque

LOG_MAIN = logging.getLogger('server')


@Log(LOG_MAIN)
def process_client_msg(client_message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param client_message: сообщение от клиента в виде словаря
    :param messages_list: список сообщений для отправки
    :param client: сокет клиента
    """
    if ACTION in client_message and TIME in client_message and USER in client_message and PORT in client_message:
        if client_message[ACTION] == PRESENCE and client_message[USER][ACCOUNT_NAME] == 'Vadim':
            send_message(client, {RESPONSE: 200})
            return
        if client_message[ACTION] == MESSAGE and MESSAGE_TEXT in client_message:
            messages_list.append((client_message[USER][ACCOUNT_NAME], client_message[MESSAGE_TEXT]))
            return
    send_message(client,
                 {
                     RESPONSE: 400,
                     ERROR: 'Bad Request'
                 })
    return


def server_main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    arg_parser.add_argument('-a', type=str, default='')

    args = arg_parser.parse_args()

    # Загружаем порт для прослушки

    try:
        listen_port = args.p
        if not (1024 < listen_port < 65535):
            raise errors_user.PortError
    except errors_user.PortError as port_error:
        LOG_MAIN.critical(f'Ошибка порта {args.listen_port}: {port_error}. Соединение закрывается.')
        sys.exit(1)

    # Загружаем адрес для прослушки

    address_listen = args.a

    # список клиентов и очередь сообщений:
    clients_list = []
    messages_deque = deque()

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((address_listen, listen_port))
    transport.settimeout(1)

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)
    LOG_MAIN.info(f'Запущен сервер. Порт подключений: {listen_port}, адрес прослушивания: {address_listen}')

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOG_MAIN.info(f'Установлено соедение с клиентом {client_address}')
            clients_list.append(client)

        receive_data_list = []
        send_data_list = []
        errors_list = []

        try:
            if clients_list:
                receive_data_list, send_data_list, errors_list = select.select(clients_list, clients_list, [], 0)
        except OSError:
            pass

        for client_with_message in receive_data_list:
            try:
                process_client_msg(get_message(client_with_message), messages_deque, client_with_message)
            except Exception:
                LOG_MAIN.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                clients_list.remove(client_with_message)

        if messages_deque and send_data_list:
            message_data = messages_deque.popleft()
            message = {
                ACTION: MESSAGE,
                SENDER: message_data[0],
                TIME: time.time(),
                MESSAGE_TEXT: message_data[1]
            }

            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except Exception:
                    LOG_MAIN.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients_list.remove(waiting_client)


if __name__ == '__main__':
    server_main()
