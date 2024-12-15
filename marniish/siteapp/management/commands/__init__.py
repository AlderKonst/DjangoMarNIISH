import os # Для работы с OC
pc_dir = os.path.join('F:\\', 'UII', 'Python+') # Директория в моём ПК
site_dir = os.path.join(pc_dir, 'DjangoMarRIA', 'marniish', 'templates', 'MarRIA') # Директория страниц для парсинга

# Проверяем существование директорий
if not os.path.exists(site_dir):
    print(f"Директория {site_dir} не найдена!\nНеобходимо в ..DjangoMarRIA/marniish/siteapp/management/commands/__init__.py сменить значение pc_dir")

from datetime import datetime # Для работы со временем
def date_transform( # Для прреобразования дат
        date_lst, # Список отпарсенных дат
        date_num, # Порядковых номер даты в списке date
        date_format="%Y-%m-%d", # Формат выходного преобразования дат
        ):
    months = { # Словарь для преобразования названий месяцев
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12
    }
    day, month_str, year = date_lst[date_num].split() # Дата публикации документа с номером date_num и разделяем на составляющие
    month = months[month_str] # Преобразуем месяц в число
    data_obj = datetime(year=int(year), month=month, day=int(day)) # Создаём объект datetime
    return data_obj.strftime(date_format) # Преобразуем дату и возвращаем её