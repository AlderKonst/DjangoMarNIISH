from django.shortcuts import (render, # Импортируем функцию для рендеринга шаблонов,
                              get_object_or_404, # получения объекта или возврата 404 ошибки
                              HttpResponseRedirect) # и перенаправления
from django.urls import reverse # Импортируем функцию для получения URL по имени
from django.core.mail import send_mail # Импортируем функцию для отправки электронной почты
# Импортируем модели соответствующих таблиц
from .models import (Page, TrendItem, Reference, Article, Progress, History,
                     HistoryData, Culture, Taxon, CultureGroup, Document, Price, News)  # Импортируем модели соответствующих таблиц
from .forms import ContactForm # Импортируем форму

def index(request): # Для рендеринга главной страницы
    page = Page.objects.get(url='index') # Получаем запись в таблице Page с именем index в поле url
    trends = TrendItem.objects.all() # Получаем все записи в таблице TrendItem
    references = Reference.objects.all() # Получаем все записи в таблице Reference
    context = {'page': page, 'trends': trends, 'references': references} # Передаем поля в шаблон
    return render(request, 'siteapp/index.html', context) # Рендерим шаблон с передачей в него переменной page

def news(request, year): # Общая функция для рендеринга страницы новостей за определённый год
    page = get_object_or_404(Page, url='News' + str(year)) # Получаем запись в таблице Page с именем News со строчным year в поле url
    newses = News.objects.filter(date__year=year # Получаем записи этого (year) года в таблице News и
                                 ).prefetch_related('news_blocks') # связанными блоками NewsBlock, через имя 'news_bloks'
    context = {'page': page, 'newses': newses, 'year': year} # Передаем поля в шаблон
    return render(request, 'siteapp/News.html', context) # Рендерим шаблон с передачей в него переменных

def contact(request): # Для рендеринга страницы контактов
    page = Page.objects.get(url='Contact')  # Получаем запись в таблице Page с именем Contact в поле url
    if request.method == 'POST': # Если метод POST
        form = ContactForm(request.POST) # Загружаем данные, полученные из формы
        if form.is_valid(): # Если форма валидна (все данные правильные)
            name = form.cleaned_data['name'] # Имя отправившего сообщение
            email = form.cleaned_data['email'] # Email отправившего сообщение
            subject = form.cleaned_data['subject'] # Тема отправившего сообщение
            message = form.cleaned_data['message'] # Сообщение отправившего сообщение
            send_mail(subject, # Тема сообщения
                      f'{name} отправил текст сообщения: {message}',
                      email, # Email отправившего сообщение
                      ['marniish@yandex.ru'], # Кому отправляем
                      fail_silently=True) # Если не удалось отправить, то пропускаем
            return HttpResponseRedirect(reverse('siteapp:Contact')) # Перенаправляем на главную страницу
        else: # Если данные формы неправильные
            return render(request, 'siteapp/Contact.html', {'form': form}) # Рендерим шаблон с передачей в него переменной pag
    else:
        form = ContactForm() # Создаем форму
        context = {'page': page, 'form': form} # Передаем шаблон
        return render(request, 'siteapp/Contact.html', context) # Рендерим шаблон с передачей в него переменной page

def prod(request): # Для рендеринга страницы продукции
    page = Page.objects.get(url='Prod') # Получаем запись в таблице Page с именем Prod в поле url
    context = {'page': page} # Передаем шаблон
    return render(request, 'siteapp/Prod.html', context) # Рендерим шаблон с передачей в него переменной page

def grain(request): # Для рендеринга страницы зерновых
    page = Page.objects.get(url='Grain') # Получаем запись в таблице Page с именем Grain в поле url
    group = CultureGroup.objects.get(name='Зерновые культуры') # Получаем запись в таблице Culture с нужным именем
    cultures = Culture.objects.filter(group=group) # Получаем запись в таблице Culture с культурами этой группы
    taxons = Taxon.objects.filter(culture__in=cultures) # Получаем запись в таблице Taxon с таксонами этих культур
    context = {'page': page, 'groups': group, 'cultures': cultures, 'taxons': taxons} # Передаем записи в шаблон
    return render(request, 'siteapp/Grain.html', context) # Рендерим шаблон с передачей в него переменных

def potato(request): # Для рендеринга страницы картофеля
    page = Page.objects.get(url='Potato') # Получаем запись в таблице Page с именем Potato в поле url
    group = CultureGroup.objects.get(name='Клубнеплоды') # Получаем запись в таблице Culture с нужным именем
    cultures = Culture.objects.filter(group=group) # Получаем запись в таблице Culture с культурами этой группы
    taxons = Taxon.objects.filter(culture__in=cultures) # Получаем запись в таблице Taxon с таксонами этих культур
    context = {'page': page, 'groups': group, 'cultures': cultures, 'taxons': taxons} # Передаем записи в шаблон
    return render(request, 'siteapp/Potato.html', context) # Рендерим шаблон с передачей в него переменной page

def grass(request): # Для рендеринга страницы многолетних трав
    page = Page.objects.get(url='Grass') # Получаем запись в таблице Page с именем Grass в поле url
    group = CultureGroup.objects.get(name='Многолетние травы') # Получаем запись в таблице Culture с нужным именем
    cultures = Culture.objects.filter(group=group) # Получаем запись в таблице Culture с культурами этой группы
    taxons = Taxon.objects.filter(culture__in=cultures) # Получаем запись в таблице Taxon с таксонами этих культур
    context = {'page': page, 'groups': group, 'cultures': cultures, 'taxons': taxons} # Передаем записи в шаблон
    return render(request, 'siteapp/Grass.html', context) # Рендерим шаблон с передачей в него переменной page

def jim(request): # Для рендеринга страницы жимолости
    page = Page.objects.get(url='Jim') # Получаем запись в таблице Page с именем Jim в поле url
    group = CultureGroup.objects.get(name='Плодово-ягодные культуры') # Получаем запись в таблице Culture с нужным именем
    cultures = Culture.objects.filter(group=group) # Получаем запись в таблице Culture с культурами этой группы
    taxons = Taxon.objects.filter(culture__in=cultures) # Получаем запись в таблице Taxon с таксонами этих культур
    context = {'page': page, 'groups': group, 'cultures': cultures, 'taxons': taxons} # Передаем записи в шаблон
    return render(request, 'siteapp/Jim.html', context) # Рендерим шаблон с передачей в него переменной page

def about(request): # Для рендеринга страницы истории института
    page = Page.objects.get(url='About') # Получаем запись в таблице Page с именем About в поле url
    data = HistoryData.objects.all()  # Получаем все записи в таблице HistoryData
    histories = History.objects.all()  # Получаем все записи в таблице History
    context = {'page': page, 'histories': histories, 'data': data} # Передаем шаблон
    return render(request, 'siteapp/About.html', context) # Рендерим шаблон с передачей в него переменной page

def trend(request): # Для рендеринга страницы направлений деятельности
    page = Page.objects.get(url='Trend') # Получаем запись в таблице Page с именем Trend в поле url
    context = {'page': page} # Передаем шаблон
    return render(request, 'siteapp/Trend.html', context) # Рендерим шаблон с передачей в него переменной page

def progress(request): # Для рендеринга страницы достижений
    page = Page.objects.get(url='Progress') # Получаем запись в таблице Page с именем Progress в поле url
    progresses = Progress.objects.all()  # Получаем все записи в таблице Progress
    context = {'page': page, 'progresses': progresses} # Передаем в шаблон
    return render(request, 'siteapp/Progress.html', context) # Рендерим шаблон с передачей в него переменной page

def article(request): # Для рендеринга страницы статей
    page = Page.objects.get(url='Article') # Получаем запись в таблице Page с именем Article в поле url
    articles = Article.objects.all()  # Получаем все записи в таблице Article
    context = {'page': page, 'articles': articles} # Передаем шаблон
    return render(request, 'siteapp/Article.html', context) # Рендерим шаблон с передачей в него переменной page

def price(request): # Для рендеринга страницы прайса
    page = Page.objects.get(url='Price') # Получаем запись в таблице Page с именем Price в поле url
    prices = Price.objects.all()  # Получаем все записи в таблице Price
    context = {'page': page, 'prices': prices} # Передаем шаблон
    return render(request, 'siteapp/Price.html', context) # Рендерим шаблон с передачей в него переменной page

def docs(request): # Для рендеринга страницы документов
    page = Page.objects.get(url='Docs') # Получаем запись в таблице Page с именем Docs в поле url
    docs = Document.objects.all()  # Получаем все записи в таблице Docs
    context = {'page': page, 'docs': docs} # Передаем в шаблон
    return render(request, 'siteapp/Docs.html', context) # Рендерим шаблон с передачей в него переменной page

def mapping(request): # Для рендеринга страницы карты сайта
    page = Page.objects.get(url='Map') # Получаем запись в таблице Page с именем Map в поле url
    context = {'page': page} # Передаем шаблон
    return render(request, 'siteapp/Map.html', context) # Рендерим шаблон с передачей в него переменной page

# Для отображения текущих и родительских страниц
def this_page(request, url):  # Для отображения пути к текущей странице
    context = {'page': {'url': url}} # Передаем в шаблон page переменную url
    return render(request, 'siteapp/index.html', context) # Рендерим шаблон с передачей в него переменной page

def parent_page(request, parent_url): # Для отображения пути к родительской странице
    context = {'page': {'parent_url': parent_url}} # Передаем в шаблон page переменную parent_url
    return render(request, 'siteapp/index.html', context) # Рендерим шаблон с передачей в него переменной page