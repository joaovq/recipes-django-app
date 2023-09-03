from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from app.models import Category, Recipes
from django.db.models import Q
from utils.pagination import make_pagination
import os
from django.contrib import messages

PER_PAGE = os.environ.get('PER_PAGE', 6)

def home_view(request):
    recipes = Recipes.objects.filter(is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request=request,queryset=recipes, per_page=PER_PAGE)
    return render(
        request=request,
        template_name='recipes/pages/home.html',
        context={
            'recipes': page_obj,
            'pagination_range':pagination_range,
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
    recipes = get_list_or_404(Recipes.objects.filter(
        category__id=category_id, is_published=True))
    category = get_object_or_404(Category, pk=category_id)
    return render(request=request, template_name='recipes/pages/home.html', context={
        'recipes': recipes,
        'is_detail_page': False,
        'category': category,
        'title': f"{category.categoryName} | Recipes"
    })


def search_recipes_view(request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404
    recipes = Recipes.objects.filter(
        Q(
          Q(title__icontains= search_term) |
          Q(description__icontains= search_term)
        ),
        is_published=True
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request=request,queryset=recipes, per_page=PER_PAGE)
    return render(request=request, template_name='recipes/pages/recipes_search.html', context={
        'recipes': page_obj,
        'is_detail_page': False,
        'title': f"Search Results for \"{search_term}\"",
        'search_term': search_term,
        'pagination_range':pagination_range,
        'additional_url_query':f'&search={search_term}'  
    })
