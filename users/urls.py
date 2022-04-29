


from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.models import MpesaPayment
from . import views
from rest_framework.routers import DefaultRouter
from .views import  MpesaPaymentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('MpesaPayment', views.MpesaPaymentViewSet)
# router.register('posts', views.PostViewSet)
# router.register('profile', views.ProfileViewSet)



urlpatterns = [
     path('', include(router.urls)),
     path('api/', include(router.urls)),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('register/', views.signup, name='signup'),
    # path('account/', include('django.contrib.auth.urls')),
    # path('profile/<username>', views.profile, name='profile'),
    # path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)