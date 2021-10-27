import subprocess

# таск_5
print('Задание 5')
source_1 = ['ping', 'yandex.ru']

ping_source_1 = subprocess.Popen(source_1, stdout=subprocess.PIPE)
for line in ping_source_1.stdout:
    print(line.decode('cp866').encode('utf-8').decode('utf-8'))

source_2 = ['ping', 'youtube.com']

ping_source_2 = subprocess.Popen(source_2, stdout=subprocess.PIPE)
for line in ping_source_2.stdout:
    print(line.decode('cp866').encode('utf-8').decode('utf-8'))


# ping_source_1 = subprocess.call(source_1)