from django.contrib.auth.models import AbstractUser
from django.db import models

from newsletter.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='user_email', max_length=100, unique=True)
    phone = models.CharField(verbose_name='user_phone', max_length=50, **NULLABLE)
    avatar = models.ImageField(verbose_name='user_avatar', upload_to='avatars/', **NULLABLE)
    verification_code = models.CharField(verbose_name='email_verification_code', **NULLABLE)
    is_verified = models.BooleanField(verbose_name='is_verified', default=False, **NULLABLE)
    is_manager = models.BooleanField(verbose_name='is_manager', default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
