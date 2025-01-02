from django.core.management.base import BaseCommand # Импорт базового класса команды Django
import os # Загружаем модуль os

class Command(BaseCommand):
    help = 'Запускает все команды'

    def handle(self, *args, **kwargs):  # Переопределяем метод handle
        self.all_run()  # Вызываем функцию all_run()

    def all_run(self):  # Создаем функцию запуска всех своих команд
        commands = [
            'article', # Статьи
            'culture', # Культуры
            'doc', # Документы
            'history', # История
            'news', # Новости
            'page', # Страницы
            'progress', # Достижения
            'reference', # Полезные ссылки
            'trenditem', # Направления деятельности
            'price', # Прайс-лист
        ]
        for command in commands:  # Перебираем все команды
            os.system(f'python manage.py {command}')  # Запускаем каждую команду
            print(f'Команда {command} выполнена') # Сообщение о выполнении команды

if __name__ == '__main__':  # Если это файл с именем __main__, то запускаем функцию all_run()
    Command().all_run()  # Запускаем функцию all_run()