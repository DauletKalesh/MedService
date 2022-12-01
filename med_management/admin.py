from django.contrib import admin
from .models import Hospital, Medical_history, Appointment

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Medical_history)
admin.site.register(Appointment)