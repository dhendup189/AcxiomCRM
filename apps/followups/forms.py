from django import forms
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            'customer',
            'lead',
            'subject',
            'followup_type',
            'scheduled_at',
            'status',
            'assigned_to',
            'notes',
        ]

        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'lead': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Follow-up subject',
                'required': True,
            }),
            'followup_type': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }, format='%Y-%m-%dT%H:%M'),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Follow-up notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].required = False
        self.fields['lead'].required = False
        self.fields['assigned_to'].required = False
        self.fields['customer'].empty_label = 'Select customer (optional)'
        self.fields['lead'].empty_label = 'Select lead (optional)'

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        lead = cleaned_data.get('lead')

        if not customer and not lead:
            raise forms.ValidationError(
                'Select at least one Customer or Lead.'
            )

        return cleaned_data