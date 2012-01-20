from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group

from symposion.review import AUTH_GROUPS


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for group in AUTH_GROUPS:
            Group.objects.get_or_create(name=group)
