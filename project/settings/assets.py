# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

from .environment import BASE_DIR, DATA_DIR


STATIC_URL = 'static/'

STATICFILES_DIRS = [
   BASE_DIR / "base_static"
]
STATIC_ROOT = DATA_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = DATA_DIR / 'media'