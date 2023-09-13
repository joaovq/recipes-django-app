def is_positive_number(string):
    try:
        number = float(string)    
    except ValueError:
        return False
    return number > 0