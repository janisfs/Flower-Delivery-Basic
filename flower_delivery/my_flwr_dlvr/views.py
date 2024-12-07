from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the my_flwr_dlvr index.")
   # return render(request, 'index.html')


def login_view(request):
    return HttpResponse("Login page.")


def register_view(request):
    return HttpResponse("Register page.")


def logout_view(request):
    return HttpResponse("Logout page.")


def order_view(request):
    return HttpResponse("Order page.")