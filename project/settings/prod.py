from .base import *

DEBUG = False
ALLOWED_HOSTS = ["account.zvwb.ru"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(pathname)s -> %(funcName)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'main': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(LOGS_DIR, 'logs', 'main.log')
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['main']
        }
    }
}