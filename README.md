# PanaSystem

PanaSystem is an API for grocery stores.

Why PanaSystem? Because my parents own a bakery, so I used a short way of saying that word.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### How to start it

- When you pull/download the project, you have to build the image with docker so:
  ```
      $ docker compose -f local.yml build
  ```
- When docker finish to build the image you have to up the container with this command:
  ```
      $ docker compose -f local.yml up
  ```

### Setting Up Your Users

- To create a **normal user account**, just have to create a superuser account and go to Admin and create an user there.

- To create a **superuser account**, use this command:
```
      $ docker compose -f local.yml run --rm django python manage.py createsuperuser
```
### Migrations

- After you created the image in docker and the user, you have to do migrations with the following command:
  ```
      $ docker compose -f local.yml run --rm django python manage.py makemigrations
      $ docker compose -f local.yml run --rm django python manage.py migrate
  ```
