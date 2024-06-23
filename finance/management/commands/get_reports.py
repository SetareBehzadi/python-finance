from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('--is-staff', action='active_true', help='Deactivate if user is not staff')

    def handle(self, *args, **options):
        usernames = options['username']
        users = User.objects.filter(username__in=usernames)
        if options['--is-staff']:
            users = users.filter(is_staff=False)
