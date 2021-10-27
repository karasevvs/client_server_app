import chardet
import re
import csv


def get_data():
    """
    1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
    из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
        a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и
         считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения
         параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра
         поместить в соответствующий список. Должно получиться четыре списка —
         например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для
         хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка:
         «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов
         также оформить в виде списка и поместить в файл main_data (также для каждого файла);

        b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
        В этой функции реализовать получение данных через вызов функции get_data(), а
        также сохранение подготовленных данных в соответствующий CSV-файл;

        c. Проверить работу программы через вызов функции write_to_csv().
    :return: подготовленный список для записи
    """
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(1, 4):
        with open(f'info_{i}.txt', 'rb') as file:
            file_read = file.read()
            result = chardet.detect(file_read)
            data = file_read.decode(result['encoding'])

        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])

        os_name_reg = re.compile(r'Название ОС:\s*\S*')
        os_name_list.append(os_name_reg.findall(data)[0].split()[2])

        os_code_reg = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(os_code_reg.findall(data)[0].split()[2])

        os_type_reg = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type_reg.findall(data)[0].split()[2])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)
    data_for_rows = [os_prod_list, os_name_list, os_code_list, os_type_list]

    for i in range(len(data_for_rows[0])):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


def write_to_csv(file_patch):
    """
    Функция для записи данных в csv
    :param file_patch:  название файла
    :return: None
    """
    main_data = get_data()
    with open(file_patch, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in main_data:
            writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('my.csv')
