from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    REQUIRED = []

    def __str__(self):
        return f'{self.username}User'

    def save_user(self):
        super().save()

    @classmethod
    def get_user(cls):
        user=User.objects.all()
        return user

    def delete_user(self):
        self.delete()

class Post(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField(max_length=255)
    file= models.CharField( )
    