from settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'NAME': os.environ.get('DB_NAME', 'gymder'),
        'USER': os.environ.get('DB_USERNAME', 'gymder'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password')
    }
}


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
