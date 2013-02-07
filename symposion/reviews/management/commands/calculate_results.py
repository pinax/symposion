from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group

from symposion.reviews.models import ProposalResult


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        ProposalResult.full_calculate()
