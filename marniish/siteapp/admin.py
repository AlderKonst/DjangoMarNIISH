from django.contrib import admin
from .models import * # Все модели загружаем (Trend, Article, Progress, Page, TrendItem, Reference, HistoryData, History)

admin.site.register(Trend) # Регистрируем модель с основными направлениями
admin.site.register(Article) # Регистрируем модель со статьями
admin.site.register(Progress) # Регистрируем модель с достижениями
admin.site.register(Page) # Регистрируем модель для шаблонов страниц
admin.site.register(TrendItem) # Регистрируем модель с пунктами направлений деятельности
admin.site.register(Reference) # Регистрируем модель с полезными ссылками
admin.site.register(HistoryData) # Регистрируем модель с историческими датами
admin.site.register(History) # Регистрируем модель с историческими событиями к датам