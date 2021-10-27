import json


def write_order_to_json(filepath, **kwargs):
    """
    a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
    цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных
    в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;

    b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
    каждого параметра.
    :param filepath: путь к файлу
    :param kwargs: информация по заказу, параметры используются при записи в файл.
    :return: None
    """
    with open(filepath, encoding='UTF-8') as json_file:
        data = json.load(json_file)

    data['orders'].append(kwargs)

    with open(filepath, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    for_write = [
        {'item': 'Apple MacBook Pro 13',
         'quantity': 1,
         'price': 161490.00,
         'buyer': 'Карасев Вадим',
         'date': '23-10-2021'},
    ]

    for order in for_write:
        write_order_to_json('orders.json', **order)
