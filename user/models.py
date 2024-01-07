from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

MAX_USERNAME_LENGTH = 64

class User(AbstractUser):
    username = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
    email = models.EmailField(unique=True)


