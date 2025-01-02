import os # Для работы с OC
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import Article, Trend # Импорт моделей Article и Trend из siteapp
import re # Пришлось для работы с регулярными выражениями

# Здесь будет код для получения данных со страницы Article.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(site_dir, 'Article.html'),
                  'r', encoding='utf-8') as f:  # Открываем для чтения нужный файл
            content = f.read()  # Читаем содержимое файла c кодом
            soup = BeautifulSoup(content, 'html.parser')  # Парсим исходный HTML-код
            pages = soup.find('div', class_='pages')  # Самая динамичная часть кода страницы
            lis = pages.find_all('li')  # Находим все теги <li>
            trends = sorted(list(set(li.find('span').get('class')[0] for li in lis)))  # Собираем все направления деятельности

            trends_dict = {}  # Создаем пустой словарь
            for trend in trends:  # Проходим по каждому направлению деятельности
                trend_obj, _ = Trend.objects.get_or_create(name=trend)  # Добавляем уникальное направление в БД
                trends_dict[trend] = trend_obj  # Собираем словарь с именем направления деятельности и их объектом

            for li in lis:  # Проходим по каждому тегу <li>
                article = li.get_text()  # Получаем текст cо статьёй в теге <li>
                article = re.sub(r'DOI:.*|URL:.*', '', article) # Удаляем текст внутри <p> без с 'DOI:' или 'URL:'
                trend = li.find('span').get('class')[0]  # Получаем из <span> название направления деятельности, заложенный в атрибуте class
                year = li.find('span').get('title')  # Получаем из <span> название года, заложенный в атрибуте title
                p = li.find('p')  # Получаем из <p> текст, заложенный в атрибуте class
                doi = ''  # Инициируем DOI пустым
                link = ''  # Инициируем URL пустым
                if p:
                    doi_match = re.search(r'DOI: (.*)', p.text)
                    link_match = re.search(r'URL: (.*)', p.text)
                    doi = doi_match.group(1) if doi_match else ''
                    link = link_match.group(1) if link_match else ''
                else: # Если же нет и DOI, и URL
                    doi = '' # Получаем пустое значение
                    link = '' # Получаем пустое значение
                trend_obj = trends_dict[trend]  # Получаем объект Trend из словаря, чтобы потом вставить в Article
                Article.objects.create(name=article,  # Достижение
                                       year=year,  # Год
                                       doi=doi, # DOI
                                       link=link, # URL
                                       trend=trend_obj)  # Направление деятельности (из Trend, один-ко-многим)