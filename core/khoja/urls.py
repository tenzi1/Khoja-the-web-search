from django.urls import path
from khoja import views

app_name = 'khoja'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('category/<slug:category_name_slug>/', views.show_category, name="show_category"),
    path('add_category/', views.add_category, name="add_category"),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('user_register/', views.user_register, name='user_register'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('search/', views.search, name='search'),
    path('goto/<int:page_id>/', views.goto_url, name='goto'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('register_profile', views.register_profile, name='register_profile'),
    path('profiles/', views.ListProfileView.as_view(), name='list_profiles'),
    path('category/<slug:category_slug>/khoja/like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
]
