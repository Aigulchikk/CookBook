from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipe
from .forms import FeedbackForm, RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print("=" * 50)
            print("НОВОЕ СООБЩЕНИЕ ИЗ ФОРМЫ ОБРАТНОЙ СВЯЗИ")
            print(f"Тема: {form.cleaned_data['subject']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Сообщение: {form.cleaned_data['message']}")
            print("=" * 50)
            
            messages.success(request, '✅ Ваше сообщение отправлено! Спасибо!')
            return redirect('home')
    else:
        form = FeedbackForm(initial={'email': 'cookbook@example.com'})
    
    return render(request, 'pages/contact.html', {'form': form})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'pages/recipe_form.html', {'form': form, 'title': '➕ Добавление рецепта'})

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои рецепты!')
        return redirect('recipe_detail', recipe_id=recipe.id)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'pages/recipe_form.html', {'form': form, 'title': '✏️ Редактирование рецепта'})

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def custom_logout(request):
    logout(request)
    return redirect('home')