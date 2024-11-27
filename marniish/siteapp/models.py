from django.db import models

class Trend(models.Model):# Основные направления деятельности института
    name = models.CharField(max_length=10) # Название направления (достаточно было и 5)
    def __str__(self):
        return self.name # Возвращает название направления

class Article(models.Model): # Статьи
    name = models.CharField(max_length=500)  # Библиоинфа из не более 500 символов (обычно их до 300)
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