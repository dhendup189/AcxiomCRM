from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.followups.models import FollowUp
from apps.opportunities.models import Opportunity

from .services import log_action
from .middleware import get_current_user


TRACKED_MODELS = (Customer, Lead, FollowUp, Opportunity)


@receiver(post_save)
def record_save(sender, instance, created, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    user = get_current_user()
    action = 'CREATE' if created else 'UPDATE'

    log_action(
        user=user,
        action=action,
        module=sender.__name__,
        record_id=instance.pk,
        details=f'{action} {sender.__name__} record #{instance.pk}',
    )


@receiver(pre_delete)
def record_delete(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    log_action(
        user=get_current_user(),
        action='DELETE',
        module=sender.__name__,
        record_id=instance.pk,
        details=f'DELETE {sender.__name__} record #{instance.pk}',
    )


@receiver(user_logged_in)
def record_login(sender, request, user, **kwargs):
    log_action(
        user=user,
        action='LOGIN',
        module='Authentication',
        record_id=user.pk,
        details=f'User {user.username} logged in',
    )


@receiver(user_logged_out)
def record_logout(sender, request, user, **kwargs):
    if user is None:
        user = get_current_user()

    log_action(
        user=user,
        action='LOGOUT',
        module='Authentication',
        record_id=user.pk if user else None,
        details=f'User {user.username} logged out' if user else 'User logged out',
    )