from django.shortcuts import (render, # Импортируем функцию для рендеринга шаблонов,
                              get_object_or_404, # получения объекта или возврата 404 ошибки
                              HttpResponseRedirect) # и перенаправления
from django.urls import reverse_lazy # Импортируем функцию для получения URL по имени
from django.core.mail import EmailMessage # Импортируем функцию для отправки электронной почты

from .models import (Page, TrendItem, Reference, Article, Progress, History, ProdCategory,
                     HistoryData, Culture, Taxon, CultureGroup, Document, Price, News,
                     NewsPicture)  # Импортируем модели соответствующих таблиц
from .forms import (ContactForm, TrendItemAddForm, DocsAddForm, HistoryEditingForm, ArticleEditingForm, ProgressEditingForm, NewsEditingForm, NewsPictureEditingForm,
                    TaxonEditingForm, CultureEditingForm, CultureGroupEditingForm, PriceEditingForm, CategoryEditingForm) # Импортируем формы
import os # Здесь для удаления файла из /media/
from django.db.models import Min, Max # Импортируем функцию для получения мин и макс значений из БД

from django.views.generic.base import ContextMixin # Для создания общего класса
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView  # Базовые классы

class PageContextMixin(ContextMixin): # Миксин для добавления объекта Page в контекст
    page_url = None # Инициируем переменную
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['page'] = get_object_or_404(Page, url=self.page_url) # Добавляем страницу в контекст
        return context # Возвращаем контекст

class IndexTemplateView(PageContextMixin, TemplateView): # Для рендеринга главной страницы
    page_url = 'index' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/index.html' # Указываем расположение шаблона рендеринга
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['trends'] = TrendItem.objects.all() # Добавляем все записи таблицы TrendItem в контекст
        context['references'] = Reference.objects.all() # Добавляем все записи таблицы Reference в контекст
        return context # Передаём обновлённый контекст в страницу

class AllYearsContextMixin(ContextMixin): # Миксин для добавления объектов в контекст
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        min_year = News.objects.aggregate(Min('date__year'))['date__year__min'] # Получаем минимальный год
        max_year = News.objects.aggregate(Max('date__year'))['date__year__max'] # Получаем максимальный год
        context['all_years'] = range(min_year, max_year + 1) if min_year and max_year else [] # Добавляем все годы в контекст
        return context # Передаём обновлённый контекст в страницу

class NewsLastTemplateView(PageContextMixin, AllYearsContextMixin, TemplateView): # Для рендеринга страницы последних новостей
    page_url = 'News_last' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_last.html' # Указываем расположение шаблона рендеринга
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['newses'] = News.objects.all()[:3]  # Получаем последние 3 записи в таблице News
        return context # Передаём обновлённый контекст в страницу

class NewsListView(PageContextMixin, AllYearsContextMixin, ListView): # Для рендеринга страницы новостей
    template_name = 'siteapp/News.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'newses' # Указываем имя контекста
    def get_queryset(self): # Для получения записей в таблице News
        self.year = self.kwargs['year'] # Получаем значение поля year (благодаря self. ненужно передавать в контексте с помощью def get_context_data)
        self.page_url = self.year # Создаём наследованный из ContextMixin контекст из записи таблицы Page
        return News.objects.filter(date__year=self.year) # Получаем записи этого (year) года в таблице News
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['year'] = self.year # Добавляем year в контекст
        return context # Передаём обновлённый контекст в страницу

class NewsEditingView(PageContextMixin, AllYearsContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования новостей НИИ
    page_url = 'News_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_editing.html' # Указываем расположение шаблона рендеринга
    model = News # Указываем модель
    form_class = NewsEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на эту же страницу в случае успеха
    context_object_name = 'newses' # Указываем имя контекста

class NewsUpdateView(PageContextMixin, AllYearsContextMixin, UpdateView): # Для рендеринга страницы новостей НИИ
    page_url = 'News_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_update.html' # Указываем расположение шаблона рендеринга
    model = News # Указываем модель
    form_class = NewsEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на страницу редактирования новостей НИИ
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['newses'] = News.objects.all() # Оборачиваем объект для контекста в список
        return context # Передаём обновлённый контекст в страницу

class NewsDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы удаления новостей НИИ
    page_url = 'News_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_delete.html' # Указываем расположение шаблона рендеринга
    model = News # Указываем модель
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на страницу редактирования новостей НИИ
    context_object_name = 'deleted' # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['newses'] = News.objects.all() # Оборачиваем объект для контекста в список
        return context # Передаём обновлённый контекст в страницу

class NewsPictureEditingView(PageContextMixin, AllYearsContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования списка изображений новостей НИИ
    page_url = 'News_picture_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_picture_editing.html' # Указываем расположение шаблона рендеринга
    model = NewsPicture # Указываем модель
    form_class = NewsPictureEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на страницу редактирования новостей НИИ
    context_object_name = 'pictures' # Указываем имя контекста

class NewsPictureUpdateView(PageContextMixin, AllYearsContextMixin, UpdateView): # Для рендеринга страницы изменения новостного изображения
    page_url = 'News_picture_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_picture_update.html' # Указываем расположение шаблона рендеринга
    model = NewsPicture # Указываем модель
    form_class = NewsPictureEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на страницу редактирования новостей НИИ
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['pictures'] = NewsPicture.objects.all() # Передаем объект для контекста в список
        return context # Передаём обновлённый контекст в страницу

class NewsPictureDeleteView(PageContextMixin, AllYearsContextMixin, DeleteView): # Для рендеринга страницы удаления новостного изображения
    page_url = 'News_picture_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/News_picture_delete.html' # Указываем расположение шаблона рендеринга
    model = NewsPicture # Указываем модель
    success_url = reverse_lazy('siteapp:News_editing') # Перенаправляем на страницу редактирования новостей НИИ
    context_object_name = 'deleted' # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст
        context['pictures'] = NewsPicture.objects.all() # Оборачиваем объект для контекста в список
        return context # Передаём обновлённый контекст в страницу

class ContactTemplateView(PageContextMixin, TemplateView): # Для рендеринга страницы контактов (вот тебе и, блин, сокращённый код)
    page_url = 'Contact' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Contact.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Contact') # Перенаправляем на страницу контактов даже при успешном отправлении сообщения
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['form'] = ContactForm() # Добавляем форму в контекст
        return context # Передаём обновлённый контекст в страницу
    def post(self, request): # Для обработки данных формы
        form = ContactForm(request.POST) # Загружаем данные, полученные из формы
        if form.is_valid(): # Если форма валидна (все данные правильные)
            name = form.cleaned_data['name'] # Имя отправившего сообщение
            email = form.cleaned_data['email'] # Email отправившего сообщение
            subject = form.cleaned_data['subject'] or "Сообщение с сайта" # Тема отправившего сообщение с возможным значением по умолчанию
            message = form.cleaned_data['message'] # Сообщение отправившего сообщение
            message_txt = f"{message}\nОт: {name} <{email}>" # Текст сообщения
            email_message = EmailMessage( # Тут оказывается есть более новое и универсальное решение, чем send_email()
                subject, # Тема сообщения, на русском не работает правильно
                f'Тема сообщения: {subject}\nТекст сообщения: {message_txt}\n', # Тема и текст сообщения
                email, # Email отправившего сообщение
                ['marniish@yandex.ru']) # Кому отправляем
            email_message.send(fail_silently=False) # Отправляем сообщение
            return HttpResponseRedirect(self.success_url) # Перенаправляем на главную страницу
        else: # Если данные формы неправильные
            context = self.get_context_data() # Создаем контекст
            context['form'] = form # Добавляем форму в контекст
            return render(request, self.template_name, context) # Рендерим шаблон с передачей в него контекста

class ProdTemplateView(PageContextMixin, TemplateView): # Для рендеринга главной страницы
    page_url = 'Prod' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Prod.html' # Указываем расположение шаблона рендеринга

class TaxonEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования таксонов
    page_url = 'Taxon_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Taxon_editing.html' # Указываем расположение шаблона рендеринга
    model = Taxon # Указываем модель
    form_class = TaxonEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    context_object_name = 'taxons' # Указываем имя контекста

class TaxonUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы изменения таксона
    page_url = 'Taxon_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Taxon_update.html' # Указываем расположение шаблона рендеринга
    model = Taxon # Указываем модель
    form_class = TaxonEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    def get_context_data(self, **kwargs): # Для получения контекста
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['taxons'] = [self.object] # Оборачиваем объект для контекста в список
        return context # Возвращаем обновленный контекст

class TaxonDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы удаления таксона
    page_url = 'Taxon_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Taxon_delete.html' # Указываем расположение шаблона рендеринга
    model = Taxon # Указываем модель
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    context_object_name = 'deleted'  # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для получения контекста
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['taxons'] = [self.object] # Оборачиваем объект для контекста в список
        return context # Возвращаем обновленный контекст

class CultureEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования культур
    page_url = 'Culture_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Culture_editing.html' # Указываем расположение шаблона рендеринга
    model = Culture # Указываем модель
    form_class = CultureEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    context_object_name = 'cultures' # Указываем имя контекста

class CultureUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы изменения культуры
    page_url = 'Culture_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Culture_update.html' # Указываем расположение шаблона рендеринга
    model = Culture # Указываем модель
    form_class = CultureEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    def get_context_data(self, **kwargs): # Для получения контекста
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['cultures'] = Culture.objects.all() # Получаем все культуры
        return context  # Возвращаем обновленный контекст

class CultureDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы удаления культуры
    page_url = 'Culture_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Culture_delete.html' # Указываем расположение шаблона рендеринга
    model = Culture # Указываем модель
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    context_object_name = 'deleted' # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для получения контекста
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['cultures'] = Culture.objects.all() # Получаем все культуры
        return context # Возвращаем обновленный контекст

class CultureGroupEditingView(PageContextMixin, ListView): # Для рендеринга страницы группы культур
    page_url = 'Culture_group_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Culture_group_editing.html' # Указываем расположение шаблона рендеринга
    model = CultureGroup # Указываем модель
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    context_object_name = 'groups' # Указываем имя контекста

class CultureGroupUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы изменения группы культур
    page_url = 'Culture_group_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Culture_group_update.html' # Указываем расположение шаблона рендеринга
    model = CultureGroup # Указываем модель
    form_class = CultureGroupEditingForm # Указываем форму
    success_url = reverse_lazy('siteapp:Taxon_editing') # Перенаправляем на страницу редактирования таксонов
    def get_context_data(self, **kwargs): # Для получения контекста
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['groups'] = CultureGroup.objects.all() # Получаем все группы культур
        return context  # Возвращаем обновленный контекст

class CultureTaxonMixin(ContextMixin): # Миксин для добавления в контекст культуры и таксонов
    group_name = None # Определяем атрибут для имени группы
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['group'] = CultureGroup.objects.get(name=self.group_name) # Добавляем запись таблицы CultureGroup с нужным именем в контекст
        context['cultures'] = Culture.objects.filter(group=context['group'])  # Добавляем запись таблицы Culture в контекст с культурами этой группы
        context['taxons'] = Taxon.objects.filter(culture__in=context['cultures'])  # Добавляем запись таблицы Taxon в контекст с таксонами этих культур
        return context # Передаём обновлённый контекст в страницу

class GrainTemplateView(PageContextMixin, CultureTaxonMixin, TemplateView): # Для рендеринга страницы зерновых
    page_url = 'Grain' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Grain.html' # Указываем расположение шаблона рендеринга
    group_name = 'Зерновые культуры' # Указываем имя группы для передачи в контекст через миксин CultureTaxonMixin

class PotatoTemplateView(PageContextMixin, CultureTaxonMixin, TemplateView): # Для рендеринга страницы клубнеплодов
    page_url = 'Potato' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Potato.html' # Указываем расположение шаблона рендеринга
    group_name = 'Клубнеплоды' # Указываем имя группы для передачи в контекст через миксин CultureTaxonMixin

class GrassTemplateView(PageContextMixin, CultureTaxonMixin, TemplateView): # Для рендеринга страницы многолетних трав
    page_url = 'Grass' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Grass.html' # Указываем расположение шаблона рендеринга
    group_name = 'Многолетние травы' # Указываем имя группы для передачи в контекст через миксин CultureTaxonMixin

class JimTemplateView(PageContextMixin, CultureTaxonMixin, TemplateView): # Для рендеринга страницы жимолости
    page_url = 'Jim' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Jim.html' # Указываем расположение шаблона рендеринга
    group_name = 'Плодово-ягодные культуры' # Указываем имя группы для передачи в контекст через миксин CultureTaxonMixin

class HistoriesDataMixin(ContextMixin): # Миксин для добавления в контекст всех данных истории
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['histories'] = History.objects.all()  # Добавляем все записи таблицы History в контекст
        context['data'] = HistoryData.objects.all()  # Добавляем все записи таблицы HistoryData в контекст
        return context # Передаём обновлённый контекст в страницу

class AboutTemplateView(PageContextMixin, HistoriesDataMixin, TemplateView): # Для рендеринга страницы истории института
    page_url = 'About' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/About.html' # Указываем расположение шаблона рендеринга

# Для создания этих 3-х классов существенно помогла нейросеть
class HistoryEditingView(PageContextMixin, HistoriesDataMixin, CreateView): # Для рендеринга страницы редактирования истории
    page_url = 'About_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/About_editing.html' # Указываем расположение шаблона рендеринга
    form_class = HistoryEditingForm # Указываем форму для редактирования абзаца события
    success_url = reverse_lazy('siteapp:About_editing') # После успешного сохранения возвращаемся на эту же страницу
    def form_valid(self, form): # Метод для обработки валидной формы
        history_data, _ = HistoryData.objects.get_or_create( # Получаем или создаем объект HistoryData
            year=form.cleaned_data['year'], # Используем год из формы как параметр
            day_month=form.cleaned_data['day_month'] # Используем день и месяц из формы как параметр
        ) # Если объект не существует, он будет создан
        form.instance.data = history_data # Связываем событие с созданной или найденной датой
        return super().form_valid(form) # Вызываем родительский метод для завершения обработки формы

class HistoryUpdateView(PageContextMixin, HistoriesDataMixin, UpdateView): # Для рендеринга страницы изменения абзаца события
    page_url = 'About_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/About_update.html' # Указываем расположение шаблона рендеринга
    form_class = HistoryEditingForm  # Указываем форму для редактирования абзаца события
    success_url = reverse_lazy('siteapp:About_editing') # После успешного сохранения возвращаемся на страницу редактирования
    queryset = History.objects.all() # Для получения всех записей таблицы History
    def form_valid(self, form): # Метод для обработки валидной формы
        history_data, _ = HistoryData.objects.get_or_create( # Получаем или создаем объект HistoryData
            year=form.cleaned_data['year'], # Используем год из формы как параметр
            day_month=form.cleaned_data['day_month'] # Используем день и месяц из формы как параметр
        ) # Если объект не существует, он будет создан
        form.instance.data = history_data # Связываем событие с созданной или найденной датой
        return super().form_valid(form) # Вызываем родительский метод для завершения обработки формы
    def get_initial(self): # Переопределяем метод для получения инициализированных данных
        initial = super().get_initial() # Получаем инициализированные данные
        history_instance = self.get_object() # Получаем объект для отображения в шаблоне
        initial['year'] = history_instance.data.year # Используем год из формы как параметр
        initial['day_month'] = history_instance.data.day_month # Используем день и месяц из формы как параметр
        return initial # Возвращаем инициализированные данные

class HistoryDeleteView(PageContextMixin, HistoriesDataMixin, DeleteView): # Для рендеринга страницы подтверждения удаления абзаца события
    page_url = 'About_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/About_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:About_editing') # После успешного сохранения возвращаемся на страницу редактирования
    queryset = History.objects.all() # Для получения всех записей таблицы History
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['paragraph'] = self.get_object() # Получаем объект удаления для отображения в шаблоне
        return context # Передаём обновлённый контекст в страницу
    def post(self, request, *args, **kwargs): # POST-метод для обработки формы
        pk = self.kwargs.get('pk') # Получаем первичный ключ из URL
        history_instance = History.objects.get(pk=pk) # Получаем экземпляр History по первичному ключу
        data_instance = history_instance.data # Получаем связанный HistoryData
        history_instance.delete() # Удаляем экземпляр History
        if not History.objects.filter(data=data_instance).exists(): # Проверяем, остались ли другие History с этой же датой
            data_instance.delete() # Удаляем HistoryData, если нет связанных History
        return HttpResponseRedirect(self.success_url) # Перенаправляем на URL после успешного удаления

class TrendListView(PageContextMixin, ListView): # Для рендеринга страницы направлений деятельности
    page_url = 'Trend' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Trend.html' # Указываем расположение шаблона рендеринга
    queryset = TrendItem.objects.all() # Добавляем все записи таблицы TrendItem в контекст
    context_object_name = 'lis' # Указываем имя переменной контекста таким

class TrendEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Trend_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = TrendItem # Указываем модель
    form_class = TrendItemAddForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Trend_editing.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Trend_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    context_object_name = 'lis' # Указываем имя переменной контекста таким

class TrendUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Trend_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = TrendItem # Указываем модель
    form_class = TrendItemAddForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Trend_update.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Trend_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['lis'] = TrendItem.objects.all()  # Добавляем все записи таблицы TrendItem в контекст
        return context # Передаём обновлённый контекст в страницу

class TrendDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Trend_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = TrendItem # Указываем модель
    template_name = 'siteapp/Trend_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Trend_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    context_object_name = 'trend' # Указываем имя переменной контекста таким
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['lis'] = TrendItem.objects.all() # Добавляем все записи таблицы TrendItem в контекст
        return context # Передаём обновлённый контекст в страницу

class ProgressListView(PageContextMixin, ListView): # Для рендеринга страницы направлений деятельности
    page_url = 'Progress' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Progress.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'progresses' # Указываем имя переменной контекста таким
    queryset = Progress.objects.all() # Добавляем все записи таблицы TrendItem в контекст
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Progress.objects.all().order_by('-year') # Сортировка по убыванию года

class ProgressEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования списка достижений НИИ
    page_url = 'Progress_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Progress # Указываем модель
    form_class = ProgressEditingForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Progress_editing.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Progress_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    context_object_name = 'progresses' # Указываем имя переменной контекста таким
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Progress.objects.all().order_by('-year') # Сортировка по убыванию года

class ProgressUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы статей
    page_url = 'Progress_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Progress # Указываем модель
    form_class = ProgressEditingForm  # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Progress_update.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Progress_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Progress.objects.all().order_by('-year') # Сортировка по убыванию года
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['progresses'] = Progress.objects.all() # Добавляем все записи таблицы Progress в контекст
        return context # Передаём обновлённый контекст в страницу

class ProgressDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы подтверждения удаления достижения
    page_url = 'Progress_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Progress # Указываем модель
    template_name = 'siteapp/Progress_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Progress_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    context_object_name = 'deleted' # Указываем имя контекста удаления
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Progress.objects.all().order_by('-year') # Сортировка по убыванию года
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['progresses'] = Progress.objects.all() # Добавляем все записи таблицы Progress в контекст
        return context # Передаём обновлённый контекст в страницу

class ArticleListView(PageContextMixin, ListView): # Для рендеринга страницы статей
    page_url = 'Article' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Article.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'articles' # Указываем имя переменной контекста таким
    queryset = Article.objects.all() # Добавляем все записи таблицы Article в контекст
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Article.objects.all().order_by('-year') # Сортировка по убыванию года

class ArticleEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования списка статей
    page_url = 'Article_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Article # Указываем модель
    form_class = ArticleEditingForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Article_editing.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Article_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    context_object_name = 'articles' # Указываем имя переменной контекста таким
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Article.objects.all().order_by('-year') # Сортировка по убыванию года

class ArticleUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы изменения стати
    page_url = 'Article_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Article # Указываем модель
    form_class = ArticleEditingForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Article_update.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Article_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Article.objects.all().order_by('-year') # Сортировка по убыванию года
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['articles'] = Article.objects.all() # Добавляем все записи таблицы Article в контекст
        return context # Передаём обновлённый контекст в страницу

class ArticleDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы подтверждения удаления статьи
    page_url = 'Article_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Article # Указываем модель
    template_name = 'siteapp/Article_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Article_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    def get_queryset(self): # Возвращает отсортированный по году список статей
        return Article.objects.all().order_by('-year') # Сортировка по убыванию года
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['articles'] = Article.objects.all() # Добавляем все записи таблицы Article в контекст
        return context # Передаём обновлённый контекст в страницу

class PriceListView(PageContextMixin, ListView): # Для рендеринга страницы прайс-листа
    page_url = 'Price' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Price.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'prices' # Указываем имя переменной контекста таким
    queryset = Price.objects.all() # Добавляем все записи таблицы Price в контекст

class PriceEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования прайс-листа
    page_url = 'Price_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Price_editing.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'prices' # Указываем имя переменной контекста таким
    model = Price # Указываем модель
    form_class = PriceEditingForm # Указываем форму с передачей в виде контекста как 'form'
    success_url = reverse_lazy('siteapp:Price_editing') # Перенаправляем на страницу редактирования даже при успешном изменении записи

class PriceUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы редактирования прайс-листа
    page_url = 'Price_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Price_update.html' # Указываем расположение шаблона рендеринга
    model = Price # Указываем модель
    form_class = PriceEditingForm # Указываем форму с передачей в виде контекста как 'form'
    success_url = reverse_lazy('siteapp:Price_editing') # Перенаправляем на страницу редактирования при успешном изменении записи
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['prices'] = Price.objects.all() # Добавляем все записи таблицы Price в контекст
        return context # Передаём обновлённый контекст в страницу

class PriceDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы подтверждения удаления записи прайс-листа
    page_url = 'Price_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Price_delete.html' # Указываем расположение шаблона рендеринга
    model = Price # Указываем модель
    success_url = reverse_lazy('siteapp:Price_editing') # Перенаправляем на страницу редактирования при успешном удалении записи
    context_object_name = 'deleted'  # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['prices'] = Price.objects.all() # Добавляем все записи таблицы Price в контекст
        return context # Передаём обновлённый контекст в страницу

class CategoryEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования категорий продукции
    page_url = 'Category_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Category_editing.html' # Указываем расположение шаблона рендеринга
    model = ProdCategory # Указываем модель
    form_class = CategoryEditingForm # Указываем форму с передачей в виде контекста как 'form'
    success_url = reverse_lazy('siteapp:Category_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    context_object_name = 'prod_categories' # Указываем имя переменной контекста таким

class CategoryUpdateView(PageContextMixin, UpdateView): # Для рендеринга страницы редактирования категорий продукции
    page_url = 'Category_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = ProdCategory # Указываем модель
    form_class = CategoryEditingForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Category_update.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Category_editing') # Перенаправляем на страницу редактирования при успешном
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['prod_categories'] = ProdCategory.objects.all() # Добавляем все записи таблицы ProdCategory в контекст
        return context # Передаём обновлённый контекст в страницу

class CategoryDeleteView(PageContextMixin, DeleteView): # Для рендеринга страницы подтверждения удаления записи категории продукции
    page_url = 'Category_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = ProdCategory # Указываем модель
    template_name = 'siteapp/Category_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Category_editing') # Перенаправляем на страницу редактирования при успешном удалении записи
    context_object_name = 'deleted' # Указываем имя контекста удаления
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['prod_categories'] = ProdCategory.objects.all() # Добавляем все записи таблицы ProdCategory в контекст
        return context # Передаём обновлённый контекст в страницу

class DocsListView(PageContextMixin, ListView): # Для рендеринга страницы документов
    page_url = 'Docs' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Docs.html' # Указываем расположение шаблона рендеринга
    context_object_name = 'docs' # Указываем имя переменной контекста таким
    queryset = Document.objects.all() # Добавляем все записи таблицы Document в контекст

class DocsEditingView(PageContextMixin, CreateView, ListView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Docs_editing' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Document # Указываем модель
    form_class = DocsAddForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Docs_editing.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Docs_editing') # Перенаправляем на страницу редактирования даже при успешном отправлении сообщения
    context_object_name = 'docs' # Указываем имя переменной контекста таким

class DocsMixin(ContextMixin): # Миксин для добавления def get_context_data и def form_valid
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['docs'] = Document.objects.all() # Добавляем все записи таблицы Document в контекст
        return context # Передаём обновлённый контекст в страницу
    def form_valid(self, form): # Для переопределения работы с правильными данными
        one_doc = self.get_object() # Получаем текущий объект
        if one_doc.url and os.path.isfile(one_doc.url.path): # Если есть медиафайл с соответствующим url
            os.remove(one_doc.url.path) # то удаляем старый файл перед сохранением нового
        return super().form_valid(form) # Вызываем стандартный метод form_valid

class DocsUpdateView(PageContextMixin, DocsMixin, UpdateView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Docs_update' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Document # Указываем модель
    form_class = DocsAddForm # Указываем форму с передачей в виде контекста как 'form'
    template_name = 'siteapp/Docs_update.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Docs_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения

class DocsDeleteView(PageContextMixin, DocsMixin, DeleteView): # Для рендеринга страницы редактирования направлений деятельности
    page_url = 'Docs_delete' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    model = Document # Указываем модель
    template_name = 'siteapp/Docs_delete.html' # Указываем расположение шаблона рендеринга
    success_url = reverse_lazy('siteapp:Docs_editing') # Перенаправляем на страницу редактирования при успешном отправлении сообщения
    context_object_name = 'one_doc' # Указываем имя переменной контекста таким

class MapTemplateView(PageContextMixin, TemplateView): # Для рендеринга страницы карты сайта
    page_url = 'Map' # Создаём наследованный из ContextMixin контекст из записи таблицы Page
    template_name = 'siteapp/Map.html' # Указываем расположение шаблона рендеринга

class PageTemplateView(TemplateView): # Для отображения путей к страницам
    template_name = 'siteapp/index.html' # Указываем расположение шаблона рендеринга
    def get_context_data(self, **kwargs): # Для передачи данных в контекст
        context = super().get_context_data(**kwargs) # Получаем базовый контекст
        context['page'] = get_object_or_404(Page, url=kwargs['url']) # Добавляем url в цикл контекста
        return context # Передаём обновлённый контекст в страницу