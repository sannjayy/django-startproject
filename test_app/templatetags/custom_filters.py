from django import template
import re

register = template.Library()

@register.filter
def hide_mongo_password(value, type='uri'):
    try:
        from urllib.parse import urlparse
        # Parse the MongoDB URI
        parsed_uri = urlparse(value)
        # Extract host, username, password, and database name
        protocol = parsed_uri.scheme
        hostname = parsed_uri.hostname
        port = parsed_uri.port
        username = parsed_uri.username
        password = parsed_uri.password
        database_name = parsed_uri.path.strip('/')
        mongodb_uri = f"{protocol}://{username}:{'*' * len(password)}@{hostname}:{port}/{database_name}"
        if type == 'database_name':
            return database_name
        return mongodb_uri
    except Exception as e:
        pass
