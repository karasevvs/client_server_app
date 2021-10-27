import yaml
from random import randint


def task_3(file_name):
    """
    Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
    Для этого:
    a. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
    третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим
    в кодировке ASCII (например, €);
    b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
    с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
    c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
    :param file_name: наименование файла для сохранения.
    :return: None
    """

    for_write = {
        'список': [f'элемент_{item}' for item in range(1, 6)],
        'целое число': 777,
        'вложенный словарь': {
            key: f'элемент_{randint(1, 5)}' for key in ([1, 2, 3, 4, 5])
        },
    }
    with open(file_name, 'w', encoding='UTF-8') as file:
        yaml.dump(for_write, file, default_flow_style=False, allow_unicode=True)

    with open(file_name, encoding='UTF-8') as file:
        for_read = yaml.load(file, yaml.Loader)

    print('Сверка данных => ', for_write == for_read)


if __name__ == '__main__':
    task_3('my_yaml_.yaml')
