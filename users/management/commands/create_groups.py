from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create user groups'

    def handle(self, *args, **kwargs):
        groups = ['moderators']
        for group in groups:
            created, _ = Group.objects.get_or_create(name=group)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group}" created successfully!'))
            else:
                self.stdout.write(f'Group "{group}" already exists.')
