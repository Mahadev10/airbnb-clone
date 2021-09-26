import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms.models import Room
from users.models import User
from reviews.models import Review


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=4, type=int, help="How many reviews you want to craete"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda _: random.randint(0, 6),
                "communication": lambda _: random.randint(0, 6),
                "cleanliness": lambda _: random.randint(0, 6),
                "location": lambda _: random.randint(0, 6),
                "check_in": lambda _: random.randint(0, 6),
                "value": lambda _: random.randint(0, 6),
                "user": lambda _: random.choice(users),
                "room": lambda _: random.choice(rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created"))
