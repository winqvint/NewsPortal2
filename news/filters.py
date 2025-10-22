from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from django import forms
from .models import Post, Author

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по заголовку'})
    )

    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_from = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата от',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_from']

