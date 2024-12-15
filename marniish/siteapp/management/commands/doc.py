import os # Для работы с OC
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.files import File # Для работы с файлами в Django
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir, date_transform # Импортируем переменную с директорией сайта и функцию преобразования даты
from siteapp.models import Document  # Импорт моделей таблицы БД из siteapp

# Здесь будет код для получения данных со страницы Docs.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(site_dir, 'Docs.html'), 'r', encoding='utf-8') as f: # Открываем для чтения html-файл
            content = f.read() # Читаем содержимое файла с кодом
            soup = BeautifulSoup(content, 'html.parser') # Парсим исходный HTML-код
            trs = soup.find_all('tr')[1:] # Извлекаем все tr-теги, кроме первого
            time = [tr.find('td', class_='time').get_text(strip=True) if tr.find('td', class_='time') else '' for tr in trs] # Извлекаем даты
            data_before = date_transform(time, 0) # Преобразуем дату
            for n, tr in enumerate(trs): # Итерируем по каждому найденному тегу <tr>
                date = '' # Инициируем пустую переменную для дат
                if time[n]: # Если есть данные
                    date = date_transform(time, n) # Преобразуем дату
                name = tr.find('td', class_='left').get_text(strip=True)  # Извлекаем название (второй столбец)
                url = tr.find('a').get('href').split('/') # Извлекаем ссылку (третий столбец)
                file_path = os.path.join(site_dir, *url)
                if not os.path.exists(file_path):
                    self.stdout.write(self.style.WARNING(f'Файл {file_path} не найден!'))
                    continue
                with open(file_path, 'rb') as doc:
                    if not date: # Если дата публикации ксивы пустая
                        Document.objects.get_or_create(name=name, # Название документа
                                                date=data_before,  # Дата публикации документа берётся предыдущий
                                                url=File(doc, name=url[-1])) # Ссылка его скачивания с сохранением в /media/
                    else:
                        Document.objects.get_or_create(name=name,  # Название документа
                                                       date=date,  # Дата публикации документа берётся предыдущий
                                                       url=File(doc, name=url[-1])) # Ссылка его скачивания с сохранением в /media/
                        data_before = date  # Дата публикации документа берётся следующий