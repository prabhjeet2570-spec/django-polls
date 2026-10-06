from django.db import migrations


def remove_old_demo_polls(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.using(schema_editor.connection.alias).filter(question_text__in=[
        "Which language do you most enjoy coding in?",
        "Where do you do your best studying?",
        "What would you like to build next?",
    ]).delete()


class Migration(migrations.Migration):
    dependencies = [("polls", "0001_initial")]
    operations = [migrations.RunPython(remove_old_demo_polls, migrations.RunPython.noop)]
