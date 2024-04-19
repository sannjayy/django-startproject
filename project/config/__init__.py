import os

from .defaults import *
from .libs.database import *
from .info import *



if os.environ.get('ENABLE_DRF', 'False').lower() == 'true':
    from .cors import *
    from .libs.drf import *

if os.environ.get('ENABLE_REDIS', 'False').lower() == 'true':
    from .libs.redis import *
from .libs.smtp import *
if os.environ.get('ENABLE_SMS_GATEWAY', 'False').lower() == 'true':
    from .libs.sms import *
if os.environ.get('ENABLE_LOGGER', 'False').lower() == 'true':
    from .libs.logger import *
if os.environ.get('ENABLE_AWS_S3_STORAGE', 'False').lower() == 'true':
    from .libs.storage import *
from .links import *
from .email import *
if os.environ['ENABLE_CRON_JOBS'] == 'True':
    from .cronjobs import *
