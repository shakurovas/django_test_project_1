from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):  # для отображения элементов модели Women в списке в админке
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # поля, которые будут выводиться в таблице элементов в админке
    list_display_links = ('id', 'title')  # поля, которые будут ссылками на элементы
    search_fields = ('title', 'content')  # поля, по которым будет осуществляться поиск, обязательно нужна запятая, чтобы считалось кортежем, а не строкой в скобках
    list_editable = ('is_published',)  # поля, которые можно будет изменять прямо в таблице с элементами в админке
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):  # для отображения элементов модели Category в списке в админке
    list_display = ('id', 'name')  # поля, которые будут выводиться в таблице элементов в админке
    list_display_links = ('id', 'name')  # поля, которые будут ссылками на элементы
    search_fields = ('name',)  # поля, по которым будет осуществляться поиск, обязательно нужна запятая, чтобы считалось кортежем, а не строкой в скобках
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Women, WomenAdmin)  # регистрируем модель Women для админ-панели
admin.site.register(Category, CategoryAdmin)  # регистрируем модель Category для админ-панели

