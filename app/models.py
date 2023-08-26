from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    categoryName = models.TextField(max_length=30)
    
    def __str__(self) -> str:
        return f"{self.id}-{self.categoryName}"
    
# Create your models here.
class Recipes(models.Model):
    title = models.CharField(max_length=60, default='')
    description = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    num_preparations = models.IntegerField()
    num_servings = models.IntegerField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65, default='')
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    servings_unit = models.TextField(max_length=65)
    created_at = models.DateTimeField(auto_created=True,)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True, default=None) 
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True) 
    cover_image = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    def __str__(self) -> str:
        return self.name
    
