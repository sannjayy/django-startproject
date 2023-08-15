from .base import *
from .config.lib import *

ENV_NAME = os.environ.get("ENV_NAME")
if ENV_NAME == 'prod':
    print('--> PRODUCTION MODE <--')
    from .prod import *        

elif ENV_NAME == 'stagging':
    print('--> STAGING MODE <--')
    from .staging import *

else:
    print('--> DEV MODE <--')
    from .dev import *