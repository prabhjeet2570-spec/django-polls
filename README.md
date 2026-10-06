# Django polls

SWE personal assignment 4.4: Django tutorial parts 1, 2, 3, and 4.

- App: http://prabhjeet-polls-2570.us-east-2.elasticbeanstalk.com/polls/
- GitHub: https://github.com/prabhjeet2570-spec/django-application

## Run locally

Use Python 3.12 or newer.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_polls
python manage.py createsuperuser
python manage.py runserver
```

Create your own admin credentials privately when prompted. Open `/polls/` to vote and `/admin/` to manage questions. Tutorial progress is documented in [TUTORIAL.md](TUTORIAL.md).

## Verify

```bash
python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for the existing Elastic Beanstalk environment in us-east-2. Deployment runs migrations, creates sample polls, and collects admin static files. Sample data matches the final part-2 exercise: “What’s up?” with “Not much” and “The sky”. Previous custom demo questions are removed by migrations; polls created by the user are retained.

Submit the public app URL and an accessible repository URL on Brightspace. Repository visibility must be checked separately before submission.
