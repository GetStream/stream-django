STREAM_API_KEY = 'test_key'
STREAM_API_SECRET = '123'
STREAM_LOCATION = 'us-east'

SECRET_KEY = 'insecure'

AUTH_USER_MODEL = 'auth.User'

INSTALLED_APPS = [
    'test_app',
    'stream_django',
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'simple_test_db'
    }
}

MIDDLEWARE_CLASSES = []
