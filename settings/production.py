from settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '/cloudsql/gymder:europe-west3:gymder',
        'NAME': os.environ.get('DB_NAME', 'gymder'),
        'USER': os.environ.get('DB_USERNAME', 'gymder'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password')
    }
}

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
