from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    tags = models.ManyToManyField('Tag', blank=True, related_name='recipes', verbose_name="Теги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"