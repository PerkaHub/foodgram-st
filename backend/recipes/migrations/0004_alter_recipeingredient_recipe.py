# Generated by Django 4.2.21 on 2025-05-13 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_recipeshortlink"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredients_items",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
    ]
