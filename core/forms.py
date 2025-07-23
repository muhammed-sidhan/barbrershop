from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class BarberSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    shop_name=forms.CharField(
        max_length=255, 
        required=True,
        help_text='Please enter your shopename')

    location=forms.CharField( 
            max_length=255, 
            required=False,
            help_text='Please enter your location')
    class Meta :
        model=User
        fields=('username','email','password1','password2')


    def save(self, commit = True):
        user=super().save(commit=False)
        user.role='barber'
        if commit:
            user.save()
            from .models import BarberProfile
            BarberProfile.objects.create(user=user,
            shop_name=self.cleaned_data['shop_name'],
            location=self.cleaned_data['location'])

        return user
    

class CustomerSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def save(self, commit = True):
        user=super().save(commit=False)
        user.role='customer'
        if commit:
            user.save()
            from .models import CustomerProfile
            CustomerProfile.objects.create(user=user)
        return user
