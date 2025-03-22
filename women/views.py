from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *


def index(request):
    # return HttpResponse("Страница приложения women.")

    posts = Women.objects.all()

    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0
    }

    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})


def add_page(request):
    if request.method == "POST":  # если форма уже заполнялась
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #     print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()  # если первый раз отправляют форму

    return render(request, 'women/addpage.html', {'form': form, 'title': "Добавление статьи"})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)  # встроенная функция Django

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    # post = get_object_or_404(Women, slug=post_slug)  # встроенная функция Django
    cat_id = get_object_or_404(Category, slug=cat_slug).id
    posts = Women.objects.filter(cat_id=cat_id)

    if not len(posts):
        raise Http404()

    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug
    }

    return render(request, 'women/index.html', context=context)


# def categories(request, cat_id):
#     if request.POST:
#         print(request.POST)
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat_id}</p>")
#
#
# def archive(request, year):
#     if int(year) < 2020:
#         # raise Http404()  # 404-ошибка
#         # return redirect('/')  # временный редирект (302)
#         return redirect('home', permanent=True)  # постоянный редирект (301)

    # return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
