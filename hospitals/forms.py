from django import forms
from .models import Service


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['is_available', 'queue_count', 'estimated_wait_time']
        widgets = {
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'queue_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estimated_wait_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        labels = {
            'is_available': 'Disponible',
            'queue_count': 'Patients en attente',
            'estimated_wait_time': "Temps d'attente (min)",
        }
