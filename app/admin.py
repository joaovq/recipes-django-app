from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from app.models import Category,Recipes
from tag.models import Tag

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

# Se fosse uma relação sem content types ou uma relação normal
# class TagInline(admin.TabularInline):
#     model = Tag
# class TagInline(GenericStackedInline):
#     model = Tag
#     fields = 'name',
#     # Quantidades de campos que aparecem no form 
#     extra = 1
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
    # inlines = [
    #     TagInline
    # ]
    autocomplete_fields = ('tags',)
    
admin.site.register(Category,CategoryAdmin)
