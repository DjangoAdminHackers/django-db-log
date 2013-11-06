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
    ./manage.py migrate

Upgrading from pre-migrations
-----------------------------

    ./manage.py migrate djangodblog 0001 --fake
    ./manage.py migrate djangodblog
