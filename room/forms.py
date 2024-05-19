from .models import Room
from django import forms

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['file']