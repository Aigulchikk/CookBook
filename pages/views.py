from django.shortcuts import render, get_object_or_404
from .models import Recipe

def index(request, category_slug=None):
    recipes = Recipe.objects.all().order_by('-created_at')
    current_category = None

    if category_slug:
        if category_slug == 'salad':
            recipes = recipes.filter(category='salad')
            current_category = '🥗 Салаты'
        elif category_slug == 'soup':
            recipes = recipes.filter(category='soup')
            current_category = '🍲 Супы'
        elif category_slug == 'main':
            recipes = recipes.filter(category='main')
            current_category = '🍝 Горячее'
        elif category_slug == 'dessert':
            recipes = recipes.filter(category='dessert')
            current_category = '🍰 Десерты'

    context = {
        'welcome_text': 'Добро пожаловать в CookBook',
        'description': 'Твой личный сервис для создания и хранения лучших рецептов.',
        'button_text': 'Начать готовить',
        'year': 2026,
        'recipes': recipes,
        'current_category': current_category,
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