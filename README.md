**DjangoMarNIISH**

**Применение изученного по курсу Python+ при освоении занятий по Django на сайте нашего НИИ**

**Страницы сайта**

URL | Название страницы | URL | Название страницы  
--- | --- | --- | ---  
/ | Главная страница | /Trend/ | Направления деятельности  
/News_last/ | Страница последних новостей | /Trend/editing/ | Редактирование направлений деятельности  
/News/<int:year>/ | Новости за каждый год | /Trend/update/<int:pk>/ | Изменение направления деятельности  
/News/editing/ | Редактирование новостей | /Trend/delete/<int:pk>/ | Удаление направления деятельности  
/News/update/<int:pk>/ | Изменение новости | /Progress/ | Достижения  
/News/delete/<int:pk>/ | Удаление новости | /Progress/editing/ | Редактирование достижений  
/News/News_picture/editing/ | Редактирование списка изображений новостей | /Progress/update/<int:pk>/ | Изменение достижений  
/News/News_picture/update/<int:pk>/ | Изменение изображения новости | /Progress/delete/<int:pk>/ | Удаление достижений  
/News/News_picture/delete/<int:pk>/ | Удаление изображения новости | /Article/ | Статьи  
/Prod/ | Продукция | /Article/editing/ | Редактирование списка статей НИИ  
/Taxon/editing/ | Редактирование таксонов | /Article/update/<int:pk>/ | Изменение статьи  
/Taxon/update/<int:pk>/ | Изменение таксона | /Article/delete/<int:pk>/ | Подтверждение удаления статьи  
/Taxon/delete/<int:pk>/ | Удаление таксона | /Contact/ | Контакты  
/Culture/editing/ | Редактирование культур | /Price/ | Прайс  
/Culture/update/<int:pk>/ | Изменение культуры | /Price/editing/ | Редактирование прайса  
/Culture/delete/<int:pk>/ | Удаление культуры | /Price/update/<int:pk>/ | Изменение прайса  
/Culture_group/editing/ | Редактирование группы культур | /Price/delete/<int:pk>/ | Подтверждение удаления прайса  
/Culture_group/update/<int:pk>/ | Изменение группы культур  | /Category/editing/  | Редактирование категорий продукции  
/Grain/  | Зерновые  | /Category/update/<int:pk>/  | Изменение категории продукции  
/Potato/  | Картофель  | /Category/delete/<int:pk>/  | Подтверждение удаления категории продукции  
/Grass/  | Многолетние травы  | /Docs/  | Документы  
/Jim/  | Жимолость  | /Docs/editing/  | Редактирование документов  
/About/*  | История института  | /Docs/delete/<int:pk>/  | Подтверждение удаления документа  
/About/editing*  | Добавление абзаца события  | /Docs/update/<int:pk>/  | Изменение документа  
/About/delete/<int:pk>/*  | Подтверждение удаления абзаца события  | /Map/  | Карта сайта  
/About/update/<int:pk>/ * | Изменение абзаца события   |

\* Тут ничего меняться почти не будет, поэтому добавление изображений сделал лишь через текстовую вставку ссылки
**Необходимые для функционирования сайта модели таблиц в БД**

Модель | Описание | Модель | Описание  
--- | --- | --- | ---  
Trend | Основные направления | Article | Статьи  
Progress | Достижения | Page | Шаблоны страниц  
TrendItem | Пункты направлений деятельности | Reference | Полезные ссылки  
HistoryData | Исторические даты | History | Исторические события к датам  
CultureGroup | Группы культур | Culture | Виды культур, воздеваемых в НИИ  
Taxon | Таксоны, воздеваемые в НИИ культур | Document | Публикованные документы НИИ  
ProdCategory | Названия категорий продукции | Price | Цены  
NewsPicture | Картинки для новостей | News | События НИИ  

**Этапы запуска сайта**

1\. В начале работы следует выполнить последовательно следующие команды:

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

