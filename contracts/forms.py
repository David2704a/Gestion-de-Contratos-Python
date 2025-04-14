from django import forms
from .models import Clause

class ClauseForm(forms.ModelForm):
    class Meta:
        model = Clause
        fields = ['organization', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
