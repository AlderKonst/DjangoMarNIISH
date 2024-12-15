"""
В этом коде мы настраиваем WSGI-конфигурацию для нашего проекта marniish.
Переменная application экспортируется как модуль-уровневая переменная.

Для получения дополнительной информации о этом файле см.:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marniish.settings')

application = get_wsgi_application()
