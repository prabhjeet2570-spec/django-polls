from django.db import migrations


def remove_fourth_choices(apps, schema_editor):
    Choice = apps.get_model("polls", "Choice")
    choices = Choice.objects.using(schema_editor.connection.alias)
    for question, choice in [
        ("Who was the first president of the United States?", "Abraham Lincoln"),
        ("In what year was the Declaration of Independence adopted?", "1865"),
        ("Who was president during the American Civil War?", "Theodore Roosevelt"),
    ]:
        choices.filter(question__question_text=question, choice_text=choice).delete()


class Migration(migrations.Migration):
    dependencies = [("polls", "0004_remove_tutorial_sample")]
    operations = [migrations.RunPython(remove_fourth_choices, migrations.RunPython.noop)]
