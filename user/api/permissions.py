from rest_framework.permissions import BasePermission



class IsJobseekerUser(BasePermission):
    def has_permission(self, request, view):


        return bool(request.user and request.user.is_jobseeker)



class IsEmployerUser(BasePermission):
    def has_permission(self, request, view):

        
        return bool(request.user and request.user.is_employer)

from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff