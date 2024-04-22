from project.settings import BASE_DIR
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
    from urllib.parse import quote_plus, urlparse
    MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')

    # Parse the MongoDB URI
    parsed_uri = urlparse(MONGODB_CONNECTION_STRING)

    # Extract host, username, password, and database name
    protocol = parsed_uri.scheme
    host = parsed_uri.hostname
    port = parsed_uri.port
    username = parsed_uri.username
    password = parsed_uri.password
    database_name = parsed_uri.path.strip('/')
    query_string = parsed_uri.query

    # If IPv6 address is present, enclose it in '[' and ']'
    if ':' in host and '[' not in host:
        host = f'[{host}]'

    # Construct a new connection string with properly escaped characters
    escaped_uri = f"{protocol}://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}/{database_name}?{query_string}" if query_string else f"{protocol}://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}/{database_name}"
    try:
        # Connect to the MongoDB database using the updated connection string
        mongoengine.connect(db=database_name, host=escaped_uri)
    except mongoengine.connection.ConnectionFailure as e:
        print(f"Cannot connect to database {database_name}: {e}")
