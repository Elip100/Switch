from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    account_type = models.CharField(max_length=200, choices=[("SA", "Scratch Auth"), ("PA", "Password")])