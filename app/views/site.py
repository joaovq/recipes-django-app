from typing import Any
from django import http
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from app.models import Category, Recipes
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from tag.models import Tag
from utils.pagination import make_pagination, PER_PAGES
from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict
from django.db.models.aggregates import Count
from django.utils import translation
from django.utils.translation import gettext_lazy as _

PER_PAGE = PER_PAGES


class RecipeListViewBase(ListView):
    model = Recipes
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.filter(
            is_published=True
        )
        # Faz um join nas fk's (Melhora bastante a performance)
        qs = qs.select_related('author', 'category','author__profile')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request, queryset=context.get('recipes'), per_page=PER_PAGE)
        count_recipes = Recipes.objects.aggregate(Count('id'))
        html_language = translation.get_language()
        context.update(
            {
                'recipes': page_obj, 'pagination_range': pagination_range,
                "number_recipes": count_recipes['id__count'],
                'html_language': html_language
            }
        )
        return context


class RecipeHomeView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeHomeViewApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> JsonResponse:
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()
        return JsonResponse(list(recipes_list), safe=False)


class RecipeCategoryRecipeView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        # annotate cria novos campos na query set
        query_set = query_set.filter(
            category__id=category_id, is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(" ( "),
                F('author__username'), Value(' ) '),
            )
        )
        if not query_set:
            raise Http404()
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context.get('recipes')[0].category
        context.update(
            {
                'is_detail_page': False,
                'category': category,
                'title': f"{category.categoryName} | Recipes"
            }
        )
        return context


class RecipeSearchView(RecipeListViewBase):
    template_name = 'recipes/pages/recipes_search.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('search', '').strip()
        if not search_term:
            raise Http404
        query_set = query_set.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        ).order_by('-id')
        # .values() Para pegar so os campos necessários retornando um dicionario
        # .only() Para pegar so os campos necessários retornando objetos da entidade
        # .defer() Para pegar todos os campos, menos o selecionado
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request, queryset=context.get('recipes'), per_page=PER_PAGE)
        search_term = self.request.GET.get('search', '')
        context.update(
            {
                'recipes': page_obj,
                'is_detail_page': False,
                'title': f"Search Results for \"{search_term}\"",
                'search_term': search_term,
                'pagination_range': pagination_range,
                'additional_url_query': f'&search={search_term}'
            }
        )
        return context


class RecipeDetailsView(DetailView):
    model = Recipes
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    pk_url_kwarg = 'recipe_id'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True
        )
        if not query_set:
            raise Http404()
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Não precisa passar novamente o recipes, faço isso porque é uma lista
        context.update(
            {
                'recipes': [context.get('recipes')],
                'is_detail_page': True
            }
        )
        return context


class RecipeDetailsViewApi(RecipeDetailsView):
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any):
        recipe = self.get_context_data()['recipes'][0]
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover_image'):
            recipe_dict.update({
                "cover_image": self.request.build_absolute_uri + recipe_dict.get('cover_image').url
            })
        else:
            recipe_dict['cover_image'] = ''

        del (recipe_dict['is_published'])
        del (recipe_dict['preparation_steps_is_html'])

        return JsonResponse(
            recipe_dict,
            safe=False
        )


# Tag view

class RecipeTagView(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('search', '').strip()
        if not search_term:
            raise Http404
        query_set = query_set.filter(
            tags__slug = self.kwargs.get('slug',''),
            is_published=True
        ).order_by('-id')
        query_set.prefetch_related('tags')
        # .values() Para pegar so os campos necessários retornando um dicionario
        # .only() Para pegar so os campos necessários retornando objetos da entidade
        # .defer() Para pegar todos os campos, menos o selecionado
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request, queryset=context.get('recipes'), per_page=PER_PAGE)
        page_title = Tag.objects.filter(slug = self.kwargs.get('slug',''))
        if not page_title:
            page_title = 'No Recipes found.'
        page_title = f'{page_title} - Tag |'
        context.update(
            {
                'is_detail_page': False,
                'title': f"Search Results f{page_title}\"",
                'pagination_range': pagination_range
            }
        )
        return context
