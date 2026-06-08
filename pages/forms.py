from django import forms

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