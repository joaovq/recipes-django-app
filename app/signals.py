from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import os
from app.models import Recipes

def delete_cover(recipe: Recipes):
    try:
        os.remove(recipe.cover_image.path)
    except (ValueError, FileNotFoundError) as e:
        ...
@receiver(pre_save, sender=Recipes)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipes.objects.filter(pk=instance.pk).first()
    
    if not old_instance:
        return
    
    is_new_cover = instance.cover_image != old_instance.cover_image
    if old_instance or is_new_cover:
        delete_cover(old_instance)
            
@receiver(pre_delete, sender=Recipes)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipes.objects.get(pk=instance.pk)
    delete_cover(old_instance)