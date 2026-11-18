from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{10,15}$',
    message='Enter a valid phone number (10–15 digits).'
)


class Lead(models.Model):

    SOURCE_CHOICES = [
        ('WEBSITE', 'Website'),
        ('REFERRAL', 'Referral'),
        ('SOCIAL', 'Social Media'),
        ('ADVERTISEMENT', 'Advertisement'),
        ('COLD_CALL', 'Cold Call'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('QUALIFIED', 'Qualified'),
        ('UNQUALIFIED', 'Unqualified'),
        ('CONVERTED', 'Converted'),
        ('LOST', 'Lost'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    lead_name = models.CharField(max_length=150)

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=16,
        validators=[phone_validator]
    )

    company_name = models.CharField(max_length=150, blank=True)

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='OTHER'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_leads'
    )

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.lead_name