from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Comment, Jobseeker, Employer,Post, Profile


class PaymentForm(forms.ModelForm):
    id = forms.IntegerField()
    name = forms.CharField()
    phone_number= forms.IntegerField(required=True)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')




class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['Full_name','Email','Contact','Profile_image','Upload_Image']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ['user']

class JobseekerForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        exclude = ('user', 'bio','Education', 'Work_experience','skills','References','avalaibility','salary_expections','Job_category')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user']