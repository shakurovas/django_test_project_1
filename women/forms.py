from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women
        # fields = '__all__'  # все поля, кроме тех что заполняются автоматически
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
    # title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))  # названия атрибутов желательно чтоб совпадали с названиями полей модели
    # slug = forms.SlugField(max_length=255, label="URL")
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Содержание")
    # is_published = forms.BooleanField(label="Опубликовать?", required=False, initial=True)
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана")

    def clean_title(self):  # название метода должно начинаться с clean и дальше - проверяемое поле
        title = self.cleaned_data['title']  # cleaned_data - встроенная коллекция экземпляра класса формы
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")

        return title

