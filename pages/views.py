from django.shortcuts import render, get_object_or_404
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    context = {
        'welcome_text': 'Добро пожаловать в CookBook',
        'description': 'Твой личный сервис для создания и хранения лучших рецептов.',
        'button_text': 'Начать готовить',
        'year': 2026,
        'recipes': recipes,
    }
    return render(request, 'pages/index.html', context)

def about(request):
    context = {
        'site_name': 'CookBook',
        'mission': 'Мы создаём удобное пространство для обмена кулинарным опытом и рецептами.',
        'audience': 'Для тех, кто любит готовить и хочет делиться своими рецептами с миром.',
        'year': 2026,
    }
    return render(request, 'pages/about.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'pages/recipe_detail.html', context)