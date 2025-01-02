import os # Для работы с OC
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import HistoryData, History # Импорт моделей таблиц БД HistoryData, History из siteapp

# Здесь будет код для получения данных со страницы Article.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(site_dir, 'About.html'), 'r', encoding='utf-8') as f: # Открываем для чтения нужный файл
            content = f.read() # Читаем содержимое файла с кодом
            soup = BeautifulSoup(content, 'html.parser') # Парсим исходный HTML-код
            articles = soup.find_all('article')[2:] # Находим все теги <article> (пропускаем первые 2)
            for article in articles: # Итерируем по каждому найденному тегу <article>
                year = article.find('h3').get_text()[:4] # Извлекаем год из заголовка <h3>
                day_month = article.find('b').get_text() if article.find('b') else None # Извлекаем дату из тега <b>, если он существует
                data = HistoryData.objects.create(year=year, day_month=day_month) # Создаем объект HistoryData с годом и датой
                texts = [text.get_text() for text in article.find_all('p')]  # Извлекаем текст из каждого абзаца <p>
                labels = article.find_all('label')  # Находим все теги <label> с изображением
                imgs = [] # Инициируем пустой список с адресом изображения
                alts = [] # Инициируем пустой список с альт-названием изображения
                for label in labels: # Итерируем по каждому тегу <label>
                    imgs.append(label.find('img').get('src')) # Извлекаем путь к изображению из тега <img> и добавляем в список
                    alts.append(label.find('img').get('alt')) # Извлекаем текст альт-описания изображения и добавляем в список
                if len(labels) == 0: # Если <labels> нет в <article>
                    imgs = [''] # То список будет из пустого элемента
                    alts = [''] # То список будет из пустого элемента
                for text, img, alt in zip(texts, imgs, alts): # Итерируем по каждому тексту из абзацев
                    History.objects.create(text=text, # Создаем объект с таблицей History с текстом
                                           img=img, # Добавляем путь к изображению
                                           alt=alt, # Добавляем альт-текст изображения
                                           data=data) # Связываем с объектом HistoryData