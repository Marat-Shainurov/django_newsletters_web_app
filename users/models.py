from django.contrib.auth.models import AbstractUser
from django.db import models

from newsletter.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='user_email', max_length=100, unique=True)
    phone = models.CharField(verbose_name='user_phone', max_length=50, **NULLABLE)
    avatar = models.ImageField(verbose_name='user_avatar', upload_to='avatars/', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []