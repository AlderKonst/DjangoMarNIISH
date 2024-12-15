from django.db import models

class Trend(models.Model):# Основные направления деятельности института
    name = models.CharField(max_length=10, unique=True) # Название направления (достаточно было и 5)
    def __str__(self):
        return self.name # Для отображения названия направления

class Article(models.Model): # Статьи
    name = models.CharField(max_length=500, unique=True)  # Библиоинфа из не более 500 символов (обычно их до 300)
    year = models.IntegerField() # Год
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE) # К какому основному направлению относится
    doi = models.CharField(max_length=50, blank=True)  # Значение DOI не выше 50 символов (обычно их до 40)
    link = models.CharField(max_length=100, blank=True)  # Ссылка на статью
    def __str__(self):
        return self.name # Для отображения библиоинфы

class Progress(models.Model): # Наиболее значимые достижения по направлениям НИР
    name = models.CharField(max_length=250) # Название достижения
    year = models.IntegerField() # Год
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)  # К какому основному направлению относится
    def __str__(self):
        return self.name # Для отображения наименования достижения

class Page(models.Model): # Страница сайта
    title = models.CharField(max_length=100)  # Название страницы
    url = models.CharField(max_length=30, unique=True)  # URL страницы (без .html)
    description = models.CharField(max_length=150) # Метаописание страницы
    parent_url = models.URLField(max_length=30, blank=True, null=True)  # URL родительской страницы (без .html)
    parent_title = models.CharField(max_length=100, blank=True, null=True)  # Название родительской страницы
    def __str__(self):
        return self.title # Для отображения названия страницы

class TrendItem(models.Model): # Пункты направления
    name = models.CharField(max_length=250, unique=True)  # Название пункта направления
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE) # К какому основному направлению относится
    def __str__(self):
        return self.name # Для отображения названия направления

class Reference(models.Model): # Полезные ссылки
    name = models.CharField(max_length=100, unique=True)  # Наименование ссылки
    id_name = models.CharField(max_length=10, unique=True)  # ID ссылки
    url = models.URLField(max_length=100, unique=True) # URL ссылки
    top = models.CharField(max_length=10, blank=True, null=True) # Расстояние до верхнего уровня в CSS
    left = models.CharField(max_length=10, blank=True, null=True) # Расстояние до левого края в CSS
    def __str__(self):
        return self.name # Для отображения наименования ссылки

class HistoryData(models.Model): # Историческая дата НИИ
    year = models.IntegerField() # Год
    day_month = models.CharField(max_length=15, blank=True, null=True) # Месяц и день
    def __str__(self):
        return str(self.year) # Для отображения года в строковом виде

class History(models.Model): # Исторические события НИИ
    text = models.CharField(max_length=1500) # Текст абзаца
    data = models.ForeignKey(HistoryData, on_delete=models.CASCADE) # Дата события (один-ко-многим)
    img = models.URLField(max_length=150, blank=True, null=True) # URL картинки
    alt = models.CharField(max_length=100, blank=True, null=True) # Описание картинки
    def __str__(self):
        return self.text # Для отображения наименования ссылки

class CultureGroup(models.Model): # Группа агрокультур, выращиваемых в НИИ
    name = models.CharField(max_length=100, unique=True) # Группа культуры
    def __str__(self):
        return self.name # Для отображения наименования группы культур

class Culture(models.Model): # Виды агрокультур, выращиваемых в НИИ
    name = models.CharField(max_length=100, unique=True) # Вид с/х культуры
    group = models.ForeignKey(CultureGroup, on_delete=models.CASCADE) # Группа культуры (связь один-ко-многим)
    def __str__(self):
        return self.name # Для отображения вида культуры

class Taxon(models.Model): # Низшие таксоны агрокультур, выращиваемых в НИИ
    name = models.CharField(max_length=100) # Таксон с/х культуры
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE) # Культура (связь один-ко-многим)
    text = models.CharField(max_length=1500) # Текст описания
    img = models.ImageField(upload_to='Taxons', blank=True, null=True) # URL картинки, с загрузкой в /media/Taxons
    alt = models.CharField(max_length=100, blank=True, null=True) # Описание картинки
    def __str__(self):
        return self.name # Для отображения вида культуры

class Document(models.Model): # Документы НИИ
    date = models.DateField() # Дата публикации ксивы (решил многие-ко-многим не делать, тут не особо надо)
    name = models.CharField(max_length=250)  # Название документа
    url = models.FileField(upload_to='Docs', unique=True) # URL документа, с загрузкой в /media/
    def __str__(self):
        return self.date.strftime('%d.%m.%Y') # Для отображения даты

class ProdCategory(models.Model): # Категории качества продукции
    name = models.CharField(max_length=25) # Название категории
    def __str__(self):
        return self.name # Для отображения названия категории

class Price(models.Model): # Цены продукции
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE) # Таксон (связь один-ко-многим)
    category = models.ForeignKey(ProdCategory, on_delete=models.CASCADE) # Категория качества (связь один-ко-многим)
    mass = models.FloatField() # Масса, т
    price = models.IntegerField(blank=True, null=True) # Цена
    def __str__(self):
        return self.taxon.name # Для отображения названия таксона

class NewsPicture(models.Model): # Адрес картинки
    src = models.ImageField(upload_to='News', unique=True) # URL картинки, с загрузкой в /media/News
    alt = models.CharField(max_length=150, blank=True, null=True) # Описание картинки
    def __str__(self):
        return self.src.url # Отображаем адрес

class News(models.Model): # Новости сайта
    date = models.DateField(unique=True) # Дата события
    title = models.CharField(max_length=150) # Название события
    def __str__(self):
        return str(self.date) # Отображаем дату события
    class Meta:
        ordering = ['date'] # Упорядочивание новостей по дате также подсказал нейросеть

class NewsBlock(models.Model): # 1 блок события
    content_type = models.CharField(max_length=10, # Тип контента
                                    choices=(('text', 'Текст'), # Текст
                                             ('image', 'Картинка'))) # Картинка
    text = models.CharField(max_length=3000, blank=True, null=True) # Текст блока
    news = models.ForeignKey(News, null=True, on_delete=models.CASCADE, related_name='news_blocks')  # Событие (связь один-ко-многим)
    img = models.ForeignKey(NewsPicture, blank=True, null=True, on_delete=models.CASCADE) # Картинка блока
    order = models.PositiveIntegerField(default=0) # Порядоковый номер отображения блока
    def __str__(self):
        return self.text or str(self.img) # Отображаем или текст, или картинку
    class Meta:
        ordering = ['order', 'news'] # Упорядочивание новостей по новости и порядку также подсказал нейросеть