from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,PasswordResetForm, SetPasswordForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username','id':'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password','id':'login-pwd'}))

class CreateForm(UserCreationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"].label = 'Repeat Password'
        self.fields['username'].widget.attrs = {'class':'form-control','placeholder':'Enter Your Username'}
        self.fields['email'].widget.attrs = {'class':'form-control','placeholder':"Enter Your Email"}
        self.fields['password1'].widget.attrs = {'class':'form-control','placeholder':"Passwords must not be less than 8 figures or letters"}
        self.fields['password2'].widget.attrs = {'class':'form-control','placeholder':'Enter Password again they are case sensitive'}
    class Meta:
        model = User
        fields =['username','email','password1','password2']
    
    def clean_username(self):
        user_name = self.cleaned_data['username']
        test = User.objects.filter(username=user_name).exists()
        if test:
            forms.ValidationError("This Username can't be used, Try another Username")
        else:
            return user_name



class PwdResetForm(PasswordResetForm):
    email = forms.CharField(max_length= 250, widget = forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'email','id':'form-email'}))

    def clean_email(self):
        email = self.cleaned_data[email]
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError('Unfortunately we cant find the email address')

        return email

class PwdConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email address', 'id': 'form-email'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken, Try another email')
        return email
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =[ 'bio','avatar']
        widgets = {'bio':forms.Textarea(attrs={'class':'form-control','row':'5'})}

class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label=("Old password"),
                                    widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-new-pass2'}),min_length=7)
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder':"Repeat New Password", 'id': 'form-new-pass2'}))

    def clean_data(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        if new_password1 != new_password2:
            raise forms.ValidationError("Password Does Not Match")
        return self.new_password1
