from django.contrib import admin
from .models import AdvancedUser, Profile, ProfileDetail

# Register your models here.
admin.site.register(AdvancedUser)
admin.site.register(Profile)
admin.site.register(ProfileDetail)