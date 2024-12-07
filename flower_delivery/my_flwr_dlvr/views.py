from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the my_flwr_dlvr index.")
    return render(request, 'my_flwr_dlvr/index.html')


def login_view(request):
    # return HttpResponse("Login page.")
    return render(request, 'my_flwr_dlvr/login.html')


def register_view(request):
    # return HttpResponse("Register page.")
    return render(request, 'my_flwr_dlvr/register.html')


def logout_view(request):
    # return HttpResponse("Logout page.")
    return render(request, 'my_flwr_dlvr/logout.html')


def order_view(request):
    # return HttpResponse("Order page.")
    return render(request, 'my_flwr_dlvr/order.html')