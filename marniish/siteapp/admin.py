from django.contrib import admin
from .models import * # Все модели загружаем (Trend, Article, Progress)

admin.site.register(Trend)
admin.site.register(Article)
admin.site.register(Progress)