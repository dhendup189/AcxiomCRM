
from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{10,15}$',
    message='Enter a valid phone number (10 to 15 digits, optionally starting with +).'
)


class Customer(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    customer_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=16,
        unique=True,
        validators=[phone_validator]
    )

    company_name = models.CharField(max_length=150, blank=True)

    address = models.TextField(blank=True)

    city = models.CharField(max_length=100, blank=True)

    state = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    created_date = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_customers'
    )

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        if not self.customer_code:
            last_customer = Customer.objects.order_by('-id').first()
            next_number = (last_customer.id + 1) if last_customer else 1
            self.customer_code = f'CUST-{next_number:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer_code} - {self.customer_name}'
