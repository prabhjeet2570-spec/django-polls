# Django polls

A simple polling app built with Django 6.1, following parts 1–4 of the Django tutorial. Choose an answer, vote, and see the results. The app includes three U.S. history questions with three choices each.

[Live app](http://prabhjeet-polls-2570.us-east-2.elasticbeanstalk.com/polls/) · [Django tutorial](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)

## Run locally

Requires Python 3.12 or newer.

```bash
git clone https://github.com/prabhjeet2570-spec/django-polls.git
cd django-polls
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_polls
python manage.py runserver
```

Open http://127.0.0.1:8000/polls/. To manage questions through Django's admin, run `python manage.py createsuperuser` and visit `/admin/`.

## Tests

```bash
python manage.py test
```

## AWS deployment

The app runs on a single Elastic Beanstalk instance in `us-east-2`. `Procfile` starts Gunicorn, WhiteNoise serves static files, and the deployment hook applies migrations, creates sample polls, and collects static files.

Create a source bundle from committed code:

```bash
git archive --format=zip --output=../django-polls.zip HEAD
```

Upload the bundle to the Python Elastic Beanstalk environment. Set `DJANGO_SECRET_KEY` to a private random value and `DJANGO_ALLOWED_HOSTS` to the environment's hostname. `.ebextensions/django.config` sets the remaining deployment defaults. `.env.example` lists environment variables; Django does not load this file automatically.

Votes are stored in SQLite: `db.sqlite3` locally and `/var/app/data/db.sqlite3` on AWS. Redeploying on the same instance preserves the database; replacing or terminating the instance can remove it. Running `seed_polls` again preserves existing vote counts.
