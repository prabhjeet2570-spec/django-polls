from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from polls.models import Question

SAMPLE_POLLS = [
    ("Who was the first president of the United States?", [
        "George Washington", "Thomas Jefferson", "John Adams", "Abraham Lincoln",
    ]),
    ("In what year was the Declaration of Independence adopted?", [
        "1492", "1776", "1789", "1865",
    ]),
    ("Who was president during the American Civil War?", [
        "George Washington", "Andrew Jackson", "Abraham Lincoln", "Theodore Roosevelt",
    ]),
]


class Command(BaseCommand):
    help = "Create three simple U.S. history polls without resetting votes."

    @transaction.atomic
    def handle(self, *args, **options):
        for text, choices in SAMPLE_POLLS:
            question, _ = Question.objects.get_or_create(
                question_text=text, defaults={"pub_date": timezone.now()}
            )
            for choice_text in choices:
                question.choice_set.get_or_create(choice_text=choice_text, defaults={"votes": 0})
        self.stdout.write(self.style.SUCCESS("U.S. history polls are ready."))
