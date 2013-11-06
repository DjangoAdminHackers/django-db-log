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

    ./manage.py syncdb


Upgrades
--------

South is not used. Simply run:

    ./manage.py sqlclear djangodblog | ./manage.py dbshell && ./manage.py syncdb
