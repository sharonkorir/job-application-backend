from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from worklinks.settings import AUTH_USER_MODEL
from cloudinary.models import CloudinaryField

# Create your models here.


class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Jobseeker(models.Model):
    user = models.OneToOneField(User, related_name='jobseeker', on_delete=models.CASCADE)
    jobseeker_name = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.jobseeker_name


class Employer(models.Model):
    user = models.OneToOneField(User, related_name='employer', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    company_contact = models.CharField(max_length=255, blank=True)
    company_location = models.CharField(max_length=255, blank=True)
    company_bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True)
    company_profile = CloudinaryField('image', null=True)
    

    def save_employer(self):
        self.save()

    def delete_employer(self):
        self.delete()

    @classmethod
    def search_by_company_name(cls, search_term):
        company = cls.objects.filter(title__icontains=search_term)
        return company

    def __str__(self):
        return self.company_name

class Advertisements(models.Model):
    user = models.OneToOneField(
        User, related_name='admin', on_delete=models.CASCADE)
    ad_name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    ad_content = models.TextField(max_length=500, blank=True)
    ad_image = models.ImageField('ad_image', null=True)

    def __str__(self):
        return self.ad_name
