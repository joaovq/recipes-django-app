# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

import os

from .environment import BASE_DIR


LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Bahia'

USE_I18N = True

USE_TZ = True

LOCALE_PATH = [
    os.path.join(BASE_DIR, "locale"),
]