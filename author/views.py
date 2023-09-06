from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages

from author.forms import RegisterForm

# Create your views here.

def register_view(request):
    # O django cria cookies com um dicionario de sessão. 
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(
        request=request,
        template_name='author/pages/register_author.html',
        context= {
            'form': form
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
        del(request.session['register_form_data'])
    return redirect(to='author:register_author')       