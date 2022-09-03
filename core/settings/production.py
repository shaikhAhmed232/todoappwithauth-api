from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "https://todo-app-with-auth.herokuapp.com",
    "http://localhost:3000",
]

DATABASES = {
    'default': {
        'ENGINE': get_variables('DATABASE_URL'),
        'NAME': get_variables('DB_NAME'),
        'USER': get_variables('DB_USER'),
        'PASSWORD': get_variables('DB_PASSWORD'),
        'HOST': get_variables('DB_HOST'),
        'PORT': get_variables('DB_PORT')
    }
}
