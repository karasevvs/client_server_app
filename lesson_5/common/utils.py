"""Утилиты"""

import json
from lesson_5.common.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(socket):
    """
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param socket: объект сокета
    :return: словарь
    """

    response_encoded = socket.recv(MAX_PACKAGE_LENGTH)
    if isinstance(response_encoded, bytes):
        response_json = response_encoded.decode(ENCODING)
        response = json.loads(response_json)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(socket, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param socket: объект сокета
    :param message: сообщение в виде словаря
    :return: None
    """

    message_json = json.dumps(message)
    message_encoded = message_json.encode(ENCODING)
    socket.send(message_encoded)
