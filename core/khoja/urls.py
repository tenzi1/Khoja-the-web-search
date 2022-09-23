from django.urls import path
from khoja import views

app_name = 'khoja'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('category/<slug:category_name_slug>/', views.show_category, name="show_category")
]