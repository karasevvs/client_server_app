# таск_4
print('Задание 4')
print()
words = ["разработка", "администрирование", "protocol", "standard"]

for word in words:
    print(f'оригинал: {word}')
    x = word.encode('utf-8')
    print(f'encode: {x}')
    print(f"decode: {x.decode('utf-8')}")
    print()
