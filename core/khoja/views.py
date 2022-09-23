from django.shortcuts import render
from django.http import HttpResponse

from .models import Category, Page


def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    context = {}
    context['categories'] = categories
    return render(request, 'khoja/index.html', context)

def about(request):
    return render(request, 'khoja/about.html')

def show_category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context['pages'] =  pages
        context['category'] = category
    except Category.DoesNotExist:
        context['category'] = None
        context['pages'] = None

    return render(request, 'khoja/category.html', context)
