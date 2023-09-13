from django.contrib import admin

from app.models import Category,Recipes

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id','title', 'created_at', 'is_published', 'category'
    list_display_links = 'title', 'created_at'
    search_fields = 'id', 'title', 'description', 'slug'
    list_filter='category', 'author', 'is_published', 'preparation_steps_is_html'
    list_per_page = 10
    list_editable = ['is_published']
    ordering = '-id',
    prepopulated_fields = {'slug': ('title',) }
admin.site.register(Category,CategoryAdmin)
