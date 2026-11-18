from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create and configure AcxiomCRM user roles'

    def handle(self, *args, **options):

        app_models = {
            'customers': 'customer',
            'leads': 'lead',
            'followups': 'followup',
            'opportunities': 'opportunity',
        }

        role_permissions = {
            'Admin': ['add', 'change', 'delete', 'view'],
            'Manager': ['add', 'change', 'view'],
            'Sales Executive': ['add', 'change', 'view'],
        }

        for role_name, actions in role_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)

            permissions = []

            for app_label, model_name in app_models.items():
                for action in actions:
                    codename = f'{action}_{model_name}'

                    permission = Permission.objects.filter(
                        content_type__app_label=app_label,
                        codename=codename
                    ).first()

                    if permission:
                        permissions.append(permission)

            group.permissions.set(permissions)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created role: {role_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Updated role: {role_name}')
                )

        self.stdout.write(
            self.style.SUCCESS('CRM roles configured successfully.')
        )