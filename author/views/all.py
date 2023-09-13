from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Recipes
from author.forms import RegisterForm, LoginAuthorForm
from author.forms.recipe_form import AuthorRecipeForm


def register_view(request):
    # O django cria cookies com um dicionario de sessão.
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(
        request=request,
        template_name='author/pages/register_author.html',
        context={
            'form': form,
            'form_action': reverse('author:register_success')
        }
    )


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')
        del (request.session['register_form_data'])
        return redirect(to='author:login')
    return redirect(to='author:register_author')


def login_view(request):
    form = LoginAuthorForm()
    return render(
        request=request,
        template_name='author/pages/login_author.html',
        context={
            'form': form,
            'form_action': reverse('author:login_success')
        }
    )


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginAuthorForm(request.POST)
    login_url = 'author:dashboard'
    
    if form.is_valid():
        authenticated_user = authenticate(request=request, username=form.cleaned_data.get(
            'username', ''), password=form.cleaned_data.get('password'))
        if authenticated_user is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)        
        else:
            messages.error(request,'Invalid credentials')
    else:    
        messages.error(request,'Error to validate form data')
        
    return redirect(login_url)

@login_required(redirect_field_name='next',login_url='author:login_author')
def logout_view(request):
    """
    Por segurança é melhor colocar logout por formulário para evitar ataque csrf
    Desta forma, conseguimos identificar de onde as requisições chegam    
    """    
    if not request.POST:
        messages.error(request,'Invalid logout request')
        redirect(to='author:login')   
    
    if request.POST.get('username') != request.user.username:
        messages.error(request,'Invalid user request')
        return redirect(reverse('author:login'))
    
    logout(request)
    messages.info(request, 'You session was terminated')
    return redirect(to='author:login')

@login_required(redirect_field_name='next',login_url='author:login')
def dashboard_view(request):
    recipes = Recipes.objects.filter(author=request.user, is_published = False)
    return render(request, 'author/pages/dashboard.html', context={
        "recipes": recipes
    })    
    
@login_required(redirect_field_name='next',login_url='author:login')
def dashboard_recipe_create(request):
    form = AuthorRecipeForm(request.POST,files=request.FILES or None)
    
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        
        messages.success(request,' Your recipe was creted with success')
        return redirect(reverse('author:dashboard_recipe_edit',args=[recipe.id]))
    return render(request, 'author/pages/dashboard_create_recipe.html', context={
        'form': form
    })