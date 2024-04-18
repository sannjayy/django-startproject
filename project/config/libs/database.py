from project.settings.base import BASE_DIR
import os

# DATABASE CONFIG
import os

ENABLE_DB = os.environ.get('ENABLE_DB', 'False').lower() == 'true'
DATABASE_TYPE = os.environ.get('DB_TYPE', 'sqlite').lower()
DATABASE_CONFIGS = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            "init_command": "SET default_storage_engine=INNODB",
        }
    },
}

DATABASES = {
    'default': DATABASE_CONFIGS.get(DATABASE_TYPE, DATABASE_CONFIGS['sqlite'])} if ENABLE_DB else {'default': DATABASE_CONFIGS['sqlite']}


    
 # MONGO CONFIG
ENABLE_MONGO_ENGINE = (os.environ.get('ENABLE_MONGO_ENGINE') == 'True')
if ENABLE_MONGO_ENGINE:
    import mongoengine
    from urllib.parse import quote_plus

    MONGO_USERNAME = quote_plus(os.environ.get('MONGO_USERNAME'))
    MONGO_PASSWORD = quote_plus(os.environ.get('MONGO_PASSWORD'))
    MONGO_HOST = os.environ.get('MONGO_HOST_URI')
    MONGO_HOST_URI = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}'
    mongoengine.connect(db=os.environ.get('MONGO_DB_NAME'), host=MONGO_HOST_URI)