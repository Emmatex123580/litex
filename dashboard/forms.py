from django import forms
from django.forms.widgets import PasswordInput, DateInput,TextInput, EmailInput, FileInput, NumberInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField ,UserCreationForm ,AuthenticationForm ,PasswordResetForm, PasswordChangeForm, SetPasswordForm 
from .models import CustomUser, Wallets
from  django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

class UserRegistrationForm(forms.ModelForm):
  password1 = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
  )

  class Meta:
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'date_of_birth','phone_number' )

    widgets = {
      'first_name': TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'first name',
          'required': "required"
      }),
      'last_name': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'last name',
        'required': 'required'
      }),
      'email': EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'Email',
          'required': "required"
      }),
      'date_of_birth': DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'dd/mm/yy',
        'required': 'required'
      }),
      'phone_number': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'phone',
        'required': 'required'
      })
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords dont seem to match')
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "email or username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )

  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')




class BvnForm(forms.Form):
    bvn = forms.CharField(widget=NumberInput(attrs={'class':'form-control','placeholder':'bvn', 'required':'required'}))


class UpdateBvnForm(forms.Form):
    bvn = forms.CharField(widget=NumberInput(attrs={'class':'form-control','placeholder':'set pin','required':'required'}))


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields =('email', 'password', 'phone_number')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")

