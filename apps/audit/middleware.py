from threading import local

_audit_context = local()


def get_current_user():
    return getattr(_audit_context, 'user', None)


class AuditUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _audit_context.user = getattr(request, 'user', None)

        try:
            return self.get_response(request)
        finally:
            _audit_context.user = None