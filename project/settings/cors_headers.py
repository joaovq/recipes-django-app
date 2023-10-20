from utils.environment import get_env_variable, parse_element_sep_str_to_list


CORS_ALLOWED_ORIGINS = parse_element_sep_str_to_list(get_env_variable('CORS_ALLOWED_ORIGINS'))

# docs https://pypi.org/project/django-cors-headers/