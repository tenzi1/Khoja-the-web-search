from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .models import Category, Page
from .forms import CategoryForm, PageForm

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    context = {}
    context['categories'] = categories
    return render(request, 'khoja/index.html', context)

def about(request):
    return render(request, 'khoja/about.html')

#Add Category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/khoja/')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'khoja/add_category.html', {'form':form})

#Display Category
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

#Add Page
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/khoja/')

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('khoja:add_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.erros)
    
    context = {
        'form': form,
        'category': category
    }

    return render(request, 'khoja/add_page.html', context)

    