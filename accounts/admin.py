from accounts.models import FoundationIndustry, HeatBuyer, Supplier, User
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    """ 
    The forms to add and change user instances
    The fields to be used in displaying the User model.
    These override the definitions on the base UserAdmin
    that reference specific fields on auth.User.
    """
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    """
    When displayed in a list, user instances are shown using their emails and whether 
    they are admins or not.
    Filtered by wheter they are admins or not.
    """
    list_display = ['email', 'admin']
    list_filter = ['admin']

    """
    The fields to be shown on the UserAdmin page.
    """
    fieldsets = (
                (None, {'fields': ('email', )}),
                ('Permissions', {'fields': ('admin', )}),
    )
    
    """
    Fields to be completed when creating a user instance.
    """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2', 'user_type')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


#Registering the new UserAdmin.
admin.site.register(User, UserAdmin)

""" 
Classes used for adding admin pages for each user type (Heat Buyer, Foundation Industry and Supplier) with their respective fields.
"""
class FoundationAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'name']
    add_fieldsets = ['name']
    fieldsets = (
                ('Details', {'fields': ('name', 'user', 'level_one', 'level_two')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'user')
        }),
    )

    ordering = ['name']

class HeatAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'name']
    add_fieldsets = ['name']
    fieldsets = (
                ('Details', {'fields': ('name', 'user', 'level_one', 'level_two')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'user')
        }),
    )

    ordering = ['name']

class SupplierAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'name']
    add_fieldsets = ['name']
    fieldsets = (
                ('Details', {'fields': ('name', 'user', 'website', 'level_one', 'level_two')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'user')
        }),
    )

    ordering = ['name']

admin.site.register(FoundationIndustry, FoundationAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(HeatBuyer, HeatAdmin)
