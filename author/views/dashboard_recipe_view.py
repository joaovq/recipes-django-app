from typing import Any
from django import http
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from app.models import Recipes
from author.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(
        login_required(redirect_field_name='next', login_url='author:login'),
        name='dispatch'
)
class DashboardRecipeView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            # Poderia usar o get
            recipe = Recipes.objects.filter(
                author=self.request.user, is_published=False, pk=id).first()

            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, recipe, form):
        return render(self.request, 'author/pages/dashboard_recipe.html', context={
            "recipe": recipe,
            'form': form
        })
    
    def get(self, request, id=None):
        # Poderia usar o get para pegar somente uma instancia
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(request.POST or None,
                                files=request.FILES or None, instance=recipe)
        return self.render_recipe(recipe, form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(request.POST or None,
                                files=request.FILES or None, instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, ' Your recipe was saved with success')
            return redirect(reverse('author:dashboard_recipe_edit', args=[recipe.id]))
        return self.render_recipe(recipe, form)


@method_decorator(
    login_required(redirect_field_name='next', login_url='author:login'),
    name='dispatch'
)
class DashboardDeleteView(DashboardRecipeView):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Delete successfully')
        return redirect(reverse('author:dashboard'))