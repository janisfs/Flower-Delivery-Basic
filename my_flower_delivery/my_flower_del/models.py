from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # Наследуем встроенную модель AbstractUser
    email = models.EmailField(unique=True)  # Поле email становится уникальным
