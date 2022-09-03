from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "https://todo-app-with-auth.herokuapp.com",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_variables('DB_NAME'),
        'USER': get_variables('DB_USER'),
        'PASSWORD': get_variables('DB_PASSWORD'),
        'HOST': get_variables('DB_HOST'),
        'PORT': get_variables('DB_PORT')
    }
}
