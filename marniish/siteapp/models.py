from django.db import models
from django.utils.safestring import mark_safe # Для избегания экранирования в News (нейросеть предложила)

class NameStr(models.Model): # Абстрактный класс, который является родительским для большинства моделей
    def __str__(self):
        return self.name # Для отображения наименования записи name
    class Meta:
        abstract = True # Делаем абстрактный класс

class Trend(NameStr): # Основные направления деятельности института
    name = models.CharField(max_length=10, unique=True) # Название направления (достаточно было и 5)
    class Meta:
        verbose_name = 'Основное направление деятельности' # Для отображения в админке
        verbose_name_plural = 'Основные направления деятельности' # Для отображения в админке

class YearTrends(models.Model): # Абстрактный класс: год и направление деятельности
    year = models.IntegerField() # Год
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE) # К какому основному направлению относится
    class Meta:
        abstract = True # Делаем абстрактный класс

class Article(YearTrends, NameStr): # Статьи
    name = models.CharField(max_length=500, unique=True)  # Библиоинфа из не более 500 символов (обычно их до 300)
    doi = models.CharField(max_length=50, blank=True)  # Значение DOI не выше 50 символов (обычно их до 40)
    link = models.CharField(max_length=100, blank=True)  # Ссылка на статью
    class Meta:
        verbose_name = 'Статья' # Для отображения в админке
        verbose_name_plural = 'Статьи' # Для отображения в админке

class Progress(YearTrends, NameStr): # Наиболее значимые достижения по направлениям НИР
    name = models.CharField(max_length=250) # Название достижения
    class Meta:
        verbose_name = 'Достижение' # Для отображения в админке
        verbose_name_plural = 'Достижения' # Для отображения в админке

class Page(models.Model): # Страница сайта
    url = models.CharField(max_length=30, unique=True)  # URL страницы (без .html)
    title = models.CharField(max_length=100) # Название страницы
    description = models.CharField(max_length=150) # Метаописание страницы
    parent_url = models.CharField(max_length=30, blank=True, null=True) # URL родительской страницы (без .html)
    parent_title = models.CharField(max_length=100, blank=True, null=True) # Название родительской страницы
    pre_parent_url = models.CharField(max_length=30, blank=True, null=True) # URL прародительской страницы (без .html)
    pre_parent_title = models.CharField(max_length=100, blank=True, null=True) # Название прародительской страницы
    def __str__(self):
        return self.title # Для отображения названия страницы
    class Meta:
        verbose_name = 'Страница сайта' # Для отображения в админке
        verbose_name_plural = 'Страницы сайта' # Для отображения в админке

class TrendItem(NameStr): # Пункты направления
    name = models.CharField(max_length=250, unique=True) # Название пункта направления
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE) # К какому основному направлению относится
    class Meta:
        verbose_name = 'Пункт направления' # Для отображения в админке
        verbose_name_plural = 'Пункты направления' # Для отображения в админке

class NameUnique100(models.Model): # Абстрактный класс: имя полезной ссылки или группы, или вида культур
    name = models.CharField(max_length=100, unique=True) # Название уникальное
    class Meta:
        abstract = True # Делаем абстрактный класс

class Reference(NameUnique100, NameStr): # Полезные ссылки
    id_name = models.CharField(max_length=10, unique=True)  # ID ссылки
    url = models.URLField(max_length=100, unique=True) # URL ссылки
    top = models.CharField(max_length=10, blank=True, null=True) # Расстояние до верхнего уровня в CSS
    left = models.CharField(max_length=10, blank=True, null=True) # Расстояние до левого края в CSS
    class Meta:
        verbose_name = 'Полезная ссылка' # Для отображения в админке
        verbose_name_plural = 'Полезные ссылки' # Для отображения в админке

class HistoryData(models.Model): # Историческая дата НИИ
    year = models.IntegerField() # Год
    day_month = models.CharField(max_length=15, blank=True, null=True) # Месяц и день
    def __str__(self):
        return f'{self.year} год {self.day_month or ''}' # Для отображения даты в строковом виде
    class Meta:
        ordering = ['year', 'day_month'] # Для сортировки
        verbose_name = 'Историческая дата' # Для отображения в админке
        verbose_name_plural = 'Исторические даты' # Для отображения в админке

class History(models.Model): # Исторические события НИИ
    text = models.CharField(max_length=1500) # Текст абзаца
    data = models.ForeignKey(HistoryData, on_delete=models.CASCADE) # Дата события (один-ко-многим)
    img = models.CharField(max_length=150, blank=True, null=True) # URL картинки
    alt = models.CharField(max_length=100, blank=True, null=True) # Описание картинки
    def __str__(self):
        return self.text # Для отображения наименования ссылки
    class Meta:
        verbose_name = 'Историческое событие' # Для отображения в админке
        verbose_name_plural = 'Исторические события' # Для отображения в админке

class CultureGroup(NameUnique100, NameStr): # Группа агрокультур, выращиваемых в НИИ
    add_info = models.CharField(max_length=250, blank=True, null=True) # Допинфа по группе
    class Meta:
        verbose_name = 'Группа агрокультур' # Для отображения в админке
        verbose_name_plural = 'Группы агрокультур' # Для отображения в админке

class Culture(NameUnique100, NameStr): # Виды агрокультур, выращиваемых в НИИ
    group = models.ForeignKey(CultureGroup, on_delete=models.CASCADE) # Группа культуры (связь один-ко-многим)
    class Meta:
        verbose_name = 'Вид агрокультуры' # Для отображения в админке
        verbose_name_plural = 'Виды агрокультур' # Для отображения в админке

class Taxon(models.Model): # Низшие таксоны агрокультур, выращиваемых в НИИ
    name = models.CharField(max_length=100) # Таксон с/х культуры (в редких случаях сорта и гибриды у различных культур могут совпадать)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE) # Культура (связь один-ко-многим)
    text = models.CharField(max_length=1500) # Текст описания
    img = models.ImageField(upload_to='Taxons', blank=True, null=True) # URL картинки, с загрузкой в /media/Taxons
    alt = models.CharField(max_length=100, blank=True, null=True) # Описание картинки
    def __str__(self):
        return f'{self.culture.name} {self.name}' # Для отображения наименования записи name и культуры
    class Meta:
        verbose_name = 'Таксон' # Для отображения в админке
        verbose_name_plural = 'Таксоны' # Для отображения в админке

class Document(models.Model): # Документы НИИ
    date = models.DateField() # Дата публикации ксивы (решил многие-ко-многим не делать, тут не особо надо)
    name = models.CharField(max_length=250)  # Название документа
    url = models.FileField(upload_to='Docs', unique=True) # URL документа, с загрузкой в /media/
    def __str__(self):
        return self.date.strftime('%d.%m.%Y') # Для отображения даты
    class Meta:
        ordering = ['-date'] # Для сортировки по дате по убыванию
        verbose_name = 'Документ' # Для отображения в админке
        verbose_name_plural = 'Документы' # Для отображения в админке

class ProdCategory(NameStr): # Категории качества продукции
    name = models.CharField(max_length=25) # Название категории
    class Meta:
        verbose_name = 'Категория качества' # Для отображения в админке
        verbose_name_plural = 'Категории качества' # Для отображения в админке

class Price(models.Model): # Цены продукции
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE) # Таксон (связь один-ко-многим)
    category = models.ForeignKey(ProdCategory, on_delete=models.CASCADE) # Категория качества (связь один-ко-многим)
    mass = models.FloatField() # Масса, т
    price = models.CharField(max_length=10, blank=True, null=True) # Цена
    def __str__(self):
        return self.taxon.name # Для отображения названия таксона
    class Meta:
        verbose_name = 'Прайс' # Для отображения в админке
        verbose_name_plural = 'Прайс-лист' # Для отображения в админке

class NewsPicture(models.Model): # Адрес картинки
    src = models.ImageField(upload_to='News', unique=True) # URL картинки, с загрузкой в /media/News
    alt = models.CharField(max_length=150, blank=True, null=True) # Описание картинки
    date = models.DateField(auto_now_add=True) # Дата добавления картинки
    def __str__(self):
        return f'{self.date}: {self.alt} ' # Отображаем время и название картинки
    class Meta:
        ordering = ['-date'] # Упорядочивание по дате
        verbose_name = 'Картинка' # Для отображения в админке
        verbose_name_plural = 'Картинки' # Для отображения в админке

class News(models.Model): # Новости сайта
    date = models.DateField(unique=True) # Дата события
    title = models.CharField(max_length=150) # Название события
    img = models.ManyToManyField(NewsPicture, blank=True) # Картинка блока
    text = models.TextField() # Текст неограниченной длины
    def __str__(self):
        return str(self.date) # Отображаем дату события
    class Meta:
        ordering = ['-date'] # Упорядочивание новостей по дате
        verbose_name = 'Событие' # Для отображения в админке
        verbose_name_plural = 'Новости НИИ' # Для отображения в админке