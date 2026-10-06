from django.db import migrations


def remove_custom_samples(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.using(schema_editor.connection.alias).filter(
        question_text__in=[
            "Which transport do you prefer for everyday trips?",
            "How do you prefer to spend a free evening?",
            "Which feature matters most when choosing a phone?",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("polls", "0002_replace_demo_polls")]
    operations = [migrations.RunPython(remove_custom_samples, migrations.RunPython.noop)]
