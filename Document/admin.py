from django.contrib import admin
from . import models
# Register your models here.


class UserAdminArea(admin.AdminSite):
    site_header = 'Admin'


admin_site = UserAdminArea()
admin.site.register(models.User)
admin.site.register(models.Document)
admin.site.register(models.Category)
