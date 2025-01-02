from django import forms # Для работы с формами
from django.db.models import Max # Для получения максимального значения в БД
from .models import TrendItem, Trend, Document, History, Article, Progress, CultureGroup, Culture, Taxon, ProdCategory, \
    Price, News, NewsPicture  # Для работы с моделью
import datetime # Для работы с примененными зонами (для NewsEditingForm)

class NewsEditingForm(forms.ModelForm): # Форма для страницы со списком новостей
    date = forms.DateField( # Поле для выбора даты
        label="Дата *", # Метка для поля
        initial=datetime.date.today, # Устанавливаем текущую дату по умолчанию
        widget=forms.DateInput(attrs={'type': 'date'})) # Виджет для выбора даты
    title = forms.CharField( # Поле для ввода заголовка
        label="Заголовок *", # Метка для поля
        max_length=150, # Максимальная длина заголовка
        widget=forms.TextInput(attrs={'placehholder': 'Введите текст заголовка'})) # Виджет для ввода заголовка
    text = forms.CharField( # Поле для ввода текста
        label="Текст *", # Метка для поля
        initial= '<p>Абзац №1</p>\n<p>Абзац №2</p>\n<p>Абзац №3</p>\n<p><a href="http://адрес">Текст ссылки</a></p>', # Значение по умолчанию
        widget=forms.Textarea()) # Виджет для ввода текста
    img = forms.ModelMultipleChoiceField( # Поле для выбора нескольких изображений
        label="Изображения", # Метка для поля
        required=False,  # Поле не обязательно для заполнения
        queryset=NewsPicture.objects.all(), # Список изображений
        widget=forms.SelectMultiple(attrs={'size': 5})) # Виджет для выбора нескольких изображений
    class Meta: # Класс для описания формы
        model = News # Модель, с которой связана форма
        fields = ['date', 'title', 'text', 'img'] # Поля, которые будут отображаться в форме

class NewsPictureEditingForm(forms.ModelForm): # Форма для страницы со списком изображений
    src = forms.FileField( # Поле для выбора и загрузки изображения
        label="Загрузить изображение *", # Метка для поля
        widget=forms.FileInput( # Виджет для выбора и загрузки изображения
            attrs={'accept': '.png,.jpeg,.jpg'})) # Такие форматы лишь будут допустимы
    alt = forms.CharField( # Поле для ввода альтернативного текста
        label="Альтернативный текст", # Метка для поля
        required=False, # Поле не обязательно для заполнения
        widget=forms.TextInput(attrs={'placehholder': 'Введите описание картинки'})) # Виджет для ввода описания картинки
    class Meta: # Класс для описания формы
        model = NewsPicture # Модель, с которой связана форма
        fields = ['src', 'alt'] # Поля, которые будут отображаться в форме

class PriceEditingForm(forms.ModelForm): # Форма для страницы со списком цен
    taxon = forms.ModelChoiceField( # Поле для выбора таксона
        label="Таксон *", # Метка для поля
        queryset=Taxon.objects.all(), # Список таксонов
        widget=forms.Select()) # Виджет для выбора таксона
    category = forms.ModelChoiceField( # Поле для выбора категории продукции
        label="Категория продукции *", # Метка для поля
        queryset=ProdCategory.objects.all(), # Список категорий продукции
        widget=forms.Select()) # Виджет для выбора категории продукции
    mass = forms.FloatField( # Поле для ввода массы продукции
        label="Масса, т *", # Метка для поля
        widget=forms.NumberInput( # Виджет для ввода числа
            attrs={'placeholder': 'Введите массу продукции в тоннах'})) # Подсказка для ввода массы продукции
    price = forms.CharField( # Поле для ввода цены продукции
        label="Цена", # Метка для поля
        initial="договорная", # Значение по умолчанию
        required=False, # Поле не обязательно для заполнения
        widget=forms.TextInput( # Виджет для ввода цены продукции
            attrs={'placeholder': 'Оставить договорную или ввести цену с указанием единицы измерения'})) # Подсказка для ввода цены продукции
    class Meta: # Класс для описания формы
        model = Price # Модель, с которой связана форма
        fields = ['taxon', 'category', 'mass', 'price'] # Поля, которые будут отображаться в форме

class CategoryEditingForm(forms.ModelForm): # Форма для страницы со списком категорий продукции
    name = forms.CharField( # Поле для ввода названия категории продукции
        label="Название категории продукции *", # Метка для поля ввода названия категории продукции
        max_length=25, # Максимальное количество символов названия категории продукции
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите название категории продукции (не более 25 символов)'})) # Подсказка для ввода названия категории продукции
    class Meta: # Класс для описания формы
        model = ProdCategory # Модель, с которой связана форма
        fields = ['name'] # Поля, которые будут отображаться в форме

class CultureGroupEditingForm(forms.ModelForm): # Форма для страницы со списком групп культуры
    name = forms.CharField( # Поле для ввода имени группы культуры
        label="Имя группы культур *", # Метка для поля
        max_length=100, # Максимальное количество символов имени группы культур
        widget=forms.Textarea( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите имя группы культуры'})) # Подсказка для ввода имени группы культуры
    add_info = forms.CharField( # Поле для ввода дополнительной информации
        label="Дополнительная информация *", # Метка для поля
        max_length=250, # Максимальное количество символов дополнительной информации
        widget=forms.Textarea( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите дополнительную информацию'})) # Подсказка для ввода дополнительной информации
    class Meta: # Класс для описания формы
        model = CultureGroup # Модель, с которой связана форма
        fields = ['name', 'add_info'] # Поля, которые будут отображаться в форме

class CultureEditingForm(forms.ModelForm): # Форма для страницы со списком культур
    name = forms.CharField( # Поле для ввода названия культуры
        label="Название культуры *", # Метка для поля ввода названия культуры
        max_length=100, # Максимальное количество символов названия культуры
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите название культуры'})) # Подсказка для ввода названия культуры
    group = forms.ModelChoiceField( # Поле выбора группы культуры
        label="Группа культуры *", # Метка для поля выбора группы культуры
        queryset=CultureGroup.objects.all(), # Получение всех объектов модели CultureGroup
        widget=forms.Select()) # Использование стандартного виджета выбора
    class Meta: # Класс для описания формы
        model = Culture # Модель, с которой связана форма
        fields = ['name', 'group'] # Поля, которые будут отображаться в форме

class TaxonEditingForm(forms.ModelForm): # Форма для страницы со списком таксонов
    name = forms.CharField( # Поле для ввода названия таксона
        label="Название таксона *", # Метка для поля ввода названия таксона
        max_length=100, # Максимальное количество символов названия таксона
        required=False, # Поле не является обязательным для заполнения
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите таксон (гибрид, сорт)'})) # Подсказка для ввода названия таксона
    culture = forms.ModelChoiceField( # Поле выбора культуры
        label="Культура *", # Метка для поля выбора культуры
        queryset=Culture.objects.all(), # Получение всех объектов модели Culture
        widget=forms.Select()) # Использование стандартного виджета выбора
    text = forms.CharField( # Поле для ввода текста
        label="Описание *", # Метка для поля ввода текста
        max_length=1000, # Максимальное количество символов описания таксона
        widget=forms.Textarea( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите описание таксона'})) # Подсказка для ввода текста
    img = forms.FileField( # Поле для загрузки изображения
        label="Загрузить документ", # Метка для загрузки изображения, с загрузкой в /media/
        required=False, # Поле не является обязательным для заполнения
        widget=forms.FileInput( # Виджет для загрузки изображения через html-код
            attrs={'accept': '.png,.jpeg,.jpg'})) # Такие форматы лишь будут допустимы
    alt = forms.CharField( # Поле для ввода описания картинки
        label="Описание картинки", # Метка для поля ввода описания картинки
        max_length=100, # Максимальная количество символов текста описания картинки
        required=False, # Поле не является обязательным
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Описание'})) # Подсказка для ввода описания картинки
    class Meta: # Класс для описания формы
        model = Taxon # Модель, с которой связана форма
        fields = ['name', 'culture', 'text', 'img', 'alt'] # Поля, которые будут отображаться в форме

class ArticleEditingForm(forms.ModelForm): # Форма для страницы со списком статей НИИ
    year = forms.IntegerField( # Поле для ввода года публикации статьи
        label="Год *", # Метка для поля ввода года
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите год'})) # Подсказка для ввода года
    trend = forms.ModelChoiceField( # Поле выбора основного направления
        label="Основное направление НИИ *", # Метка для поля выбора основного направления НИИ
        queryset=Trend.objects.all(), # Получение всех объектов модели Trend
        widget=forms.Select())  # Использование стандартного виджета выбора
    name = forms.CharField( # Поле для ввода статьи
        label="Статья *", # Метка для поля ввода статьи
        max_length=500, # Максимальное количество символов статьи
        widget=forms.Textarea( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите статью'})) # Подсказка для ввода статьи
    doi = forms.CharField( # Поле для ввода DOI документа
        label="DOI", # Метка для поля ввода DOI документа
        max_length=50, # Максимальное количество символов DOI
        required=False, # Поле не является обязательным для заполнения
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите без https://doi.org/'})) # Подсказка для ввода DOI документа
    link = forms.CharField( # Поле для ввода ссылки
        label="URL", # Метка для поля ввода ссылки
        max_length=100, # Максимальное количество символов ссылки
        required=False, # Поле не является обязательным для заполнения
        widget=forms.TextInput( # Виджет для ввода текста в html-код
             attrs={'placeholder': 'Введите полный URL'})) # Подсказка для ввода ссылки
    def __init__(self, *args, **kwargs): # Конструктор формы
        super().__init__(*args, **kwargs) # Вызываем метод родительского класса
        max_year = Article.objects.aggregate(Max('year'))['year__max'] # Получаем максимальный год из БД (спасибо нейросети)
        self.fields['year'].initial = max_year # Устанавливаем значение по умолчанию для поля year
        self.fields['trend'].initial = Trend.objects.get(name='plant') # Устанавливаем значение по умолчанию для поля trend
    class Meta: # Класс для работы с моделью формы
        model = Article # Модель для работы с моделью
        fields = ['year', 'trend', 'name', 'doi', 'link'] # Поля для работы с моделью

class ProgressEditingForm(forms.ModelForm): # Форма для страницы со списком достижений НИИ
    year = forms.IntegerField( # Поле для ввода года достижения
        label="Год *", # Метка для поля ввода года
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите год'})) # Подсказка для ввода года
    trend = forms.ModelChoiceField( # Поле выбора основного направления
        label="Основное направление НИИ *", # Метка для поля выбора основного направления НИИ
        queryset=Trend.objects.all(), # Получение всех объектов модели Trend
        widget=forms.Select()) # Использование стандартного виджета выбора
    name = forms.CharField( # Поле для ввода достижения
        label="Достижение *", # Метка для поля ввода достижения
        max_length=250, # Максимальное количество символов достижения
        widget=forms.Textarea( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите достижение'})) # Подсказка для ввода достижения
    def __init__(self, *args, **kwargs): # Конструктор формы
        super().__init__(*args, **kwargs) # Вызываем метод родительского класса
        max_year = Article.objects.aggregate(Max('year'))['year__max'] # Получаем максимальный год из БД (спасибо нейросети)
        self.fields['year'].initial = max_year # Устанавливаем значение по умолчанию для поля year
        self.fields['trend'].initial = Trend.objects.get(name='plant') # Устанавливаем значение по умолчанию для поля trend
    class Meta: # Класс для работы с моделью
        model = Progress # Модель для работы с моделью
        fields = ['year', 'trend', 'name'] # Поля для работы с моделью

class HistoryEditingForm(forms.ModelForm): # Форма для страницы с событием НИИ
    year = forms.IntegerField( # Поле для ввода года
        label="Год *", # Метка для поля ввода года
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите год'})) # Подсказка для ввода года
    day_month = forms.CharField( # Поле для ввода дня и месяца
        label="День и месяц", # Метка для поля ввода дня и месяца
        max_length=15, # Максимальная количество символов текста строки
        required=False, # Поле не является обязательным
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': '22 февраля (образец)'})) # Подсказка для ввода дня и месяца
    text = forms.CharField( # Поле для ввода текста абзаца
        label="Текст абзаца *", # Метка для поля ввода текста абзаца
        max_length=1500, # Максимальная количество символов текста абзаца
        widget=forms.Textarea( # Виджет для ввода большого текста в html-код
            attrs={'placeholder': 'Текст абзаца ...'})) # Подсказка для ввода текста абзаца
    img = forms.CharField( # Поле для ввода URL изображения
        label="URL изображения", # Метка для поля ввода URL изображения
        required=False, # Поле не является обязательным
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Сперва скопировать в папку static!'}))  # Подсказка по загрузке изображения
    alt = forms.CharField( # Поле для ввода описания картинки
        label="Описание картинки", # Метка для поля ввода описания картинки
        max_length=100, # Максимальная количество символов текста описания картинки
        required=False, # Поле не является обязательным
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Описание'})) # Подсказка для ввода описания картинки
    class Meta: # Класс для описания модели
        model = History # Модель для описания события
        fields = ['year', 'day_month', 'text', 'img', 'alt'] # Дата события, текст абзаца, фото и его описание

class ContactForm(forms.Form): # Форма для страницы с контактами для отправки сообщений в почту
    name = forms.CharField( # Поле для ввода имени
        label="Имя *", # Метка для поля ввода имени
        max_length=100, # Максимальная количество символов текста имени
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите Ваше Имя'})) # Подсказка для ввода имени
    email = forms.EmailField( # Поле для ввода email адреса
        label="Электронная почта *", # Метка для поля ввода email
        max_length=100, # Максимальная количество символов email адреса
        widget=forms.EmailInput( # Виджет для ввода емейла в html-код
            attrs={'placeholder': 'email@email.ru'})) # Подсказка для ввода email адреса
    subject = forms.CharField( # Поле для ввода темы сообщения
        label="Тема сообщения", # Метка для поля ввода темы сообщения
        max_length=150, # Максимальная количество символов текста темы сообщения
        required=False, # Поле не является обязательным
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите Тему сообщения'})) # Подсказка для ввода темы сообщения
    message = forms.CharField( # Поле для ввода сообщения
        label="Сообщение *", # Метка для поля ввода сообщения
        widget=forms.Textarea( # Виджет для ввода большого текста в html-код
            attrs={'placeholder': 'Произвольный текст сообщения ...'})) # Подсказка для ввода текста сообщения

class TrendItemAddForm(forms.ModelForm): # Форма для страницы с направлениями НИИ для добавления нового направления
    name = forms.CharField( # Поле для ввода текста направления
        label="Направление деятельности НИИ *", # Метка для поля ввода направления деятельности НИИ
        max_length=250, # Максимальная количество символов текста названия направления
        widget=forms.TextInput( # Виджет для ввода текста в html-код
            attrs={'placeholder': 'Введите ещё одно направление деятельности НИИ'})) # Подсказка для ввода направления
    trend = forms.ModelChoiceField( # Поле выбора основного направления
        label="Основное направление НИИ *", # Метка для поля выбора основного направления НИИ
        queryset=Trend.objects.all(), # Получение всех объектов модели Trend
        widget=forms.Select()) # Использование стандартного виджета выбора
    class Meta: # Класс для описания модели
        model = TrendItem # Модель для описания пункта основного направления НИИ
        fields = ['name', 'trend'] # Пункт основного направления и основное направление деятельности НИИ

class DocsAddForm(forms.ModelForm): # Форма для добавления документов в систему
    date = forms.DateField( # Поле для выбора даты публикации документа
        widget=forms.DateInput( # Виджет для ввода даты в html-код
            attrs={'type': 'date'}), # Указываем тип поля как дата
            label="Дата публикации документа") # Указываем метку здесь
    name = forms.CharField( # Поле для ввода названия документа
        label="Название документа", # Метка для поля ввода названия документа
        max_length=250, # Максимальная количество символов текста названия документа
        widget=forms.Textarea( # Виджет для ввода большого текста в html-код
            attrs={'placeholder': 'Введите название документа'})) # Подсказка для ввода названия документа
    url = forms.FileField( # Поле для загрузки документа
        label="Загрузить документ", # Метка для загрузки документа, с загрузкой в /media/
        widget=forms.FileInput( # Виджет для загрузки документа через html-код
            attrs={'accept': '.pdf,.doc,.docx'})) # Такие форматы лишь будут допустимы
    class Meta: # Класс для описания модели
        model = Document # Модель для описания документов
        fields = ['date', 'url', 'name'] # Дата публикации документа, его название и URL

