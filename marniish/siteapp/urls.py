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

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'), # Главная страница
    path('News_last/', views.NewsLastTemplateView.as_view(), name='News_last'), # Страница последних новостей
    path('News/<int:year>/', views.NewsListView.as_view(), name='News'), # Добавляем пути для новостей за каждый год
    path('News/editing/', views.NewsEditingView.as_view(), name='News_editing'), # Редактирование новостей
    path('News/update/<int:pk>/', views.NewsUpdateView.as_view(), name='News_update'), # Изменение новости
    path('News/delete/<int:pk>/', views.NewsDeleteView.as_view(), name='News_delete'), # Удаление новости
    path('News/News_picture/editing/', views.NewsPictureEditingView.as_view(), name='News_picture_editing'),  # Редактирование списка изображений новостей
    path('News/News_picture/update/<int:pk>/', views.NewsPictureUpdateView.as_view(), name='News_picture_update'), # Изменение изображения новости
    path('News/News_picture/delete/<int:pk>/', views.NewsPictureDeleteView.as_view(), name='News_picture_delete'), # Удаление изображения новости
    path('Prod/', views.ProdTemplateView.as_view(), name='Prod'), # Продукция
    path('Taxon/editing/', views.TaxonEditingView.as_view(), name='Taxon_editing'), # Редактирование таксонов
    path('Taxon/update/<int:pk>/', views.TaxonUpdateView.as_view(), name='Taxon_update'), # Изменение таксона
    path('Taxon/delete/<int:pk>/', views.TaxonDeleteView.as_view(), name='Taxon_delete'), # Удаление таксона
    path('Culture/editing/', views.CultureEditingView.as_view(), name='Culture_editing'), # Редактирование культур
    path('Culture/update/<int:pk>/', views.CultureUpdateView.as_view(), name='Culture_update'), # Изменение культуры
    path('Culture/delete/<int:pk>/', views.CultureDeleteView.as_view(), name='Culture_delete'), # Удаление культуры
    path('Culture_group/editing/', views.CultureGroupEditingView.as_view(), name='Culture_group_editing'), # Редактирование группы культур
    path('Culture_group/update/<int:pk>/', views.CultureGroupUpdateView.as_view(), name='Culture_group_update'), # Изменение группы культур
    path('Grain/', views.GrainTemplateView.as_view(), name='Grain'), # Зерновые
    path('Potato/', views.PotatoTemplateView.as_view(), name='Potato'), # Картофель
    path('Grass/', views.GrassTemplateView.as_view(), name='Grass'), # Многолетние травы
    path('Jim/', views.JimTemplateView.as_view(), name='Jim'), # Жимолость
    path('About/', views.AboutTemplateView.as_view(), name='About'), # История института
    path('About/editing', views.HistoryEditingView.as_view(), name='About_editing'), # Добавление абзаца события
    path('About/delete/<int:pk>/', views.HistoryDeleteView.as_view(), name='About_delete'), # Подтверждение удаления абзаца события
    path('About/update/<int:pk>/', views.HistoryUpdateView.as_view(), name='About_update'), # Изменение абзаца события
    path('Trend/', views.TrendListView.as_view(), name='Trend'), # Направления деятельности
    path('Trend/editing/', views.TrendEditingView.as_view(), name='Trend_editing'), # Редактирование направлений деятельности
    path('Trend/update/<int:pk>/', views.TrendUpdateView.as_view(), name='Trend_update'), # Изменение направления деятельности
    path('Trend/delete/<int:pk>/', views.TrendDeleteView.as_view(), name='Trend_delete'), # Удаление направления деятельности
    path('Progress/', views.ProgressListView.as_view(), name='Progress'), # Достижения
    path('Progress/editing', views.ProgressEditingView.as_view(), name='Progress_editing'), # Редактирование достижений
    path('Progress/update/<int:pk>/', views.ProgressUpdateView.as_view(), name='Progress_update'), # Изменение достижений
    path('Progress/delete/<int:pk>/', views.ProgressDeleteView.as_view(), name='Progress_delete'), # Удаление достижений
    path('Article/', views.ArticleListView.as_view(), name='Article'), # Статьи
    path('Article/editing/', views.ArticleEditingView.as_view(), name='Article_editing'), # Редактирование списка статей НИИ
    path('Article/update/<int:pk>/', views.ArticleUpdateView.as_view(), name='Article_update'), # Изменение статьи
    path('Article/delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='Article_delete'), # Подтверждение удаления статьи
    path('Contact/', views.ContactTemplateView.as_view(), name='Contact'), # Контакты
    path('Price/', views.PriceListView.as_view(), name='Price'), # Прайс
    path('Price/editing/', views.PriceEditingView.as_view(), name='Price_editing'), # Редактирование прайса
    path('Price/update/<int:pk>/', views.PriceUpdateView.as_view(), name='Price_update'), # Изменение прайса
    path('Price/delete/<int:pk>/', views.PriceDeleteView.as_view(), name='Price_delete'), # Подтверждение удаления прайса
    path('Category/editing/', views.CategoryEditingView.as_view(), name='Category_editing'), # Редактирование категорий продукции
    path('Category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='Category_update'), # Изменение категории продукции
    path('Category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='Category_delete'), # Подтверждение удаления категории продукции
    path('Docs/', views.DocsListView.as_view(), name='Docs'), # Документы
    path('Docs/editing/', views.DocsEditingView.as_view(), name='Docs_editing'), # Редактирование документов
    path('Docs/delete/<int:pk>/', views.DocsDeleteView.as_view(), name='Docs_delete'), # Подтверждение удаления документа
    path('Docs/update/<int:pk>/', views.DocsUpdateView.as_view(), name='Docs_update'), # Изменение документа
    path('Map/', views.MapTemplateView.as_view(), name='Map'), # Карта сайта
    path('<path:url>/', views.PageTemplateView.as_view(), name='page'), # Текущая страница
]

if settings.DEBUG: # Чтобы изображения могли отображаться в браузере
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)