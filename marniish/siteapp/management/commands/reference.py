import os # Для работы с OC
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
import cssutils # Импорт библиотеки для парсинга CSS
import logging # Импорт библиотеки для логирования
from . import site_dir # Импортируем переменную с директорией сайта
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from siteapp.models import Reference # Импорт модели таблицы БД References из siteapp

# Здесь будет код для получения свойств полезных ссылок из index.html и style.css

class Command(BaseCommand):
    def handle(self, *args, **options):
        dir_html = os.path.join(site_dir, 'index.html') # Директория c index.html
        dir_css = os.path.join(site_dir, 'css', 'style.css') # Директория c style.css

        with open(dir_html, 'r', encoding='utf-8') as f:  # Прочитываем html-файл
            content = f.read()  # Читаем содержимое файла c кодом
        soup = BeautifulSoup(content, 'html.parser')  # Парсим исходный HTML-код
        div_refs = soup.find('div', class_='references')  # Получаем блок со ссылками
        refs = div_refs.find_all('a')  # Получаем все тэги со ссылками

        cssutils.log.setLevel(logging.CRITICAL) # Устанавливаем максимальный уровень логирования на критический
        with open(dir_css, 'r', encoding='utf-8') as f:  # Прочитываем css-файл
            content = f.read()  # Читаем содержимое файла c кодом
        css_parser = cssutils.CSSParser(raiseExceptions=False)  # Инициализируем парсер
        css_styles = css_parser.parseString(content)  # Парсим исходный CSS-код

        for rule in css_styles: # Перебираем все правила
            if rule.type == rule.STYLE_RULE: # Если правило является стилем
                selector = rule.selectorText.strip() # Получаем селектор
                for ref in refs:  # Перебираем все ссылки
                    title = ref.get('title')  # Получаем заголовок ссылки
                    id_name = ref.get('id')  # Получаем id ссылки
                    url = ref.get('href')  # Получаем url ссылки
                    top = '' # Создаём пустое значение top
                    left = '' # Cоздаём пустое значение left
                    if f'#{id_name} img' in selector: # Если есть ссылка на изображение
                        top = rule.style.getPropertyValue('top') # Получаем значение top
                        left = rule.style.getPropertyValue('left') # Получаем значение left
                        Reference.objects.get_or_create(name=title, # Заголовок ссылки
                                                 id_name=id_name, # id ссылки
                                                 url=url, # адрес ссылки
                                                 top=top, # Значение top спрайта в CSS
                                                 left=left) # Значение left спрайта в CSS