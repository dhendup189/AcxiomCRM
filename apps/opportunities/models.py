from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Opportunity(models.Model):

    STAGE_CHOICES = [
        ('QUALIFICATION', 'Qualification'),
        ('PROPOSAL', 'Proposal'),
        ('NEGOTIATION', 'Negotiation'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]

    opportunity_name = models.CharField(max_length=200)

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='opportunities'
    )

    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='QUALIFICATION'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    probability = models.IntegerField(
        default=10,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    expected_close_date = models.DateField()

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_opportunities'
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_opportunities'
    )

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    @property
    def weighted_value(self):
        return self.amount * self.probability / 100

    class Meta:
        ordering = ['-created_date']

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.stage not in ['WON', 'LOST']:
            if self.amount is not None and self.amount <= 0:
                raise ValidationError(
                    {'amount': 'Active opportunities must have an amount greater than zero.'}
                )

            if self.expected_close_date and self.expected_close_date < timezone.now().date():
                raise ValidationError(
                    {'expected_close_date': 'Expected close date cannot be in the past.'}
                )

    def __str__(self):
        return self.opportunity_name