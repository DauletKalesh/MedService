from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import AdvancedUser, Profile

# Register your models here.
admin.site.register(AdvancedUser)
# admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'birthday', 'avatar_img', 'gender',)

    def avatar_img(self, obj):
        if hasattr(obj.avatar, 'url'):
            return format_html('<img src="{}" width = 50/>'.format(getattr(obj.avatar, 'url')))
        return None

    avatar_img.short_description = 'Image'
