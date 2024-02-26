"""
Django settings for crag project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from dotenv import load_dotenv
from pathlib import Path
from celery.schedules import crontab
import os
import graypy

# Загрузка переменных окружения из файла .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Разрешите всем хостам доступ к кукам, чтобы CSRF-токены могли быть установлены
CSRF_TRUSTED_ORIGINS = ['https://creg.boardmaps.ru']

# Доверьтесь заголовкам X-Forwarded-For и X-Forwarded-Proto
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Указываем разрешение с какого адреса можно запускать сервер
ALLOWED_HOSTS = ['*']

# Добавляем русские буквы
JSON_USE_UTF8 = True

# Application definition

INSTALLED_APPS = [
    'dbbackup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'main',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'api',
    'apiv2',
    # выключил проверку на HTTPS
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    # 'django_celery_monitor',
    'axes',
    'auditlog',
]

# Настройки пути для сохранения резервных копий
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'  # Хранилище файлов
DBBACKUP_STORAGE_OPTIONS = {'location': './backup/db/'}  # Путь к папке для сохранения резервных копий

# # Настройки для PostgreSQL
# DBBACKUP_CLEANUP_KEEP = 3  # Количество последних бэкапов, которые нужно сохранить

# # Настройки для автоматического создания бэкапов
# DBBACKUP_BACKUP_COMMANDS = [
#     {
#         'databases': ['default'],  # Имя базы данных (если используется несколько баз данных, укажите нужные имена)
#         'command': 'dbbackup',  # Команда для создания бэкапа
#         'extension': 'sql',  # Расширение файла бэкапа (может быть 'sql', 'tar', 'zip' и др.)
#         'compress': False,  # Сжатие бэкапа (True или False)
#     },
# ]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'JSON_INDENT': 4,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # выключил проверку на HTTPS
    'corsheaders.middleware.CorsMiddleware',
    'api.middleware.AppendSlashWithPOSTMiddleware',
    'api.middleware.ExceptionLoggingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

# выключил проверку на HTTPS
CORS_ORIGIN_ALLOW_ALL = True

# Автоматически логировать все таблицы в БД
AUDITLOG_INCLUDE_ALL_MODELS=True

ROOT_URLCONF = 'crag.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.favicon',
            ],
        },
    },
]

WSGI_APPLICATION = 'crag.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Делаем переменное окружение для определения локального запуска проекта или в докере (production)
# Перед запуском нужно выполнить команду: export DJANGO_ENV=local
# Windows set DJANGO_ENV=local
# Для установки переменного окружения DJANGO_ENV
DJANGO_ENV = os.environ.get('DJANGO_ENV')

if DJANGO_ENV == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'database_1_test',
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
elif 'GITHUB_ACTIONS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': '5432',
        }
    }
    from django_auth_ldap.config import LDAPSearch
    import ldap

    AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Basic Django auth
    'django_auth_ldap.backend.LDAPBackend',      # LDAP auth
    'axes.backends.AxesBackend',
    ]

    # Rонфигурации для django-axes:
    # Ограничение на количество неудачных попыток входа
    AXES_FAILURE_LIMIT = 5

    # Период, в течение которого считаются неудачные попытки (в минутах)
    AXES_COOLOFF_TIME = 60

    # Блокировка IP-адресов после достижения лимита
    AXES_LOCK_OUT_AT_FAILURE = True

    # Настройки для подключения к LDAP-серверу
    AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI')
    AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN')
    AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD')

    # Настройка будет пытаться найти пользователя в созданной нами OU Django и стандартной папке DashboardUsers, 
    # сопоставляя введенный login пользователя с аттрибутами sAMAccountName
    AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=DashboardUsers,dc=corp,dc=boardmaps,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")

    # Указываем как переносить данные из AD в стандартный профиль пользователя Django
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
    }

    # # Сохраняем сессию после закрытия браузера
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 две недели в секундах


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Настройки Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# Сохраняем результаты задач в БД
CELERY_TASK_IGNORE_RESULT = False
CELERY_IGNORE_RESULT = False
CELERY_BEAT_SCHEDULER = os.environ.get('CELERY_BEAT_SCHEDULER')

# Расписание Celery Beat
CELERY_BEAT_SCHEDULE = {
    'update_module_info': {
        'task': 'api.tasks.update_module_info_task',
        'schedule': crontab(hour=3, minute=0),  # Запуск в 3:00 по МСК
    },
    'update_tickets': {
        'task': 'api.tasks.update_tickets_task',
        'schedule': crontab(hour=22, minute=0),  # Запуск в 22:00 по МСК
    },
    'artifactory_downloads_log': {
        'task': 'api.tasks.artifactory_downloads_log_task',
        'schedule': crontab(hour=23, minute=00),  # Запуск в 23:00 по МСК
    },
}

# Настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Настройка, которая убирает слэш в конце "/"
# APPEND_SLASH = False

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # Создаем запись логов со временем
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': './logs/debug.log',
            'when': 'midnight',  # Устанавливаем создане нового файла логов на полночь
            'interval': 1,  # Устанавливаем создание файлов на каждый день свой
            'backupCount': 10,  # Устанавливаем количество лог файлов
            'formatter': 'verbose',  # Применяем форматтер
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/info.log',
            'maxBytes': 1024*1024*2,  # Устанавливаем размер файла логов в 2 MB
            'backupCount': 5,  # Устанавливаем количество файлов логов в 5 файлов
            'formatter': 'verbose',  # Применяем форматтер
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/warning.log',
            'maxBytes': 1024*1024*5, # Устанавливаем размер файла логов в 5 MB
            'backupCount': 2, # Устанавливаем количество файлов логов в 2 файлов
            'formatter': 'verbose', # Применяем форматтер
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/error.log',
            'maxBytes': 1024*1024*2,  # Устанавливаем размер файла логов в 2 MB
            'backupCount': 3,  # Устанавливаем количество файлов логов в 3 файла
            'formatter': 'verbose',  # Применяем форматтер
        },
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/critical.log',
            'maxBytes': 1024*1024*2,  # Устанавливаем размер файла логов в 1 MB
            'backupCount': 3,  # Устанавливаем количество файлов логов в 3 файла
            'formatter': 'verbose',  # Применяем форматтер
        },
        'celery_info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/celery_info.log',
            'maxBytes': 1024*1024*2,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'celery_error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/celery_error.log',
            'maxBytes': 1024*1024*2,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',  # Применяем форматтер
        },
        'gelf': {
        'level': 'INFO',
        'class': 'graypy.GELFTCPHandler',
        #'host': 'graylog.boardmaps.ru',
        'host': '10.6.75.201',
        'port': 12201,  # Порт Graylog GELF TCP input
        'facility': 'Creg',  # Задаём имя источника для отображения в Graylog
        },
        'gelf_celery': {
            'level': 'INFO',
            'class': 'graypy.GELFTCPHandler',
            'host': '10.6.75.201',
            'port': 12201,
            'facility': 'Celery',  # Задаём имя источника для отображения в Graylog
        },
    },
    'root': {
        'handlers': ['file', 'console', 'gelf'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'info_file', 'warning_file', 'error_file', 'critical_file', 'console', 'gelf'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['file', 'celery_info_file', 'celery_error_file', 'console', 'gelf_celery'],
            'level': 'DEBUG',
            'propagate': False,  # Убираем передачу сообщений в другие обработчики
        },
    },
}
