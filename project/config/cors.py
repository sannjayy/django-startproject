import os

# Get the environment name from the environment variables, defaulting to 'dev' if not set
ENV_NAME = os.environ.get("ENV_NAME", "dev")

# Set CORS settings based on the environment
if ENV_NAME == 'prod':
    # PROD CORS SETTINGS
    CORS_ALLOWED_ORIGINS = [host.strip() for host in os.getenv('CORS_ALLOWED_ORIGINS').split(',')]
else:
    # DEV CORS SETTINGS
    CORS_ALLOW_ALL_ORIGINS = True