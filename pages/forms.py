from django import forms
from .models import Recipe

class FeedbackForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Вопрос по рецепту'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишите ваше сообщение здесь...'})
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'cooking_time', 'category', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }