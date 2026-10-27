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

Service configuration:

1. Travis CI builds pushes and pull requests for `prabhjeet2570-spec/django-polls`; Coveralls receives the coverage reports.
2. `EB_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` are hidden Travis variables scoped to `main`. The dedicated `django-polls-travis-deploy` identity can upload polls source bundles and deploy versions to this environment. Sharing encrypted variables with forked pull requests is disabled. Never use root credentials or commit secrets.
3. Coveralls uses its Travis integration without a repository token.
4. GitHub protects `main` with the **Travis CI - Pull Request** check from the Travis CI app, requires branches to be up to date, and applies these requirements to administrators.

For assignment 6.4, submit the Travis dashboard, live app, and GitHub repository URLs after verifying the hosted build and automatic deployment.

## AWS deployment

The app runs on a single Elastic Beanstalk instance in `us-east-2`. `Procfile` starts Gunicorn, WhiteNoise serves static files, and the deployment hook applies migrations, creates sample polls, and collects static files.

Create a source bundle from committed code:

```bash
git archive --format=zip --output=../django-polls.zip HEAD
```

Upload the bundle to the Python Elastic Beanstalk environment. Set `DJANGO_SECRET_KEY` to a private random value and `DJANGO_ALLOWED_HOSTS` to the environment's hostname. `.ebextensions/django.config` sets the remaining deployment defaults. `.env.example` lists environment variables; Django does not load this file automatically.

Votes are stored in SQLite: `db.sqlite3` locally and `/var/app/data/db.sqlite3` on AWS. Redeploying on the same instance preserves the database; replacing or terminating the instance can remove it. Running `seed_polls` again preserves existing vote counts.
