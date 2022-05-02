from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Job)
# admin.site.register(models.Jobseeker)
admin.site.register(models.MpesaPayment)