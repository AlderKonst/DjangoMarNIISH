"""
Настройки Django для проекта marniish.

Сгенерировано с помощью 'django-admin startproject' с использованием Django 5.1.3.

Для получения дополнительной информации об этом файле, см.
https://docs.djangoproject.com/en/5.1/topics/settings/

Для полного списка настроек и их значений см.
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os # Из-за STATICFILES_DIRS и TEMPLATES

# Пути сборки внутри проекта, например: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Быстрые настройки для разработки - неприемлемо для производства
# Смотреть https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# ВНИМАНИЕ ПО БЕЗОПАСНОСТИ: храните секретный ключ, используемый в производстве, в секрете!
SECRET_KEY = 'django-insecure-45acl!f45^#3s58p%=1*g(wco7_kjqkh67_e!0u#oia_3ov(m0'

# ВНИМАНИЕ ПО БЕЗОПАСНОСТИ: не запускайте с включенным отладчиком в производстве!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siteapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marniish.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Свои шаблоны тут будут
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'marniish.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Проверка паролей на соответствие
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Международная локализация
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DATE_FORMAT = '%Y-%m-%d'  # Формат для вывода даты (2024.10.14)
DATE_INPUT_FORMATS = ['%Y-%m-%d']  # Формат для ввода даты

# Статичные файлы (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Указываем путь к статическим файлам

# Тип поля по умолчанию для первичного ключа
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media") # Для медиа файлов, которые часто меняются

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Используется для вывода сообщений в консоль