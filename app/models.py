from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify 
from django.contrib.contenttypes.fields import GenericRelation 
from tag.models import Tag
class Category(models.Model):
    categoryName = models.CharField(max_length=65)
    
    def __str__(self) -> str:
        return self.categoryName
    
# Podemos criar o proprio manager (objects) 
class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published = True
        )
    
    
class Recipes(models.Model):
    objects = RecipeManager()
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
    servings_unit = models.CharField(max_length=65)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True, default=None) 
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True) 
    cover_image = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    tags = models.ManyToManyField(to=Tag)
    def __str__(self) -> str:
        return self.title
    
    # Um atalho para o reverse do url
    def get_absolute_url(self):
        return reverse("app:recipe_details", kwargs={"recipe_id": self.id})
    
    # Adicionando uma slug
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = f'{slugify(self.title)}'
            
        return super().save(*args, **kwargs)
    
    def clean(self) -> None:
        error_messages = defaultdict(list)
        recipe_from_db = Recipes.objects.filter(title__iexact=self.title).first()
        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipe with same title'
                )
        if error_messages:
            raise ValidationError(error_messages)
        return super().clean()