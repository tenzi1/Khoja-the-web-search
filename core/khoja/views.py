from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm

#counter implementing session data
def visitor_cookie_handler(request):
    visits = request.session.get('visits', 1)
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] =  str(datetime.now())
    else:
        request.session['last_visit'] =  last_visit_cookie
    
    request.session['visits'] =  visits

#counter handler with Client site cookie
# def visitor_cookie_handler(request, response):
#     visits = int(request.COOKIES.get('visits', 1))
#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

#     if (datetime.now() - last_visit_time).days > 0:
#         visits += 1
#         response.set_cookie('last_visit', str(datetime.now()))
#     else:
#         response.set_cookie('last_visit', last_visit_cookie)
    
#     response.set_cookie('visits', visits)





#User registration view
def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('khoja:index'))
    else:
        form = UserForm()
    return render(request, 'khoja/user_register.html', {'form': form })
# Create User and User profile
def register(request):
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            # return redirect(reverse('khoja:index'))
        else:
            print(form.errors, profile_form.errors)
    else:
        form = UserForm()
        profile_form = UserProfileForm()
    context = {
            'form':form,
            'profile_form':profile_form,
            'registered':registered
        }
    return render(request, 'khoja/register.html', context)
        
# View for User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('khoja:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid Credentials supplied !!!')
    else:
        return render(request, 'khoja/login.html')

#View for logging out user
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('khoja:index'))



def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    context = {}
    context['categories'] = categories

    #setting up test cookie
    request.session.set_test_cookie()
    response =  render(request, 'khoja/index.html', context)

    #call helper function to handle the cookies using client site cookie
    # visitor_cookie_handler(request, response)
    #call helper function to handle the cookies using session data
    visitor_cookie_handler(request)
    return response
    
def about(request):

    #checking test cookie
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED....")
    request.session.delete_test_cookie()
    return render(request, 'khoja/about.html')

#Add Category
@login_required
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

    