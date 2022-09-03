from core.settings.production import CORS_ALLOWED_ORIGINS


from .base import *
DEBUG=True
CORS_ALLOWED_ORIGINS=[
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}