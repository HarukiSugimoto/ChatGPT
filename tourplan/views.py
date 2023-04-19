from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    text = "Hello World!!"
    context = {
        'aa' : text
    }
    return render(request, "tourplan/index.html", context)

def test(request):
    return render(request, "tourplan/test.html")
