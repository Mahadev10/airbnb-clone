import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from conversations.models import Conversation, Message


class Command(BaseCommand):

    help = "This command creates messages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=4,
            type=int,
            help="How many messages you want to craete",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        conversation = random.choice(Conversation.objects.all())
        user = random.choice(conversation.participants.all())
        seeder.add_entity(
            Message,
            number,
            {
                "conversation": conversation,
                "user": user,
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} messages created"))
