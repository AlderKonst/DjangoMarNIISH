from django.db import models

class Trend(models.Model):# Основные направления деятельности института
    name = models.CharField(max_length=10, unique=True) # Название направления (достаточно было и 5)
    def __str__(self):
        return self.name # Возвращает название направления

class Article(models.Model): # Статьи
    name = models.CharField(max_length=500, unique=True)  # Библиоинфа из не более 500 символов (обычно их до 300)
    year = models.IntegerField() # Год
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE) # Направление деятельности
    doi = models.CharField(max_length=50, blank=True)  # Значение DOI не выше 50 символов (обычно их до 40)
    link = models.CharField(max_length=100, blank=True)  # Ссылка на статью
    def __str__(self):
        return self.name # Возвращает библиоинфу

class Progress(models.Model): # Наиболее значимые достижения по направлениям НИР
    name = models.CharField(max_length=250) # Название достижения
    year = models.IntegerField() # Год
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)  # Направление деятельности
    def __str__(self):
        return self.name # Возвращает наименование достижения

class Page(models.Model): # Страница сайта
    title = models.CharField(max_length=100)  # Название страницы
    url = models.URLField(max_length=30, unique=True)  # URL страницы (без .html)
    description = models.CharField(max_length=150) # Метаописание страницы
    parent_url = models.URLField(max_length=30)  # URL родительской страницы (без .html)
    parent_title = models.CharField(max_length=100)  # Название родительской страницы
    def __str__(self):
        return self.title # Возвращает название страницы
