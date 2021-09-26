import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms.models import Room
from users.models import User
from reservations.models import Reservation


class Command(BaseCommand):

    help = "This command creates reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=4,
            type=int,
            help="How many reservations you want to craete",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(
            Reservation,
            number,
            {
                "status": lambda _: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda _: random.choice(users),
                "room": lambda _: random.choice(rooms),
                "check_in": lambda _: datetime.now(),
                "check_out": lambda _: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reservations created"))
