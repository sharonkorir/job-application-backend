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
    
class Employer(models.Model):
    id =  models.IntegerField(primary_key=True)
    name=models.CharField()
    email=models.CharField()
    contact=models.IntegerField()
    location= models.IntegerField(blank=True)
    address=models.CharField()
    company_bio=models.CharField()
    name=models.CharField()
    company_pic=models.Cloudinary()

class Jobseeker(models.Model):
    jobid =  models.IntegerField(primary_key=True)
    name=models.CharField()
    location= models.IntegerField(blank=True)
    professsion=models.CharField()
    jobtype=models.CharField()
    experience=models.CharField()
    Education_level=models.CharField()
    job_category=models.CharField()
    contact=models.IntegerField()
    salary_Expectation=models.IntegerField()
    status=models.IntegerField()
    file=models.Cloudinary()
    profile_pic=models.Cloudinary()
    bio=models.CharField()
    work=models.CharField()
    Education=models.CharField()
    skills=models.CharField()
    reference=models.CharField()

    
    def save_user_move(sender, instance, **kwargs):
        instance.move.save()  