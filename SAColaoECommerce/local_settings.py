import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('db.sqlite3')),
    }   
}

DEBUG = True
