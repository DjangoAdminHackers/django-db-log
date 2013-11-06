django-db-log
=============

Forked from dcramer's django-db-log.

Installation
------------
    
    MIDDLEWARE_CLASSES = (
        ...
        'djangodblog.middleware.DBLogMiddleware',
    )

    INSTALLED_APPS = (
        ...
        'django.contrib.redirect'
        'djangodblog',
        ...
    )

Then

    ./manage.py migrate


