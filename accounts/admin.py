from django.contrib import admin
from .models import User, Country, DocumentSet
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserManager(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ('name', 'username', 'country', 'is_admin')
    ordering = ('-date_joined',)

admin.site.register(User, UserManager)
admin.site.register(Country)
admin.site.register(DocumentSet)
