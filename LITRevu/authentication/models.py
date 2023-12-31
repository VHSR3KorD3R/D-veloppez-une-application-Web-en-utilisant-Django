from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)