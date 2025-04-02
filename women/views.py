from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women  # выбирает записи из модели и пытаться вывести их списком
    template_name = 'women/index.html'  # по умолчанию <имя приложения>/<имя модели>_list.html
    context_object_name = 'posts'  # по умолчанию "object_list"
    # extra_context = {'title': "Главная страница"}  # так можно передавать только неизменяемые значения

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # берём текущий конткест для того, чтобы не перезатереть posts
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # что выбирать из модели
        return Women.objects.filter(is_published=True).select_related('cat')  # select_related('cat') - "жадный" SQL-запрос, чтобы он не выполнялся повторно

# def index(request):
#     # return HttpResponse("Страница приложения women.")
#
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#
#     return render(request, 'women/index.html', context=context)


def about(request):
    cats = Category.objects.annotate(Count('women'))
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)
    return render(request, 'women/about.html', {'cats': cats, 'title': 'О сайте', 'menu': user_menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')  # reverse_lazy выполняет построение маршрута только в момент, когда он понадобится
    # print('bloo: ', form_class)
    login_url = reverse_lazy('home')
    raise_exception = True  # чтобы генерировалась страница 403 без авторизации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# def add_page(request):
#     if request.method == "POST":  # если форма уже заполнялась
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #     print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()  # если первый раз отправляют форму
#
#     return render(request, 'women/addpage.html', {'form': form, 'title': "Добавление статьи"})


# def contact(request):
#     return HttpResponse("Обратная связь")


# def contact(request):
#     if request.method == "POST":  # если форма уже заполнялась
#         form = ContactForm(request.POST, request.FILES)
#         if form.is_valid():
#             #     print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = ContactForm()  # если первый раз отправляют форму
#
#     return render(request, 'women/contact.html', {'form': form, 'title': "Обратная связь"})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # если форма корректно заполнена
        print(form.cleaned_data)
        form.save()
        return redirect('home')



# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # как будет называться slug/id (pk_url_kwarg) в маршруте
    context_object_name = 'post'  # в какую переменную будут помещаться данные, взятые из модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)  # встроенная функция Django
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # если будет не найдено, будет выводиться 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Категория - " + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')  # select_related('cat') - "жадный" SQL-запрос, чтобы он не выполнялся повторно


# def show_category(request, cat_slug):
#     # post = get_object_or_404(Women, slug=post_slug)  # встроенная функция Django
#     cat_id = get_object_or_404(Category, slug=cat_slug).id
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     if not len(posts):
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug
#     }
#
#     return render(request, 'women/index.html', context=context)


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


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # вызывается при успешной регистрации
        user = form.save()  # сохраняем данные пользователя в таблицу
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):  # standard method name
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
