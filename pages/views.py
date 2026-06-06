from django.shortcuts import render

def index(request):
    context = {
        'welcome_text': 'Добро пожаловать в CookBook',
        'description': 'Твой личный сервис для создания и хранения лучших рецептов.',
        'button_text': 'Начать готовить',
        'year': 2026,
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