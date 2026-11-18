
from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'lead_name',
            'email',
            'phone',
            'company_name',
            'source',
            'status',
            'priority',
            'assigned_to',
            'notes',
        ]

        widgets = {
            'lead_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lead name',
                'required': True,
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10–15 digits',
                'pattern': r'\+?[0-9]{10,15}',
                'required': True,
            }),

            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name',
            }),

            'source': forms.Select(attrs={
                'class': 'form-select',
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-select',
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional lead information...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].empty_label = 'Unassigned'

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        for field_name in ['source', 'status', 'priority', 'assigned_to']:
            self.fields[field_name].widget.attrs['class'] = 'form-select'
