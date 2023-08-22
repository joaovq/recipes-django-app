from django.contrib import admin

from app.models import Category,Recipes

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category,CategoryAdmin)
