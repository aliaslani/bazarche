from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='شماره تلفن')

    def __str__(self) -> str:
        return self.get_full_name() or self.username



