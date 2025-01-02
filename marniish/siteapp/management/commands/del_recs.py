import os # Для работы с файлами
import shutil # Для копирования файлов
from django.conf import settings # Импорт конфигурации проекта
from django.core.management.base import BaseCommand  # Импорт базового класса команды Django
from siteapp.models import (  # Импортируем все необходимые модели из приложения siteapp
    Trend, Article, Progress, Page, TrendItem, Reference, HistoryData, History,
    CultureGroup, Culture, Taxon, Document, ProdCategory, Price, NewsPicture, News
)

# Решение этой задачи сильно подсказала нейросеть:
class Command(BaseCommand):  # Определяем новый класс команды
    help = 'Удаляет записи из указанных таблиц или из всех таблиц и очищает папку /media/'  # Описание команды

    def add_arguments(self, parser):  # Метод для добавления аргументов командной строки
        parser.add_argument(  # Добавляем аргумент для передачи имен моделей
            'model_names',  # Имя аргумента
            nargs='*',  # Позволяет передавать несколько значений (или ничего)
            help='Список моделей для удаления записей. Если не указаны, удаляются записи из всех моделей.'  # Описание аргумента
        )

    def handle(self, *args, **options):  # Основной метод обработки команды
        model_names = options['model_names']  # Получаем список имен моделей из аргументов

        model_mapping = {  # Словарь сопоставления имен команд и моделей
            'trend': Trend,  # 'trend' -> Trend
            'article': Article,  # 'article' -> Article
            'progress': Progress,  # 'progress' -> Progress
            'page': Page,  # 'page' -> Page
            'trenditem': TrendItem,  # 'trenditem' -> TrendItem
            'reference': Reference,  # 'reference' -> Reference
            'historydata': HistoryData,  # 'historydata' -> HistoryData
            'history': History,  # 'history' -> History
            'culturegroup': CultureGroup,  # 'culturegroup' -> CultureGroup
            'culture': Culture,  # 'culture' -> Culture
            'taxon': Taxon,  # 'taxon' -> Taxon
            'document': Document,  # 'document' -> Document
            'prodcategory': ProdCategory,  # 'prodcategory' -> ProdCategory
            'price': Price,  # 'price' -> Price
            'newspicture': NewsPicture,  # 'newspicture' -> NewsPicture
            'news': News,  # 'news' -> News
        }

        def clear_media_folder(): # Для очистки папки /media/
            media_root = settings.MEDIA_ROOT # Путь к папке /media/
            for root, dirs, files in os.walk(media_root): # Цикл по папке /media/
                for f in files:  # Цикл по файлам
                    os.unlink(os.path.join(root, f)) # Удаляем файл
                for d in dirs: # Цикл по директориям
                    shutil.rmtree(os.path.join(root, d)) # Удаляем директорию

        if not model_names:  # Если список имен моделей пустой (не переданы аргументы)
            for model in model_mapping.values():  # Перебираем все модели в словаре
                deleted_count, _ = model.objects.all().delete()  # Удаляем все записи из текущей модели и получаем количество удалённых записей
                self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} записей из {model.__name__}'))  # Выводим сообщение об успешном удалении
                clear_media_folder() # Очищаем папку /media/ созданной функцией выше
                self.stdout.write(self.style.SUCCESS('Папка /media/ очищена')) # Выводим сообщение об успешном удалении

        else:  # Если переданы имена моделей для удаления
            for name in model_names:  # Перебираем переданные имена моделей
                model = model_mapping.get(name.lower())  # Получаем класс модели по переданному имени (в нижнем регистре)
                if model:  # Если модель найдена в словаре
                    deleted_count, _ = model.objects.all().delete()  # Удаляем все записи из найденной модели и получаем количество удалённых записей
                    self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} записей из {model.__name__}'))  # Выводим сообщение об успешном удалении
                else:  # Если модель не распознана (не найдена в словаре)
                    self.stdout.write(self.style.WARNING(f'Модель "{name}" не распознана'))  # Выводим предупреждение о том, что модель не распознана