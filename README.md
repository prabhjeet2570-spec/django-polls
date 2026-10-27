# Django polls

[![Build status](https://app.travis-ci.com/prabhjeet2570-spec/django-polls.svg?branch=main)](https://app.travis-ci.com/github/prabhjeet2570-spec/django-polls)
[![Coverage Status](https://coveralls.io/repos/github/prabhjeet2570-spec/django-polls/badge.svg?branch=main)](https://coveralls.io/github/prabhjeet2570-spec/django-polls?branch=main)

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

## Checks and tests

```bash
python -m pip install -r requirements-dev.txt
python -m black --check .
python -m flake8 .
python manage.py check
python manage.py makemigrations --check --dry-run
python -m coverage run manage.py test --noinput
python -m coverage report
```

Run `python -m black .` to format the code before committing. Black and flake8 use an 88-character line limit. Coverage includes the application and project code, excluding tests, migrations, and the ASGI/WSGI launch files.

## Continuous integration

[Travis dashboard](https://app.travis-ci.com/github/prabhjeet2570-spec/django-polls) · [Coveralls](https://coveralls.io/github/prabhjeet2570-spec/django-polls)

`.travis.yml` runs the checks above for pushes and pull requests, then reports coverage to Coveralls. Successful builds on `main` deploy to the existing `django-application-env` Elastic Beanstalk environment in `us-east-2`. Pull request builds do not deploy.

Service setup:

1. Enable `prabhjeet2570-spec/django-polls` in Travis CI and Coveralls. In Travis settings, enable builds for pushes and pull requests.
2. Set `EB_BUCKET_NAME` to the existing Elastic Beanstalk source-bundle bucket. Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as hidden Travis environment variables using a deployment identity restricted to this app and bucket. Never use root credentials or commit secrets. Keep deployment credentials unavailable to pull requests.
3. If Coveralls requires a repository token, add `COVERALLS_REPO_TOKEN` as a hidden Travis environment variable.
4. After a pull request build runs, protect `main` in GitHub and enable **Require status checks to pass before merging**, selecting the Travis CI pull request check.

For assignment 6.4, submit the Travis dashboard, live app, and GitHub repository URLs after verifying the hosted build and automatic deployment.

## AWS deployment

The app runs on a single Elastic Beanstalk instance in `us-east-2`. `Procfile` starts Gunicorn, WhiteNoise serves static files, and the deployment hook applies migrations, creates sample polls, and collects static files.

Create a source bundle from committed code:

```bash
git archive --format=zip --output=../django-polls.zip HEAD
```

Upload the bundle to the Python Elastic Beanstalk environment. Set `DJANGO_SECRET_KEY` to a private random value and `DJANGO_ALLOWED_HOSTS` to the environment's hostname. `.ebextensions/django.config` sets the remaining deployment defaults. `.env.example` lists environment variables; Django does not load this file automatically.

Votes are stored in SQLite: `db.sqlite3` locally and `/var/app/data/db.sqlite3` on AWS. Redeploying on the same instance preserves the database; replacing or terminating the instance can remove it. Running `seed_polls` again preserves existing vote counts.
