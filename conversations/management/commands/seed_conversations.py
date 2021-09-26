import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from conversations.models import Conversation


class Command(BaseCommand):

    help = "This command creates conversations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=4,
            type=int,
            help="How many conversations you want to craete",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        seeder.add_entity(
            Conversation,
            number,
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            conversation_model = Conversation.objects.get(pk=pk)
            to_add = users[random.randint(0, 5): random.randint(6, 27)]
            conversation_model.participants.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} conversations created"))
