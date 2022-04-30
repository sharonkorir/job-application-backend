


from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.models import MpesaPayment
from . import views
from rest_framework.routers import DefaultRouter
from .views import  MpesaPaymentViewSet, activate
from rest_framework import routers

router = routers.DefaultRouter()
router.register('MpesaPayment', views.MpesaPaymentViewSet)
router.register('Job', views.JobViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('api/', include(router.urls)),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     path('MpesaPayment/', views.Job, name='MpesaPayment'),
    path('job/', views.Job, name='Job'),
     path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'),  
   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)