from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
import os # Импорт модуля для работы с ОС
from django.core.files import File # Для работы с файлами в Django
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import NewsPicture, News  # Импорт моделей таблиц БД из siteapp

# Здесь будет код для получения данных со страниц News____.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        files = [f for f in os.listdir(site_dir) # Получаем список имён файлов в site_dir
                 if os.path.isfile(os.path.join(site_dir, f)) # Проверяем, является ли элемент файлом, а также
                 and f.lower().startswith('news') # начинается ли имя файла с "news" (независимо от регистра)
                 and f.lower().endswith('.html')] # заканчивается ли имя файла на ".html"
        for file in files: # Перебираем все файлы с новостями
            with open(os.path.join(site_dir, file), 'r', encoding='utf-8') as f: # Открываем для чтения каждый html-файл
                content = f.read() # Читаем содержимое файла с кодом
                soup = BeautifulSoup(content, 'html.parser') # Парсим исходный HTML-код
                articles = soup.find_all('article') # Извлекаем все article-теги
                for article in articles: # Итерируем по каждому найденному тегу <article>
                    date = article.time['datetime']  # Преобразуем строку в дату
                    title = article.h3.text # Получаем название события

                    p_lst = article.find_all('p') # Извлекаем все p-теги в виде списка объектов
                    text = '' # Создаём переменную для текста
                    link_found = False # Флаг для проверки наличия ссылки
                    for p in p_lst: # Итерируем по каждому p-тегу
                        a = p.find('a', href=True) # Ищем тег <a> внутри текущего p-тега с атрибутом href
                        if a: # Если найден тег <a>
                            file_name = os.path.splitext(os.path.basename(a['href']))[0] # Извлекаем имя файла без расширения
                            text += p.decode_contents().replace(f"{file_name}.html", # Заменяем ссылку "___.html" вида
                                                   f"/{file_name}") + '\n' # на динамическую ссылку
                            link_found = True # Если ссылка найдена
                    if not link_found: # Если ссылки не найдено
                        text = '\n'.join([p.decode_contents() for p in p_lst]) # Просто записываем текст

                    label_lst = article.find_all('label') # Извлекаем все label-теги
                    picture_objs = [] # Список для хранения объектов картинок
                    for label in label_lst: # Перебираем все label-теги
                        src = label.img['src'].split('/') # то извлекаем ссылку к изображению в src (имя файла)
                        alt = label.img['alt'] if label.img['alt'] else '' # и альт-описание картинки
                        with open(os.path.join(site_dir, *src), 'rb') as img_file: # Открываем для чтения изображения
                            picture_obj, _ = NewsPicture.objects.get_or_create( # Создаём объект NewsPicture
                                src=File(img_file, name=src[-1]), # с сохранением ссылки в поле src
                                alt=alt) # и альт-описания
                            picture_objs.append(picture_obj) # Добавляем объект в список

                    news_obj, _ = News.objects.get_or_create( # Создаём объект News
                        title=title, # Сохраняем название
                        date=date, # Сохраняем дату
                        text=text) # Сохраняем текст
                    news_obj.img.set(picture_objs)  # Связываем все картинки с новостью