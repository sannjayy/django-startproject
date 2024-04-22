import os


from test_app.document import get_timestamp
from mongoengine import ValidationError

class MongoEngineUtil():
    def __init__(self, *args, **kwargs):
        pass
    
    def save(self, *args, **kwargs):
        # print('Mongo Save Called')
        # model = args[0]
        # mongo_data = model(**kwargs)
        # mongo_data.save()
        
        try:
            model = args[0]
            mongo_data = model(**kwargs)
            mongo_data.created_at = get_timestamp()
            mongo_data.save()
            # print(f"Data saved successfully to {model.__name__} collection.")
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def get_mongo_connection_uri():
    ENABLE_MONGO_ENGINE = (os.environ.get('ENABLE_MONGO_ENGINE') == 'True')
    if ENABLE_MONGO_ENGINE:
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
        return {
            'success': True,
            'uri': escaped_uri,
            'database_name': database_name
        }
    else:
        return { 'success': True }