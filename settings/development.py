from settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST_LOCAL', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT_LOCAL', '5432'),
        'NAME': os.environ.get('DB_NAME_LOCAL', 'gymder'),
        'USER': os.environ.get('DB_USERNAME_LOCAL', 'gymder'),
        'PASSWORD': os.environ.get('DB_PASSWORD_LOCAL', 'password')
    }
}

STATIC_URL = '/static/'

# STATIC_ROOT = 'static'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
