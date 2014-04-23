# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uxc*54zvjl^n%9t##1r+rfw&&e$fq88-k6vac8%&x8_q)qp=)_'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    #'rest_framework',
    #'rest_framework.authtoken',
    'siteup_api',
    'siteup_checker',
    'siteup_frontend',
    'django_extensions',
    'gunicorn',
    'celery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'siteup.urls'

WSGI_APPLICATION = 'siteup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'django-db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# LANGUAGE_CODE = 'es-es'
LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Make sure log folder exists
if not os.path.isdir(os.path.join(BASE_DIR, '..', 'logs')):
    os.mkdir(os.path.join(BASE_DIR, '..', 'logs'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(levelname)s - %(filename)s:%(lineno)d - %(message)s'   # %(asctime)s -
        },

        'medium': {
            'format': '%(filename)s:%(lineno)d - %(message)s'   # %(asctime)s -
        },

        'simple': {
            'format': '%(asctime)s - %(message)s'
        }
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },

        'operations_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'siteup_operations.log'),
            'formatter': 'simple',
        },

        'debug_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs', 'siteup_debug.log'),
            'formatter': 'medium'
        }
    },

    'loggers': {
        'operations': {
            'handlers': ['operations_file'],
            'level': 'DEBUG'
        },

        'debugging': {
            'handlers': ['debug_file', 'console'],
            'level': 'DEBUG'
        },

        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },

        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },

        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },

        '' : {
            'handlers' : ['console'],
            'level': 'INFO'
        },

    }
}

"""
'gunicorn.error': {
    'level': 'INFO',
    'handlers': ['logfile'],
    'propagate': True,
},
'gunicorn.access': {
    'level': 'INFO',
    'handlers': ['logfile'],
    'propagate': False,
},
'celery': {
    'handlers': ['celery'],
    'level': 'DEBUG',
},
"""

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'siteup_frontend.context_processors.baseurl',
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

BASE_URL = 'http://siteup.josetomastocino.com'

from datetime import timedelta

# Number of consecutive logs to consider a change of status
CONSECUTIVE_LOGS_FOR_FAILURE = 2

# Logs older than this will be removed by a periodic maintenance task
CHECKLOG_EXPIRATION_TIME = timedelta(days=30)

# The same for CheckStatus objects
CHECKSTATUS_EXPIRATION_TIME = timedelta(days=365)   # A year

# # Each collapse level has:
# # - ID
# # - timedelta that indicates how old logs must be to be collapsed
# # - timedelta that indicates the interval of logs to collapse

# CHECKLOG_COLLAPSE_LEVELS = (
#     (1, timedelta(hours=24), timedelta(minutes=30)), # Collapse 1-minute interval to 30-minute-interval
#     (2, timedelta(hours=7 * 24), timedelta(hours=2)) # Collapse 30-minute-interval to 2-hour-interval
# )

# In hours. Logs older than this will get first level collapsing (1 min -> 30 min)
CHECKLOG_COLLAPSE_TIME_1 = 24

# CELERY Settings
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'

# EMAIL_BACKEND
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'siteup.pfc@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['GMAIL_PASS']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'siteup.pfc@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# DJANGO TOOLBAR SETTINGS

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

def show_toolbar(request):
    if request.user and request.user.username == "jose":
        return True
    return False


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'siteup.settings.base.show_toolbar',
    # Rest of config
}