import datetime


def make_recipe():
    return {
        'id':1,
        'name': "gdfgfdssdfgs",
        'description': "gdfgdf",
        'num_preparations': 457,
        'preparation_unit': 'Minutos',
        'num_servings': 897,
        'serving_unit': 'Porção',
        'preparation_steps': "Lodsfhdshfousdhgiofh",
        'created_at': datetime.datetime.now(),
        'author': {
            'first_name': "João ",
            'last_name': "Vitor",
        },
        'category': {
            'name': "Almoço"
        },
        'cover': {
            'url': 'https://loremflickr.com/550/400/food,cook',
        }
    }