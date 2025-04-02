from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):  # для отображения элементов модели Women в списке в админке
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # поля, которые будут выводиться в таблице элементов в админке
    list_display_links = ('id', 'title')  # поля, которые будут ссылками на элементы
    search_fields = ('title', 'content')  # поля, по которым будет осуществляться поиск, обязательно нужна запятая, чтобы считалось кортежем, а не строкой в скобках
    list_editable = ('is_published',)  # поля, которые можно будет изменять прямо в таблице с элементами в админке
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")  # mark_safe - не экранировать теги

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):  # для отображения элементов модели Category в списке в админке
    list_display = ('id', 'name')  # поля, которые будут выводиться в таблице элементов в админке
    list_display_links = ('id', 'name')  # поля, которые будут ссылками на элементы
    search_fields = ('name',)  # поля, по которым будет осуществляться поиск, обязательно нужна запятая, чтобы считалось кортежем, а не строкой в скобках
    prepopulated_fields = {"slug": ("name",)}


class ContactAdmin(admin.ModelAdmin):  # для отображения элементов модели Contact в списке в админке
    list_display = ('id', 'name', 'email', 'text')  # поля, которые будут выводиться в таблице элементов в админке
    list_display_links = ('id', 'name', 'text')  # поля, которые будут ссылками на элементы
    search_fields = ('name', 'text')  # поля, по которым будет осуществляться поиск, обязательно нужна запятая, чтобы считалось кортежем, а не строкой в скобках


admin.site.register(Women, WomenAdmin)  # регистрируем модель Women для админ-панели
admin.site.register(Category, CategoryAdmin)  # регистрируем модель Category для админ-панели
admin.site.register(Contact, ContactAdmin)  # регистрируем модель Category для админ-панели

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах'
