"""
Конфигурация URL для проекта блога.

Список urlpatterns перенаправляет URL-адреса на представления. Для получения дополнительной информации см.:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
Примеры:
Функциональные представления
1. Добавьте импорт: from my_app import views
2. Добавьте URL в urlpatterns: path('', views.home, name='home')
Классовые представления
1. Добавьте импорт: from other_app.views import Home
2. Добавьте URL в urlpatterns: path('', Home.as_view(), name='home')
Включение другой URLconf
1. Импортируйте функцию include(): from django.urls import include, path
2. Добавьте URL в urlpatterns: path('blog/', include('blog.urls'))
"""

from django.urls import path # Импортируем функцию для определения URL-маршрутов
from siteapp import views # Импортируем представления из приложения siteapp
from django.conf import settings # Импортируем настройки Django
from django.conf.urls.static import static # Импортируем функцию для работы со статическими файлами

app_name = 'siteapp' # Задаем имя приложения для использования в пространстве имен

news_years = range(2016, 2025) # Список годов для новостей с 2016 по 2024 гг.
# Как в занятии path('News/<int:year>/', views.news, name='News') почему-то никак не получалось, нашёл такой способ ниже
urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    *[path(f'News/{year}/', views.news, name=f'News{year}', kwargs={'year': year}) for year in news_years], # Добавляем пути для новостей за каждый год
    path('Prod/', views.prod, name='Prod'), # Продукция
    path('Grain/', views.grain, name='Grain'), # Зерновые
    path('Potato/', views.potato, name='Potato'), # Картофель
    path('Grass/', views.grass, name='Grass'), # Многолетние травы
    path('Jim/', views.jim, name='Jim'), # Жимолость
    path('About/', views.about, name='About'), # История института
    path('Trend/', views.trend, name='Trend'), # Направления деятельности
    path('Progress/', views.progress, name='Progress'), # Достижения
    path('Article/', views.article, name='Article'), # Статьи
    path('Contact/', views.contact, name='Contact'), # Контакты
    path('Price/', views.price, name='Price'), # Прайс
    path('Docs/', views.docs, name='Docs'), # Документы
    path('Map/', views.mapping, name='Map'), # Карта сайта
    path('<str:url>/', views.this_page, name='this_page'), # Текущая страница
    path('<str:parent_url>/', views.parent_page, name='parent_page'), # Страница родителя
]

if settings.DEBUG: # Чтобы изображения могли отображаться в браузере
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)