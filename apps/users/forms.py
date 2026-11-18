
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


CRM_ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Sales Executive', 'Sales Executive'),
]


class CRMUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(choices=CRM_ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            role_name = self.cleaned_data['role']
            role_group = Group.objects.get(name=role_name)

            user.groups.clear()
            user.groups.add(role_group)

        return user
