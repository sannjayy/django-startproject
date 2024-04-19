import os
from .base import *
ENV_NAME = os.environ.get("ENV_NAME", "dev")

if ENV_NAME == 'prod':
    from .prod import *
elif ENV_NAME == 'stagging':
    from .staging import *
else:
    from .dev import *