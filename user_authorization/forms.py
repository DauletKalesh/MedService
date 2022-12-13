from django import forms  
from .models import *

class AdvancedUserForm(forms.ModelForm):
    class Meta:  
        model = AdvancedUser 
        fields = "__all__" 