from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import Document  # Импорт моделей таблицы БД из siteapp
from datetime import datetime

# Здесь будет код для получения данных со страницы Docs.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{site_dir}Docs.html', 'r', encoding='utf-8') as f: # Открываем для чтения html-файл
            content = f.read() # Читаем содержимое файла с кодом
            soup = BeautifulSoup(content, 'html.parser') # Парсим исходный HTML-код
            trs = soup.find_all('tr')[1:] # Извлекаем все tr-теги, кроме первого
            time = [tr.find('td', class_='time').get_text(strip=True) if tr.find('td', class_='time') else '' for tr in trs] # Извлекаем даты
            data_before = datetime.strptime(time[0], "%d-%m-%Y").date() # Дата публикации документа берётся первая
            for n, tr in enumerate(trs): # Итерируем по каждому найденному тегу <tr>
                date = datetime.strptime(time[n], "%d-%m-%Y").date() # Извлекаем дату
                name = tr.find('td', class_='left').get_text(strip=True)  # Извлекаем название (второй столбец)
                url = tr.find('a').get('href')  # Извлекаем ссылку (третий столбец)
                if not date: # Если дата публикации пустая
                    Document.objects.get_or_create(name=name, # Название документа
                                            date=data_before,  # Дата публикации документа берётся предыдущий
                                            url=url) # Ссылка его скачивания
                else:
                    Document.objects.get_or_create(name=name,  # Название документа
                                                   date=date,  # Дата публикации документа берётся предыдущий
                                                   url=url)  # Ссылка его скачивания
                    data_before = date  # Дата публикации документа берётся следующий