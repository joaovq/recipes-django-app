import os

def get_env_variable(variable_name, default_value =''):
    return os.environ.get(variable_name, default_value)

def parse_element_sep_str_to_list(sep_str: str, element_separated: str = ','):
    if not sep_str or not isinstance(sep_str, str):
        return []
    return [string for string in sep_str.split(element_separated) if len(string)>0]

print(parse_element_sep_str_to_list("123, localhost"))