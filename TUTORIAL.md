# Tutorial progress

## Part 1

Created the project and polls app, wired URL routing, and checked the hello-world response.

## Part 2

Added Question and Choice models and the initial migration. Run `migrate`, `sqlmigrate polls 0001`, and the model API exercises before committing this step.

Create your own local admin login with `python manage.py createsuperuser`, then visit `/admin/`. Credentials must not be committed. The admin initially registers Question as shown in tutorial part 2. The tutorial's inline admin customization belongs to part 7.

## Part 3

Added function views, namespaced templates and named URLs. The index queries the latest five questions and the detail view uses `get_object_or_404`. Results and vote remain placeholders until part 4.

## Part 4

Added the POST voting form, CSRF token, missing-choice error, database-side F-expression increment, results template, and redirect after voting. Converted the function views from the previous step to separate generic index, detail, and results views.

The final views deliberately follow the part-4 query behavior. Future-date filtering is introduced in part 5; admin inlines and search are introduced in part 7 and are outside this assignment.

The part-2 verification creates a local admin superuser privately and checks access to question management. Its credentials are stored outside Git in the workspace rebuild directory. The deployed public app does not publish an admin password.

## Assignment alignment checked October 6, 2026

Compared the application with the official Django 6.1 tutorial parts 1–4:

| Part | Implementation | Evidence in repository |
| --- | --- | --- |
| [1](https://docs.djangoproject.com/en/6.1/intro/tutorial01/) | Project, app, first view and URL routing | `1cc2e14` preserves the hello-world step; later parts replace that view |
| [2](https://docs.djangoproject.com/en/6.1/intro/tutorial02/) | Question/Choice fields, model methods, migrations, database API and Question admin registration | `polls/models.py`, `polls/migrations/0001_initial.py`, `polls/admin.py`; local admin/API previously verified |
| [3](https://docs.djangoproject.com/en/6.1/intro/tutorial03/) | Latest five questions, namespaced templates, named URLs and 404 handling | `71ac96f` preserves function views before the part-4 refactor |
| [4](https://docs.djangoproject.com/en/6.1/intro/tutorial04/) | POST form, CSRF, missing-choice handling, F-expression vote increment, redirect, results and generic views | `polls/views.py`, `polls/urls.py`, three plain templates |

Removed the custom branded layout, stylesheet and external fonts. Templates now use the tutorial's plain list, radio-button form and vote-count results, using the same template fragments as the tutorial. The voting handler uses the tutorial's exception handling and save operation.

Sample question data now follows the tutorial exactly. Automated verification and AWS configuration support the assignment; they are not presented as additional completed tutorial parts. Parts 5 onward are outside the required tutorial scope.

AWS is intentionally terminated at the user's request. Completing the submission still requires redeployment, public URL verification, accessible GitHub code and submission of both URLs on Brightspace. No redeployment is authorized by this code-alignment request.

The final sample data is “What’s up?” with “Not much” and “The sky”. The part-2 exercise creates “Just hacking again” and then deletes it, so it is absent from the final app. Index/detail/results templates and the generic views/vote handler now reproduce the tutorial examples. The seed command is deployment support for recreating that same data, not an extra tutorial feature.

## User-requested sample-data change

The user subsequently requested replacing “What’s up?” with three simple U.S. history trivia questions. Only sample data changed; the tutorial’s views, templates, radio form and vote-count results remain. These are polls: the results show vote counts, and the app does not grade answers or reveal a correct-answer key.
