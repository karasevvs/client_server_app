import locale
import sys
# таск_6
print('Задание 6')

default_encoding = locale.getpreferredencoding()
print(f"Стандартная кодировка: {default_encoding}, для ос: {sys.platform}")
print()

words = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w', encoding='utf-8') as file:
    for word in words:
        file.write(f"{word}\n")

with open('test_file.txt', encoding='utf-8') as file:
    for f_str in file:
        print(f_str)
