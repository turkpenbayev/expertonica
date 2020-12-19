from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('filename', 'sites_counter', 'status', 'start_date', 'end_date')
    list_filter = ('sites_counter', 'status', 'start_date', 'end_date')
    
@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'status', 'responce_time')
    list_filter = ('session', 'status',)