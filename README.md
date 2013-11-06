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

Replaying Requests
------------------

It may be desirable to "replay" requests in order to reproduce errors (either
locally or on an live site).

*This functionality requires `requests` of at least version 2.0 to be
installed.*

To do this, navigate to the desired error in the admin, and copy the "portable
request" Base64 string into clipboard.

Now, type this at the command line:

    ./manage.py replay_error localhost:8000 <paste string here>

And hit enter. The output will be returned to the console.


Upgrading from pre-migrations
-----------------------------

    ./manage.py migrate djangodblog 0001 --fake
    ./manage.py migrate djangodblog
