from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__' 

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        parents = cleaned_data.get('parents', [])

        # Custom validation logic
        for parent in parents:
            if parent.level > level:
                raise ValidationError({
                    'parents': f"Parent document '{parent}' must be of the same or higher level."
                })

        prev_version = cleaned_data.get('prev_version')
        if prev_version and prev_version.number != cleaned_data.get('number'):
            raise ValidationError({
                'prev_version': "Previous version must have the same number as the current document."
            })

        return cleaned_data
