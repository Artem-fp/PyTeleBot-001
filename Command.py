import os
import argparse

parser = argparse.ArgumentParser(description='Попытка в консоль')
parser.add_argument('-n', '--name', nargs='?', default='Аноним', help="Вот твоё имя")
parser.add_argument('-p', '--path', help="Держи путь к файлу")
parser.add_argument('-nQ', '--noQ', action="store_true", help="Ничем не могу помочь, друг")
args = parser.parse_args()
print(f'Привет, {args.name}!')
print(args)

if os._exists(args.path):
    if args.noQ:
        os.remove(args.path)
        exit(0)
    else:
        ag = input(f'\n{args.name}, ты хочешь удалить файл? ').capitalize()
        if ag[0] == 'Y':
            os.remove(args.path)
        else:
            print('Хорошо, я жду следующей команды')
else:
    print("\nПрости, но этого файла нет")