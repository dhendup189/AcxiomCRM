
from django.contrib.auth.decorators import user_passes_test


def is_admin_role(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='Admin').exists()
    )


def is_manager_role(user):
    return user.is_authenticated and (
        is_admin_role(user) or user.groups.filter(name='Manager').exists()
    )


def is_sales_role(user):
    return user.is_authenticated and user.groups.filter(
        name='Sales Executive'
    ).exists()


def can_manage_all_records(user):
    return is_manager_role(user)


def scope_records(queryset, user, module):
    """
    Admin/Manager can access all records.
    Other users can access records assigned to them.
    Customers are scoped to the creator because Customer has created_by.
    """

    if can_manage_all_records(user):
        return queryset

    if module == 'customers':
        return queryset.filter(created_by=user)

    if module in ('leads', 'followups', 'opportunities'):
        return queryset.filter(assigned_to=user)

    return queryset.none()


def manager_required(view_func):
    return user_passes_test(can_manage_all_records)(view_func)
