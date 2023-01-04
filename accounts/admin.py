from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.utils.html import format_html

# Register your models here.
class UserAccountAdmin(UserAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_pic.url))
    list_display = ['thumbnail','username', 'email','last_login','date_created','profile_updated']
    list_display_link = ['username','email']
    readonly_fields = ['last_login', 'date_created', 'profile_updated']
    ordering = ('-last_login', )
# to present fields lined up in a horizontal direction
    filter_horizontal    = ()
    list_filter          = ()
    fieldsets            = ()

admin.site.register(models.UserAccount, UserAccountAdmin)

