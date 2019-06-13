from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Update project'

    def add_arguments(self, parser):
        parser.add_argument('--force-git', type=bool)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Not implement yet'))
