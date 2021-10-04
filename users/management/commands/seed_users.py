from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from django.contrib.admin.utils import flatten


class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to craete"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "email_secret": "",
            },
        )
        cleaned_users = seeder.execute()
        created_clean = flatten(list(cleaned_users.values()))
        for pk in created_clean:
            user = User.objects.get(pk=pk)
            user.set_password("messi123")
            user.save()
        self.stdout.write(self.style.SUCCESS(f"{number} users created"))
