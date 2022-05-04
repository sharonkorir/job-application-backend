from django.contrib import admin
from .models import Advertisements, User, Jobseeker, Employer
from django.contrib.auth.models import Group
from . import models

# Register your models here.

admin.site.site_header = "Jobseeker Admin Dashboard"

class AdvertisementsAdmin(admin.ModelAdmin):
    list_display = ("ad_name", "company", "link","ad_content", "ad_image")
    list_filter = ["ad_name"]

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Jobseeker)
admin.site.register(Employer)
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Job)
# admin.site.register(models.Jobseeker)
admin.site.register(models.MpesaPayment)
admin.site.register(Advertisements, AdvertisementsAdmin)
