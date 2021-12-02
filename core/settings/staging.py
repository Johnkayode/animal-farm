from .base import *


SECRET_KEY = 'django-insecure-q&n%+61uf0uk^kqq&)ul(+621#s(5ly=_6*&q#c_ix3meh2jn1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




ALLOWED_HOSTS = ["*"]