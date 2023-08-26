from datetime import date
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from app.models import Category, Recipes


def home_view(request):
    recipes = Recipes.objects.filter(is_published=True).order_by('-id')
    return render(
        request=request,
        template_name='recipes/pages/home.html',
        context={
            'recipes': recipes,
            'is_detail_page': False
        }
    )


def recipe_details_view(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipes, pk=recipe_id, is_published=True)
        return render(request=request, template_name='recipes/pages/home.html', context={
            'recipes': [recipe],
            'is_detail_page': True
        })
    except Http404 as error:
        print(error)
        return render(
            request,
            template_name='global/error_404_template.html',
            context={
                'error': error,
            },
            status=404
        )


def categories_recipes_view(request, category_id):
    recipes = get_list_or_404(Recipes.objects.filter(category__id=category_id, is_published=True))
    category = get_object_or_404(Category,pk=category_id)
    return render(request=request, template_name='recipes/pages/home.html', context={
        'recipes': recipes,
        'is_detail_page': False,
        'category': category,
        'title': f"{category.categoryName} | Recipes"
    })
