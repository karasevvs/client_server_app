"""Программа-клиент"""

import sys
import json
import socket
import time
from lesson_7.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT, MESSAGE, MESSAGE_TEXT, SENDER
from lesson_7.common.utils import get_message, send_message
import argparse
import lesson_7.errors_user as errors_user
import logging
from lesson_7.decos import Log

LOG_MAIN = logging.getLogger('client')
CLIENT_MODE = {
    'send': 'sending messages',
    'listen': 'receiving messages'
}


@Log(LOG_MAIN)
def create_presence_msg(message=None, action=PRESENCE, port=DEFAULT_PORT, acc_name='Vadim'):
    """
    Функция генерирует запрос о присутствии клиента
    :param message: текст сообщения
    :param action: тип передаваемого сообщения
    :param acc_name: логин (имя аккауната)
    :param port: порт клиента
    :return: сообщение-запрос о присутствии клиента (словарь)
    """
    message_output = {
        ACTION: action,
        TIME: time.time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: acc_name
        }
    }
    if message and action == MESSAGE:
        message_output[MESSAGE_TEXT] = message
    return message_output


@Log(LOG_MAIN)
def input_message(client_socket):
    """
    Функция для ввода сообщения пользователем
    :param client_socket: объект сокета клиента
    :return: сообщение (строка)
    """
    while True:
        message = input('Введите сообщение для отправки (для выхода введите exit):')
        if message.strip():
            break
        else:
            print('Сообщение не может быть пустым!')
    if message == 'exit':
        client_socket.close()
        exit(0)
    return message


@Log(LOG_MAIN)
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
    raise errors_user.NoResponseInServerMessageError


@Log(MESSAGE_TEXT)
def message_from_server(server_message):
    """
    Функция - обработчик сообщений других пользователей, поступающих с сервера
    :param server_message: сообщение от сервера
    """
    if ACTION in server_message and server_message[ACTION] == MESSAGE and SENDER in server_message \
            and MESSAGE_TEXT in server_message:
        print(f'Получено сообщение от пользователя {server_message[SENDER]}:\n{server_message[MESSAGE_TEXT]}')
        LOG_MAIN.info(f'Получено сообщение от пользователя {server_message[SENDER]}:\n{server_message[MESSAGE_TEXT]}')
    else:
        LOG_MAIN.error(f'Получено некорректное сообщение с сервера: {server_message}')


@Log(LOG_MAIN)
def mainloop(client_mode, transport, server_address, server_port):
    """
    Функция основной петли отправки-получения сообщений
    :param client_mode: режим клиента
    :param transport: сокет
    :param server_address: адрес сервера
    :param server_port: порт сервера
    """
    print(f'Режим работы - {CLIENT_MODE[client_mode]}')
    while True:
        try:
            if client_mode == 'send':
                message = create_presence_msg(MESSAGE, input_message(transport), server_port)
                send_message(transport, message)
                LOG_MAIN.info(f'Отправлено сообщение {message[MESSAGE_TEXT]} '
                              f'от пользователя {message[USER][ACCOUNT_NAME]}')
            elif client_mode == 'listen':
                message_from_server(get_message(transport))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            LOG_MAIN.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)


def client_main():
    """
    Загружаем параметы коммандной строки
    """

    for_parse = argparse.ArgumentParser()
    for_parse.add_argument('port', nargs='?', type=int, default=DEFAULT_PORT)
    for_parse.add_argument('address', nargs='?', type=str, default=DEFAULT_IP_ADDRESS)
    for_parse.add_argument('-m', '--mode', type=str, default='send')

    args_parse = for_parse.parse_args()

    server_port = args_parse.port
    server_address = args_parse.address
    client_mode = args_parse.mode

    try:
        if not (1024 < server_port < 65535):
            raise errors_user.PortError
        if client_mode not in CLIENT_MODE:
            raise errors_user.ClientModeError
    except errors_user.PortError as port_error:
        LOG_MAIN.critical(f'Ошибка порта {args_parse.server_port}: {port_error}. Завершение соединения...')
        sys.exit(1)
    except errors_user.ClientModeError as error:
        LOG_MAIN.critical(f'Ошибка режима {server_port}: {error}. Завершение соединения...')
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
    except errors_user.NoResponseInServerMessageError as error:
        LOG_MAIN.error(f'Ошибка сообщения сервера {server_address}: {error}')
    except ConnectionRefusedError:
        LOG_MAIN.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}')
        sys.exit(1)
    else:
        mainloop(client_mode, trans_port, server_address, server_port)

if __name__ == '__main__':
    client_main()
