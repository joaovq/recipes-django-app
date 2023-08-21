from django.shortcuts import render

def home_view(request):
    return render(request=request, template_name='recipes/home.html',)

def about_view(request):
    return render(request=request, template_name='recipes/home.html',)

def contact_view(request):
    return render(request=request, template_name='recipes/home.html',)
