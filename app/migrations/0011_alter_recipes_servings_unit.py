# Generated by Django 4.2.4 on 2023-10-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_recipes_num_preparations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='servings_unit',
            field=models.CharField(blank=True, default='dd', max_length=65),
        ),
    ]
