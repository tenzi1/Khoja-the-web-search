from datetime import datetime
from typing import Type
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from khoja.serpapi_search import run_query

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .helper import get_category_list
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





# User authentication using custom views
# # Create User and User profile
# def register(request):
#     registered = False
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if form.is_valid and profile_form.is_valid():
#             user = form.save()
#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#             # return redirect(reverse('khoja:index'))
#         else:
#             print(form.errors, profile_form.errors)
#     else:
#         form = UserForm()
#         profile_form = UserProfileForm()
#     context = {
#             'form':form,
#             'profile_form':profile_form,
#             'registered':registered
#         }
#     return render(request, 'khoja/register.html', context)
        
# # View for User Login
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
    
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('khoja:index'))
#             else:
#                 return HttpResponse('Your account is disabled.')
#         else:
#             return HttpResponse('Invalid Credentials supplied !!!')
#     else:
#         return render(request, 'khoja/login.html')

# #View for logging out user
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('khoja:index'))



def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context = {}
    context['categories'] = categories
    context['pages'] = pages

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
        pages = Page.objects.filter(category=category).order_by('-views')
        context['pages'] =  pages
        context['category'] = category
    except Category.DoesNotExist:
        context['category'] = None
        context['pages'] = None

    #implementing search functionality
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            result_list = run_query(query)
            context['result_list'] = result_list
            context['query'] = query
    else:
        context['result_list'] = None
    


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

                return redirect(reverse('khoja:add_category'))
        else:
            print(form.errors)
    
    context = {
        'form': form,
        'category': category
    }

    return render(request, 'khoja/add_page.html', context)


# view implementing search functionality
# def search(request):
#     result_list = []
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             result_list = run_query(query)
#         context = {
#             'result_list':result_list, 'query':query
#         } 
#     else:
#         context = {
#                 'result_list':result_list,
#         }
#     return render(request, 'khoja/search.html', context)


#view implementing click count functionality
def goto_url(request, page_id):
    try:
        page = Page.objects.get(pk=page_id)
    except Page.DoesNotExist:
        return redirect(reverse('index'))
    page.views = page.views + 1
    page.save()
    return redirect(page.url)
    


#view implementing addition profile registration
@login_required
def register_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('khoja:index'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm()
    return render(request, 'khoja/profile_registration.html', {'form':form})

#user profile
def profile(request):
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.data)
        user_form = UserForm(request.data)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
    else:
        profile_form = UserProfileForm()
        user_form = UserForm()
    context = {
        'profile_form': profile_form ,
        'user_form': user_form,
    }
    return render(request, 'khoja/profile.html', context)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('khoja:index'))

        context = {
            'user_profile':user_profile,
            'selected_user': user,
            'form': form
        }
        return render(request, 'khoja/profile.html', context)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('khoja:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('khoja:profile', user.username)
        else:
            print(form.errors)
        context = {
                        'user_profile': user_profile,
                        'selected_user': user,
                        'form': form
        }
        return render(request, 'khoja/profile.html', context)

# view to implement viewing of other user profile
class ListProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        print(profiles)
        return render(request, 'khoja/list_profiles.html',
        {'user_profile_list': profiles})


# view implementing like functionality for category
class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request, category_slug):
        category_id = request.GET['category_id']
        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.likes = category.likes + 1
        category.save()

        return HttpResponse(category.likes)

#view for implementing search help for category
class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')
        
        return render(request, 'categories.html', {'categories':category_list})
