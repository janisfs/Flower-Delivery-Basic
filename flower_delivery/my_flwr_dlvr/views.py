from django.shortcuts import get_object_or_404, render, redirect
from .models import Flower
# from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the my_flwr_dlvr index.")
    return render(request, 'my_flwr_dlvr/index.html')


def login(request):
    # return HttpResponse("Login page.")
    return render(request, 'my_flwr_dlvr/login.html')


def register(request):
    # return HttpResponse("Register page.")
    return render(request, 'my_flwr_dlvr/register.html')


def logout(request):
    # return HttpResponse("Logout page.")
    return redirect(request, 'my_flwr_dlvr/index.html')


def order(request):
    # return HttpResponse("Order page.")
    return render(request, 'my_flwr_dlvr/order.html')

def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'flower_detail.html', {'flower': flower})