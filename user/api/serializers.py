from rest_framework import serializers
from user.models import Advertisements, User, Jobseeker, Employer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_jobseeker"]

    
class JobseekerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password2"}, write_only=True)
    class Meta:
        model = User
        fields=['username', 'email', 'password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # def save(self, **kwargs):
    #     user = User(
    #         username=self.validated_data['username'],
    #         email=self.validated_data['email']
    #     )
    #     password =self.validated_data['password'],
    #     # password2 =self.validated_data['password2']
    #     # if password != password2:
    #     #     raise serializers.ValidationError({"error":"passwords did not match"})
    #     user.set_password(password)
    #     user.is_jobseeker = True
    #     user.save()
    #     Jobseeker.objects.create(user=user)
    #     return user
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_jobseeker=True
        user.save()
        Jobseeker.objects.create(user=user)
        return user

class EmployerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password2"}, write_only=True)
    class Meta:
        model = User
        fields=['username', 'email', 'password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # def save(self, **kwargs):
    #     user = User(
    #         username=self.validated_data['username'],
    #         email=self.validated_data['email']
    #     )
    #     password =self.validated_data['password'],
    #     # password2 =self.validated_data['password2']
    #     # if password!=password2:
    #     #     raise serializers.ValidationError({"error":"passwords did not match"})
    #     user.set_password(password)
    #     user.is_employer = True
    #     user.save()
    #     Employer.objects.create(user=user)
    #     return user

def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_employer=True
        user.save()
        Employer.objects.create(user=user)
        return user

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisements
        fields = ('ad_name', 'company','ad_content','link', 'ad_image')


class UpdateEmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['name', 'email', 'contact', 'company_location', 'company_bio', 'address', 'company_pic']