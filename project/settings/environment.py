# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
from pathlib import Path
from utils.environment import get_env_variable, parse_element_sep_str_to_list
if os.environ.get('DEBUG', None) is None:
    from dotenv import load_dotenv
    load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR.parent/'data'/'web'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =True if os.environ.get('DEBUG', True) == '1' else False

ALLOWED_HOSTS: list[str] = parse_element_sep_str_to_list(get_env_variable('ALLOWED_HOSTS', '*'))

CSRF_TRUSTED_ORIGINS: list[str] = parse_element_sep_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS'))

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]