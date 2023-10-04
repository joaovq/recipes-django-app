from django.contrib import admin
from author import models

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...