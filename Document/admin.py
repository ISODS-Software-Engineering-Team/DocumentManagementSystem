from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm

from .models import User, Document, Category, Competition
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.



class UserAdminArea(admin.AdminSite):
    site_header = 'Admin'


# Create a Custom User Management for admin.
# Fieldsets must match with attributes in db
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permission', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'is_user')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    # display -- easier for management
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']


admin_site = UserAdminArea()
admin_site = UserAdmin(User, UserAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Document)
admin.site.register(Category)
admin.site.register(Competition)

