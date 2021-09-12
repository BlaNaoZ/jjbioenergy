from django.contrib.auth.base_user import AbstractBaseUser
from accounts.models import FoundationIndustry, HeatBuyer, Supplier
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from accounts.models import User

User = get_user_model()

"""
Custom forms for User Creation and Edit.
"""

class UserAdminCreationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = ['name', 'email', 'user_type']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        user.save()

        """
        Based on the user type choice, an instance of said user type is created and initialised.
        """
        if user.user_type == 'Supplier':
            user.supplier_flag = True
            supplier = Supplier.objects.create(user=user)
            supplier.save()
        elif user.user_type == 'Heat Buyer':
            user.heat_buyer_flag = True
            heat_buyer = HeatBuyer.objects.create(user=user)
            heat_buyer.save()
        elif user.user_type == 'Foundation Industry':
            user.foundation_industry_flag = True
            foundation_industry = FoundationIndustry.objects.create(user=user)
            foundation_industry.save()
        else:
            user.admin = True
        
        return user
    
class UserAdminChangeForm(forms.ModelForm):
   
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ['name', 'user_type', 'email', 'password', 'is_active']
    

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]