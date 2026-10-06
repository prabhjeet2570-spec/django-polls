# Elastic Beanstalk deployment

## Account setup

Create and activate your individual account at https://aws.amazon.com/ . Complete billing and identity verification yourself. Sign in and choose a region, `us-east-2`. The new AWS experience manages human access through project team members. Use the authenticated `default` profile; verify that Elastic Beanstalk is available for the project plan before deployment. Do not put AWS keys, passwords, or Django secrets in GitHub.

## Deployment settings

Use a Python 3.12 or newer Elastic Beanstalk platform on Amazon Linux 2023. Create a **single instance** web environment for this class demo.

Set these environment properties before deployment:

- `DJANGO_SECRET_KEY`: a random secret generated locally, never committed.
- `DJANGO_ALLOWED_HOSTS`: your exact Elastic Beanstalk hostname, without a scheme or path.
- `DJANGO_DEBUG`: `false` (also set by `.ebextensions/django.config`).
- `DJANGO_DB_PATH`: `/var/app/data/db.sqlite3` (also set by the config).

Generate a secret locally:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the value directly into AWS environment properties. Do not paste it into chat or documentation.

## Console deployment

Create a zip of the application contents with `manage.py`, `requirements.txt`, and `Procfile` at its root. Include `.ebextensions` and `.platform`; exclude `.git`, `.venv`, local database files, and secrets.

Upload it as the application source bundle when creating the environment, or use **Upload and deploy** for an existing environment. The deployment hook runs migrations, creates sample polls, and collects static files. The app uses Gunicorn and WhiteNoise.

## Optional EB CLI deployment

```bash
python -m pip install -r requirements-dev.txt
eb init
```

Choose your region, application name, and Python platform. Authenticate locally when prompted. Configure environment properties through the AWS Console and launch a single instance environment; thereafter deploy updates with:

```bash
eb deploy
eb status
```

`.ebignore` excludes local tools, databases, and secrets from the upload.

## Verify before submitting

1. Check that environment health is healthy.
2. Open the public `/polls/` URL in a signed-out browser.
3. Open a poll, vote, and check that its count increases on the results page.
4. Verify the CSS and admin login page load.
5. Add the verified URL to README.md and the assignment checklist.
6. Submit the application URL and repository URL on Brightspace.

## Demo database limitation

This single instance demo uses SQLite under `/var/app/data`, outside the deployed code directory, so normal application redeploys preserve votes on the same instance. Instance replacement, environment rebuilds, or termination can remove this data. The deployment hook recreates sample polls when the database is new. Use an external database such as RDS PostgreSQL if durable data or multiple instances are required.

Keep the environment running while the course team grades it. AWS resources may incur charges; terminate them when grading is complete.

## Current deployed environment

- Application: `django-application`
- Environment: `django-application-env`
- Region: `us-east-2`
- AWS CLI profile: `default`
- Platform: Amazon Linux 2023 v4.13.9, Python 3.14
- Compute: single `t3.micro` instance
- Public app: http://prabhjeet-polls-2570.us-east-2.elasticbeanstalk.com/polls/
- Health check: http://prabhjeet-polls-2570.us-east-2.elasticbeanstalk.com/health/
- Instance role/profile: `django-application-eb-ec2`, with `AWSElasticBeanstalkWebTier`
- Database: `/var/app/data/db.sqlite3` on the instance
- Startup: Gunicorn on port 8000, with `PORT=8000` set for the proxy
- Django secret: generated during deployment and set in environment properties; not stored in this repository

Check status:

```bash
aws elasticbeanstalk describe-environments --environment-names django-application-env --region us-east-2 --profile default
```

Keep the environment running until grading is complete. After grading, stop its running resources with:

```bash
aws elasticbeanstalk terminate-environment --environment-name django-application-env --region us-east-2 --profile default
```

Termination deletes the instance and its SQLite database. Application versions in S3 and the instance role remain and can be cleaned up separately after they are no longer needed.
