from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Medical_history)
admin.site.register(Appointment)
admin.site.register(Comment)