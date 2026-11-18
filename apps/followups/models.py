from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class FollowUp(models.Model):

    TYPE_CHOICES = [
        ('CALL', 'Call'),
        ('EMAIL', 'Email'),
        ('MEETING', 'Meeting'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('COMPLETED', 'Completed'),
        ('MISSED', 'Missed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='followups'
    )

    lead = models.ForeignKey(
        'leads.Lead',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='followups'
    )

    subject = models.CharField(max_length=200)

    followup_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='CALL'
    )

    scheduled_at = models.DateTimeField()

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_followups'
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_followups'
    )

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def clean(self):
        if not self.customer and not self.lead:
            raise ValidationError(
                'A follow-up must be linked to at least a customer or a lead.'
            )

        if self.status == 'PLANNED' and self.scheduled_at:
            if self.scheduled_at < timezone.now():
                raise ValidationError(
                    'A planned follow-up cannot be scheduled in the past.'
                )

    def __str__(self):
        return self.subject
