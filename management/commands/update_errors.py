from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.contrib.redirects.middleware import RedirectFallbackMiddleware

from djangodblog.models import Error

class ErrorWrapper(object):
    '''
    Wrapper for Error, providing the get_full_path() method. so an Error looks
    like a django.http.HttpRequest for RedirectFallbackMiddleware.process_response()
    '''
    def __init__(self, error):
        self.error = error

    def get_full_path(self):
        path = urlparse(self.error.url).path
        return path

def covered_by_redirect(error_wrapper):
    class A:pass
    obj = A()
    obj.status_code = 404
    status_code = RedirectFallbackMiddleware().process_response(error_wrapper, obj).status_code
    if status_code == 301:
        return True
    else:
        return False

class Command(BaseCommand):
    help = "Update all the Errors. See if the error has been covered by redirect"
    def handle(self, *args, **options):
        print 'Updating error data...'
        all_errors = Error.objects.all()
        redirected_error_ids = []
        for error in all_errors:
            e_wrapper = ErrorWrapper(error)
            if covered_by_redirect(e_wrapper):
                redirected_error_ids.append(error.id)
        Error.objects.filter(id__in=redirected_error_ids).update(redirected = True)
        Error.objects.exclude(id__in=redirected_error_ids).update(redirected = False)
        print 'Done!'
