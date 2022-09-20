from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse(" Home page....<a href='/khoja/about/'>About Page</a>")

def about(request):
    return HttpResponse("Here is the about page... <a href='/'>Home Page</a>")
