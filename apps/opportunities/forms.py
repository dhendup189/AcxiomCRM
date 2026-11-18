from django import forms
from .models import Opportunity


class OpportunityForm(forms.ModelForm):

    class Meta:
        model = Opportunity

        fields = [
            'opportunity_name',
            'customer',
            'stage',
            'amount',
            'probability',
            'expected_close_date',
            'assigned_to',
            'notes',
        ]

        widgets = {
            'opportunity_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter opportunity name'
            }),

            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),

            'stage': forms.Select(attrs={
                'class': 'form-select'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Enter sales amount'
            }),

            'probability': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': '0–100'
            }),

            'expected_close_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional details...'
            }),
        }

    def clean_probability(self):
        probability = self.cleaned_data.get('probability')

        if probability is not None and not 0 <= probability <= 100:
            raise forms.ValidationError(
                'Probability must be between 0 and 100.'
            )

        return probability

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        stage = self.cleaned_data.get('stage')

        if amount is not None and amount < 0:
            raise forms.ValidationError(
                'Amount cannot be negative.'
            )

        if stage not in ['WON', 'LOST'] and amount is not None and amount <= 0:
            raise forms.ValidationError(
                'Active opportunities must have an amount greater than zero.'
            )

        return amount