import datetime

from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    now = datetime.datetime.now()
    posts = (Post.objects
             .select_related('category')
             .select_related('location')
             .select_related('author')
             .filter(
                 pub_date__lte=now,
                 is_published=True,
                 category__is_published=True)
             .order_by('-pub_date')[:5])
    context = {
        'post_list': posts
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    now = datetime.datetime.now()
    try:
        post = (Post.objects
                .select_related('category')
                .select_related('location')
                .select_related('author')
                .get(
                    pk=post_id,
                    is_published=True,
                    category__is_published=True,
                    pub_date__lte=now))
        context = {'post': post}
        return render(request, template, context)
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h1 style='text-align: center;"
                                    "margin-top: 10%;"
                                    "font-size: 4rem;'>"
                                    "Такого поста нет :(</h1>")


def category_posts(request, category_slug):
    template = 'blog/category.html'
    now = datetime.datetime.now()
    try:
        category = Category.objects.get(slug=category_slug, is_published=True)
        category_posts = (Post.objects
                          .select_related('category')
                          .select_related('location')
                          .select_related('author')
                          .filter(
                              category__slug=category_slug,
                              is_published=True,
                              pub_date__lte=now))
        context = {
            'category': category.title,
            'post_list': category_posts
        }
        return render(request, template, context)
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h1 style='text-align: center;"
                                    "margin-top: 10%;"
                                    "font-size: 4rem;'>"
                                    "Такой категории постов нет :(</h1>")
