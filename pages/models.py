from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    class Category(models.TextChoices):
        SALAD = 'salad', '🥗 Салат'
        SOUP = 'soup', '🍲 Суп'
        MAIN = 'main', '🍝 Горячее'
        DESSERT = 'dessert', '🍰 Десерт'

    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    instructions = models.TextField(verbose_name="Инструкция приготовления")
    cooking_time = models.IntegerField(verbose_name="Время приготовления (мин)", default=30)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.MAIN, verbose_name="Категория")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL изображения")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"