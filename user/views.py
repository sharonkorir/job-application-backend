from rest_framework import generics, status
from user.api import permissions
from user.models import Advertisements, Token, Employer
from rest_framework.response import Response
from user.api.serializers import UserSerializer, JobseekerSignupSerializer, EmployerSignupSerializer, AdvertisementSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from user.api.permissions import IsJobseekerUser, IsEmployerUser
from user.api.permissions import IsAdminOrReadOnly
from django.http import HttpResponse, Http404,HttpResponseRedirect
# from user.forms import EmployerInformationForm

# Create your views here.


class JobseekerSignupView(generics.GenericAPIView):
    serializer_class = JobseekerSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class EmployerSignupView(generics.GenericAPIView):
    serializer_class = EmployerSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_jobseeker': user.is_jobseeker
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class JobseekerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsJobseekerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class EmployerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsEmployerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


    # def post(request):
    #     user = request.user
    #     if request.method == 'POST':
    #         form = EmployerInformationForm(request.POST, request.FILES)
    #         form.is_valid()
    #         update = form.save(commit=False)
    #         form.employer = user
    #         update.save()
    #     return Response ({
    #         'update': update
    #     })

def search_results(request):

    if 'employer' in request.GET and request.GET["employer"]:
        search_term = request.GET.get("employer")
        searched_articles = Employer.search_by_title(search_term)
        message = f"{search_term}"

        return Response (request,{"message":message,"employers": searched_articles})

    else:
        message = "You haven't searched for any employer"
        return Response (request,{"message":message})

class AdvertisementsView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_add(self, ad_name):
        try:
            return Advertisements.objects.get(ad_name=ad_name)
        except Advertisements.DoesNotExist:
            return Http404

    def get(self, request, ad_name, format=None):
        add = self.get_add(ad_name)
        serializers = AdvertisementSerializer(add)
        return Response(serializers.data)

    def put(self, request, ad_name, format=None):
        add = self.get_add(ad_name)
        serializers = AdvertisementSerializer(add, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)