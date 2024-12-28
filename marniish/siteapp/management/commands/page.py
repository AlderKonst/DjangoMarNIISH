import os # Импорт модуля для работы с ОС
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга HTML
from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from . import site_dir # Импортируем переменную с директорией сайта
from siteapp.models import Page # Импорт модели таблицы БД Page из siteapp

# Здесь будет код для получения данных со всех страниц сайта марниисх.рф и добавления новых из pages_lists

pages_lists = [ # Создаем список для хранения страниц редактирования и добавляем в него данные в БД
    ['Редактирование направлений деятельности', # title
     'Trend_editing', # url
     'Редактирование на странице основных направлений деятельности на сайте Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока', # description
     'Trend', # parent_url
     'Направления деятельности'], # parent_title
    ['Изменение направлений деятельности', # title
     'Trend_edit', # url
     'Изменение направления деятельности на странице основных направлений деятельности сайта Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока', # description
     'Trend_editing', # parent_url
     'Редактирование', # parent_title
     'Trend', # pre_parent_url
     'Направления деятельности'], # pre_parent_title
    ['Удаление направлений деятельности', # Далее аналогично
     'Trend_confirm_delete',
     'Подтверждение удаления направления деятельности на странице основных направлений деятельности сайта Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока',
     'Trend_editing',
     'Редактирование',
     'Trend',
     'Направления деятельности'],
    ['Редактирование документов',
     'Docs_editing',
     'Редактирование на странице документов на сайте Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока',
     'Docs',
     'Документы'],
    ['Изменение документа',
     'Docs_edit',
     'Изменение документа на странице документов сайта Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока',
     'Docs_editing',
     'Редактирование',
     'Docs',
     'Документы'],
    ['Удаление документа',
     'Docs_confirm_delete',
     'Подтверждение удаления документа на странице документов сайта Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока',
     'Docs_editing',
     'Редактирование',
     'Docs',
     'Документы'],
    ['Редактирование истории',
     'About_editing',
     'Редактирование истории на странице историии института на сайте Марийского НИИСХ, филиала ФБГНУ ФАНЦ Северо-Востока',
     'About',
     'История института'],
        ]

class Command(BaseCommand):
    def handle(self, *args, **options):
        pages = [page for page in os.listdir(site_dir)
                 if page.endswith('.html')] # Перебираем страницы и сохраняем в генереторе имена файлов с .html в конце
        for page in pages:
            with open(os.path.join(site_dir, page), 'r', encoding='utf-8') as f:  # Прочитываем каждый html-файл
                content = f.read()  # Читаем содержимое файла c кодом
                soup = BeautifulSoup(content, 'html.parser')  # Парсим исходный HTML-код
                title = soup.find('title').get_text()[:-72] # Получаем уникальную часть текста титульника
                description = soup.select_one('meta[name="description"]')['content'] # Получаем описание страницы
                parent_block = soup.find('li', class_ = 'parent') # Получаем блок, указывающий на родительскую страницу
                parent_url = '' # Инициируем адрес родительской страницы пустым
                parent_title = '' # Инициируем имя родительской страницы пустым
                if parent_block: # Если блок родительской страницы есть
                    parent_url = parent_block.find('a').get('href') # Получаем адрес родительской страницы
                    parent_title = parent_block.find('a').get_text() # Получаем имя родительской страницы

                def format_url(url): # В страницах новостей убирает .html и форматирует в таком виде: News/ГГГГ
                    url = url[:-5] # Убираем .html из имени файла
                    if url.startswith('News'): # Если адрес начинается с News
                        year = url[4:] # Извлекаем год из имени страницы
                        return year # Форматируем URL как ГГГГ
                    else: # Если адрес не начинается с News (остальные)
                        return url # Возвращаем адрес страницы без .html

                url = format_url(page) # Убираем .html и News из имени текущей страницы с таким (ГГГГ) форматом
                parent_url = format_url(parent_url) # Убираем .html и News из адреса родительской страницы с таким (ГГГГ) форматом
                Page.objects.get_or_create( # Создаем объект таблицы БД Page
                    title=title,  # Создаем поле именем страницы
                    url = url, # Создаем поле адреса текущей страницы без расширения
                    description = description, # Создаем поле описания страницы
                    parent_url = parent_url, # Создаем поле адреса родительской страницы без расширения
                    parent_title = parent_title, # Создаем поле имени родительской страницы
                    pre_parent_url= '', # Создаем пустое поле адреса прародительской страницы без расширения
                    pre_parent_title='') # Создаем пустое поле имени прародительской страницы без расширения

        # Добавление новых страниц из pages_lists
        for pages_list in pages_lists: # Перебираем список категорий качества зерна
            Page.objects.get_or_create( # Создаем запись таблицы БД Page
                title=pages_list[0], # с полем именем страницы
                url=pages_list[1], # с полем адреса текущей страницы без расширения
                description=pages_list[2], # с полем описания страницы
                parent_url=pages_list[3], # с полем адреса родительской страницы без расширения
                parent_title=pages_list[4], # с полем имени родительской страницы
                pre_parent_url=pages_list[5] if len(pages_list) > 5 else '', # с полем адреса прародительской страницы без расширения
                pre_parent_title=pages_list[6] if len(pages_list) > 5 else '') # с полем имени прародительской страницы