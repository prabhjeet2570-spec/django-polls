from django.db import migrations


def remove_tutorial_sample(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.using(schema_editor.connection.alias).filter(question_text="What's up?").delete()


class Migration(migrations.Migration):
    dependencies = [("polls", "0003_remove_custom_sample_polls")]
    operations = [migrations.RunPython(remove_tutorial_sample, migrations.RunPython.noop)]
