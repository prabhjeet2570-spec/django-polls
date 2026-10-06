from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from polls.models import Question


class Command(BaseCommand):
    help = "Create the final sample question and choices from tutorial part 2."

    @transaction.atomic
    def handle(self, *args, **options):
        question, _ = Question.objects.get_or_create(
            question_text="What's up?", defaults={"pub_date": timezone.now()}
        )
        for text in ("Not much", "The sky"):
            question.choice_set.get_or_create(choice_text=text, defaults={"votes": 0})
        self.stdout.write(self.style.SUCCESS("Tutorial poll is ready."))
