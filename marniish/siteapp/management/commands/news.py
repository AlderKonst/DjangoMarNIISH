from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
import os # Импорт модуля для работы с ОС
from django.core.files import File # Для работы с файлами в Django
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import NewsPicture, NewsBlock, News  # Импорт моделей таблиц БД из siteapp

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
                    news_obj, _ = News.objects.get_or_create(  # Создаём объект News
                        title=title, # То, что в h3 (титульник)
                        date=date) # Дата события
                    order = 0 # Порядок для блоков, пока нуль
                    for element in article.section.children: # Перебираем все дочерние элементы в <section>
                        if element.name == 'label': # Если встретился тэг <label>
                            src = element.img['src'].split('/') # то извлекаем ссылку к изображению в src (имя файла)
                            alt = element.img['alt'] if element.img['alt'] else '' # и альт-описание картинки
                            with open(os.path.join(site_dir, *src), 'rb') as img_file: # Открываем для чтения изображения
                                picture_obj, _ = NewsPicture.objects.get_or_create( # Создаём объект NewsPicture
                                    src=File(img_file, name=src[-1]), # с сохранением ссылки в поле src
                                    alt=alt) # и альт-описания
                                NewsBlock.objects.create( # Создаём объект NewsBlock для изображения
                                    content_type='image', # Устанавливаем тип контента как изображение
                                    news=news_obj, # Привязываем новость к блоку
                                    img=picture_obj, # Привязываем созданное изображение
                                    order=order) # Устанавливаем порядок блока
                                order += 1 # Увеличиваем порядок для следующего блока
                        elif element.name == 'p': # Если встретился тэг <p> или <a>
                            text = element.decode_contents().replace("Docs.html", f"{{% url 'siteapp:Docs' %}}") # Заменяем "Docs.html" на динамическую ссылку
                            NewsBlock.objects.create( # Создание объекта NewsBlock для текста
                                content_type='text', # Устанавливаем тип контента как текст
                                news=news_obj, # Привязываем новость к блоку
                                text=text, # Привязываем текст к блоку
                                order=order) # Устанавливаем порядок блока
                            order += 1 # Увеличиваем порядок для следующего блока