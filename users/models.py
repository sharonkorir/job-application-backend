from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
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




class Comment(models.Model):
    id =  models.IntegerField(primary_key=True)
    userId=models.IntegerField()
    content=models.CharField()
    post=models.CharField()
    like=models.IntegerField()
    dislike=models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f'{self.user.name} post'



class Post(models.Model):
    id =  models.IntegerField(Comment, primary_key=True)
    title=models.CharField()
    description=models.CharField()
    file=models.Cloudinary()

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

class Employer(models.Model):
    id =  models.IntegerField(Post, primary_key=True)
    name=models.CharField()
    email=models.CharField()
    contact=models.IntegerField()
    location= models.IntegerField(blank=True)
    address=models.CharField()
    company_bio=models.CharField()
    name=models.CharField()
    company_pic=models.Cloudinary()

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    is_jobseeker = models.ForeignKey(Jobseeker, related_name='user')
    is_employer = models.ForeignKey(Employer, related_name='user')

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


    
   