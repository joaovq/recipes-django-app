from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from author.forms import RegisterForm, LoginAuthorForm


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
        return redirect(to='author:login_author')
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
    login_url = 'author:login_author'
    
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
    Desta forma, coonseguimos identificar de onde as requisições chegam    
    """    
    if not request.POST:
        redirect(to='author:login_author')   
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    
    logout(request)
    messages.info(request, 'You session was terminated')
    return redirect(to='author:login_author')