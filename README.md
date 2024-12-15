**DjangoMarNIISH**

**Применение изученного по курсу Python+ при освоении занятий по Django на сайте нашего НИИ**

**Страницы сайта**

|**Файл**|**Название**|**Файл**|**Название**|
| :- | :- | :- | :- |
|About.html|О нас|Map.html|Карта сайта|
|Article.html|Статьи|News.html|Новости|
|Contact.html|Контакты (применяется форма)|Potato.html|Картофель|
|Docs.html|Документы|Price.html|Прайс-лист|
|Grain.html|Зерновые культуры|Prod.html|Продукция|
|Grass.html|Многолетние травы|Progress.html|Достижения|
|Index.html|Главная страница|Trend.html|Направления деятельности|
|Jim.html|Синяя жимолость|||

**Необходимые для функционирования сайта модели таблиц в БД**

|Trend|Направления деятельности|CultureGroup|Группы культур|
| :- | :- | :- | :- |
|Article|Статьи|Culture|Культуры|
|Progress|Достижения|Taxon|Таксоны|
|Page|Страницы|Document|Документы|
|TrendItem|Пункты направлений деятельности|ProdCategory|Категории качества|
|Reference|Полезные ссылки|Price|Прайс-лист|
|HistoryData|Исторические даты|NewsPicture|Фото новостей|
|History|Исторические события|News|Событие|
||NewsBlock|Блоки событий||

**Этапы запуска сайта**

1\. В начале работы следует открыть следующий файл:

**DjangoMarRIA\marniish\siteapp\management\commands\\_\_init\_\_.py**

2\. В нём заменить на свой путь к проекту в следующей строчке:

|pc\_dir = os.path.join('F:\\', 'UII', 'Python+')|
| :-: |

3\. Выполнить последовательно следующие команды:

|1|**cd marniish**|Переведёт консоль на рабочую директорию|
| :- | - | :- |
|2|**python manage.py all\_run**|Сформирует все необходимые таблицы в БД парсингом страниц сайта, находящихся в **DjangoMarRIA\marniish\templates\MarRIA**|
|3|**python manage.py runserver**|Запустит сервер с рабочим сайтом|

**Дополнительные консольные команды**

<table><tr><th colspan="1" valign="top">python manage.py article</th><th colspan="2" valign="top">Пропарсить страницу и занести данные в БД для Article.html</th></tr>
<tr><td colspan="1" valign="top">то же culture</td><td colspan="2" valign="top">то же Grain.html, Grass.html, Jim.html, Potato.html (ещё создадутся медиафайлы)</td></tr>
<tr><td colspan="1" valign="top">то же doc</td><td colspan="2" valign="top">то же Docs.html (ещё создадутся медиафайлы)</td></tr>
<tr><td colspan="1" valign="top">то же history</td><td colspan="2" valign="top">то же About.html</td></tr>
<tr><td colspan="1" valign="top">то же news</td><td colspan="2" valign="top">то же News2016.html, … , News2024.html (ещё создадутся медиафайлы)</td></tr>
<tr><td colspan="1" valign="top">то же page</td><td colspan="2" valign="top">то же всех страниц</td></tr>
<tr><td colspan="1" valign="top">то же price</td><td colspan="2" valign="top">то же Price.html</td></tr>
<tr><td colspan="1" valign="top">то же progress</td><td colspan="2" valign="top">то же Progress.html</td></tr>
<tr><td colspan="1" valign="top">то же reference</td><td colspan="2" valign="top">то же index.html</td></tr>
<tr><td colspan="1" valign="top">то же trenditem</td><td colspan="2" valign="top">то же Trend.html</td></tr>
<tr><td colspan="1" valign="top">то же del_recs</td><td colspan="2" valign="top">Удалить все записи всех таблиц в БД</td></tr>
<tr><td colspan="1" rowspan="2" valign="top"><p>то же del_recs другие параметры через пробел, например:</p><p>python manage.py del_recs article progress price</p></td><td colspan="2" valign="top">Удаляет соответствующие ниже таблицы в БД</td></tr>
<tr><td colspan="1" valign="top">'trend': Trend <br>'article': Article <br>'progress': Progress <br>'page': Page <br>'trenditem': TrendItem <br>'reference': Reference <br>'historydata': HistoryData <br>'history': History </td><td colspan="1" valign="top">'culturegroup': CultureGroup <br>'culture': Culture <br>'taxon': Taxon <br>'document': Document <br>'prodcategory': ProdCategory <br>'price': Price <br>'newspicture': NewsPicture <br>'news': News <br>'newsblock': NewsBlock</td></tr>
</table>

