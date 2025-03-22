from django import template
from women.models import *

register = template.Library()  # регистрация собственных шаблонных тегов


# декоратором превращаем функцию в тег
@register.simple_tag(name='get_cats')  # простой тег, т. к. возвращает коллекцию значений
def get_categories(filter=None):  # функция для простого тега
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


# декоратором превращаем функцию в тег
@register.inclusion_tag('women/list_categories.html')  # включащий тег, т. к. формирует html-страницу, которую возвращает
def show_categories(sort=None, cat_selected=0):  # функция для включающего тега
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}
# возвращает сформированный шаблон


# декоратором превращаем функцию в тег
@register.inclusion_tag('women/main_menu.html')  # включающий тег, т. к. формирует html-страницу, которую возвращает
def show_main_menu():  # функция для включающего тега
    return {'menu': [
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
    ]}
# возвращает сформированный шаблон




