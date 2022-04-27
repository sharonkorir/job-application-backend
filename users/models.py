from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Jobseeker(models.Model):
    jobid =  models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)
    location= models.IntegerField(blank=True)
    professsion=models.CharField(max_length=255)
    jobtype=models.CharField(max_length=255)
    experience=models.CharField(max_length=255)
    Education_level=models.CharField(max_length=255)
    job_category=models.CharField(max_length=255)
    contact=models.IntegerField()
    salary_Expectation=models.IntegerField()
    status=models.IntegerField()
    # file=models.Cloudinary()
    # profile_pic=models.Cloudinary()
    bio=models.CharField(max_length=255)
    work=models.CharField(max_length=255)
    Education=models.CharField(max_length=255)
    skills=models.CharField(max_length=255)
    reference=models.CharField(max_length=255)



class Post(models.Model):
    id =  models.IntegerField( primary_key=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    # file=models.Cloudinary()

def __str__(self):
        return f'{self.title}'

def delete_post(self):
        self.delete()

@classmethod
def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()

@classmethod
def all_posts(cls):
        return cls.objects.all()

def save_post(self):
        self.save()
class Comment(models.Model):
    id =  models.IntegerField(primary_key=True ) 
    userId=models.IntegerField()
    content=models.CharField(max_length=255)
    post=models.CharField(max_length=255)
    like=models.IntegerField()
    dislike=models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f'{self.user.name} post'





class Employer(models.Model):
    id =  models.IntegerField(Post, primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    contact=models.IntegerField()
    location= models.IntegerField(blank=True)
    address=models.CharField(max_length=255)
    company_bio=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    # company_pic=models.Cloudinary()

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    is_jobseeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name='user')
    is_employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='user')

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


    
   