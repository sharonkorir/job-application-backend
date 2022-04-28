from django.urls import path
from django.urls import path, include
from . import views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet)
router.register('posts', views.PostViewSet)
urlpatterns = [
     path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]