from project.settings import BASE_DIR
import os

# DATABASE CONFIG
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
            'charset': 'utf8mb4',
            # "init_command": "SET default_storage_engine=INNODB",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}

DATABASES = {
    'default': DATABASE_CONFIGS.get(DATABASE_TYPE, DATABASE_CONFIGS['sqlite'])} if ENABLE_DB else {'default': DATABASE_CONFIGS['sqlite']}


    
 # MONGO CONFIG
ENABLE_MONGO_ENGINE = (os.environ.get('ENABLE_MONGO_ENGINE') == 'True')
if ENABLE_MONGO_ENGINE:
    import mongoengine
    from utils.mongo import get_mongo_connection_uri
    fetch_mongo = get_mongo_connection_uri()
    if fetch_mongo.get('success'):
        
        try:
            # Connect to the MongoDB database using the updated connection string
            mongoengine.connect(host=fetch_mongo.get('uri'))
        except mongoengine.connection.ConnectionFailure as e:
            print(f"Cannot connect to database {fetch_mongo.get('database_name')}: {e}")
