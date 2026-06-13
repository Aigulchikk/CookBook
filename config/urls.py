"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages import views
from pages.views import RegisterView, custom_logout, HomeView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    
    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    
    # Главная и детальные
    path('', HomeView.as_view(), name='home'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    
    # CRUD рецептов
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    
    # Комментарии
    path('recipe/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Статические страницы
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    #Категории
    path('category/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)