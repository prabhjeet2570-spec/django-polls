from datetime import timedelta
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


class PollsTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(question_text="Pick a language", pub_date=timezone.now())
        self.choice = self.question.choice_set.create(choice_text="Python")

    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_home_redirects_to_polls(self):
        self.assertRedirects(self.client.get("/"), reverse("polls:index"))

    def test_index_and_detail_show_question_and_choices(self):
        self.assertContains(self.client.get(reverse("polls:index")), self.question.question_text)
        self.assertContains(self.client.get(reverse("polls:detail", args=[self.question.pk])), "Python")

    def test_vote_increases_count_and_redirects_to_results(self):
        response = self.client.post(reverse("polls:vote", args=[self.question.pk]), {"choice": self.choice.pk})
        self.assertRedirects(response, reverse("polls:results", args=[self.question.pk]))
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)
        self.assertContains(self.client.get(response.url), "1 vote")

    def test_missing_and_invalid_choices_do_not_record_vote(self):
        for data in ({}, {"choice": 99999}):
            response = self.client.post(reverse("polls:vote", args=[self.question.pk]), data)
            self.assertContains(response, "You didn&#x27;t select a choice.")
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_cannot_vote_for_choice_from_another_question(self):
        other = Question.objects.create(question_text="Other poll", pub_date=timezone.now())
        foreign_choice = other.choice_set.create(choice_text="Another option")
        response = self.client.post(reverse("polls:vote", args=[self.question.pk]), {"choice": foreign_choice.pk})
        self.assertContains(response, "You didn&#x27;t select a choice.")
        foreign_choice.refresh_from_db()
        self.assertEqual(foreign_choice.votes, 0)

    def test_vote_requires_csrf_token(self):
        url = reverse("polls:vote", args=[self.question.pk])
        browser = Client(enforce_csrf_checks=True)
        self.assertEqual(browser.post(url, {"choice": self.choice.pk}).status_code, 403)
        browser.get(reverse("polls:detail", args=[self.question.pk]))
        response = browser.post(url, {"choice": self.choice.pk, "csrfmiddlewaretoken": browser.cookies["csrftoken"].value})
        self.assertEqual(response.status_code, 302)

    def test_missing_question_returns_404(self):
        self.assertEqual(self.client.get(reverse("polls:detail", args=[99999])).status_code, 404)

    def test_seed_command_preserves_existing_votes(self):
        call_command("seed_polls", verbosity=0)
        choice = Question.objects.get(question_text="Who was the first president of the United States?").choice_set.first()
        choice.votes = 7
        choice.save()
        count = Question.objects.count()
        call_command("seed_polls", verbosity=0)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 7)
        self.assertEqual(Question.objects.count(), count)

    def test_recent_publication_matches_part_two(self):
        self.assertTrue(self.question.was_published_recently())
        self.question.pub_date = timezone.now() + timedelta(days=1)
        self.assertTrue(self.question.was_published_recently())
        self.question.pub_date = timezone.now() - timedelta(days=2)
        self.assertFalse(self.question.was_published_recently())

    def test_admin_requires_login(self):
        self.assertEqual(self.client.get("/admin/").status_code, 302)
