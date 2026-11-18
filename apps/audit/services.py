from .models import AuditLog


def log_action(user, action, module, record_id=None, details=''):
    return AuditLog.objects.create(
        user=user if getattr(user, 'is_authenticated', False) else None,
        action=action,
        module=module,
        record_id=str(record_id) if record_id is not None else None,
        details=details,
    )