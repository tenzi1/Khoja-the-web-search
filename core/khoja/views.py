from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'boldmessage': 'Hello World!!!'
    }
    return render(request, 'khoja/index.html', context)

def about(request):
    return render(request, 'khoja/about.html')
