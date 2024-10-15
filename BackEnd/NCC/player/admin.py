from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export.admin import ExportActionMixin


class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'isLogin'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('isLogin',)  # Note the comma to create a tuple
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('isLogin',)  # Note the comma to create a tuple
        })
    )


admin.site.register(User, UserAdmin)

class TeamAdmin (ExportActionMixin,admin.ModelAdmin):
    list_display = ("teamId","user1","user2","contest","score","isLogin","isJunior","lastUpdate")
admin.site.register(Team,TeamAdmin)



class LoginAllowAdmin(admin.ModelAdmin):
    list_display= ("id","user")
admin.site.register(LoginAllow,LoginAllowAdmin)