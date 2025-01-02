import os # Для работы с OC
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import TrendItem, Trend # Импорт моделей из siteapp

# Здесь будет код для получения направлений деятельности со страницы index.html

class Command(BaseCommand):
    def handle(self, *args, **options):

        with open(os.path.join(site_dir, 'index.html'),
                  'r', encoding='utf-8') as f:  # Открываем для чтения нужный файл
            content = f.read()  # Читаем содержимое файла c кодом
            soup = BeautifulSoup(content, 'html.parser')  # Парсим исходный HTML-код
            pages = soup.find('section', class_='areas')  # Блок с пунктами направлений
            all_a = pages.find_all('a')  # Находим все теги <a>
            trends = sorted(list(set(a.get('id') for a in all_a)))  # Собираем все осн. направления деятельности

            trends_dict = {}  # Создаем пустой словарь
            for trend in trends:  # Проходим по каждому осн. направлению деятельности
                trend_obj, _ = Trend.objects.get_or_create(name=trend)  # Добавляем уникальное осн. направление в БД
                trends_dict[trend] = trend_obj  # Собираем словарь с именем осн. направления деятельности и их объектом

            for a in all_a:  # Проходим по каждому тегу <a>
                name = a.find('strong').get_text()  # Получаем текст c направлением деятельности в теге <strong>
                trend = a.get('id')  # Получаем id основного направления деятельности
                trend_obj = trends_dict[trend]  # Получаем объект Trend из словаря, чтобы потом вставить в Progress
                TrendItem.objects.get_or_create(name=name, # Направление деятельности
                                         trend=trend_obj) # Основное направление деятельности (из Trend, один-ко-многим)