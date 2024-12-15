from django.core.management.base import BaseCommand # Импорт базового класса команды Django
from siteapp.models import ProdCategory, Taxon, Price # Импорт моделей из siteapp

# Здесь будет добавление данных в БД для страницы Price.html

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = ['Суперсуперэлита', 'Суперэлита', 'Элита', 'Репродукция I', 'Репродукция II', 'Репродукция III'] # Категории качества зерна
        taxons = ['Безенчукская 380','Баженка', 'Родник Прикамья'] # Сорта (низший таксон)
        masses = [15, 20, 28] # Масса зерна в тоннах
        price = '' # Цена товара не указана
        for category in categories: # Перебираем список категорий качества зерна
            ProdCategory.objects.get_or_create(name=category) # Записываем категорию в БД (таблица ProdCategory)
        for mass, taxon in zip(masses, taxons): # Перебираем совместно список сортов и масс зерна
            Price.objects.create( # Записываем цену в БД (таблица Price)
                taxon=Taxon.objects.get(name=taxon), # Таксон низший
                category=ProdCategory.objects.get(name=categories[2]), # Элита
                mass=mass, # Масса зерна, т
                price=None) # Да, пусто, на потом