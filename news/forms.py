from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Введите содержание'
            }),
            'categories': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'categories': 'Категории',
        }