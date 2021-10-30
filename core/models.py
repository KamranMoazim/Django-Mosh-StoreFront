from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# TIP: always create your User Model before creating any app and just 'pass' it 

class User(AbstractUser):
    # pass
    email = models.EmailField(unique=True)