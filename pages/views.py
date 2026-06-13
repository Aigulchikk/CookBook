from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Recipe, Tag
from .forms import RecipeForm, CommentForm, FeedbackForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm


def about(request):
    context = {
        'site_name': 'CookBook',
        'mission': 'Мы создаём удобное пространство для обмена кулинарным опытом и рецептами.',
        'audience': 'Для тех, кто любит готовить и хочет делиться своими рецептами с миром.',
        'year': 2026,
    }
    return render(request, 'pages/about.html', context)

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
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, '✅ Ваш комментарий добавлен!')
        else:
            messages.error(request, '❌ Ошибка при добавлении комментария.')
    
    return redirect('recipe_detail', pk=pk)

class HomeView(ListView):
    model = Recipe
    template_name = 'pages/index.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_text'] = 'Добро пожаловать в CookBook'
        context['description'] = 'Твой личный сервис для создания и хранения лучших рецептов.'
        context['button_text'] = 'Начать готовить'
        context['year'] = 2026
        return context
    
class CategoryView(ListView):
    model = Recipe
    template_name = 'pages/index.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug == 'salad':
            return queryset.filter(category='salad')
        elif category_slug == 'soup':
            return queryset.filter(category='soup')
        elif category_slug == 'main':
            return queryset.filter(category='main')
        elif category_slug == 'dessert':
            return queryset.filter(category='dessert')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_text'] = 'Добро пожаловать в CookBook'
        context['description'] = 'Твой личный сервис для создания и хранения лучших рецептов.'
        context['button_text'] = 'Начать готовить'
        context['year'] = 2026
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'pages/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'pages/recipe_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '✅ Рецепт успешно создан!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '➕ Добавление рецепта'
        return context

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'pages/recipe_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        messages.success(self.request, '✅ Рецепт успешно обновлён!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '✏️ Редактирование рецепта'
        return context

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'pages/recipe_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '🗑️ Рецепт успешно удалён!')
        return super().delete(request, *args, **kwargs)
    
class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def custom_logout(request):
    logout(request)
    return redirect('home')