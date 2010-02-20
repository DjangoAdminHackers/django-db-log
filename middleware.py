import traceback
import socket
import warnings

from django.conf import settings
from django.http import Http404
from django.utils.hashcompat import md5_constructor
from django.contrib.redirects.middleware import RedirectFallbackMiddleware

from models import Error

__all__ = ('DBLogMiddleware', 'DBLOG_CATCH_404_ERRORS')

DBLOG_CATCH_404_ERRORS = getattr(settings, 'DBLOG_CATCH_404_ERRORS', False)

class DBLogMiddleware(object):
    def process_exception(self, request, exception):
        if not DBLOG_CATCH_404_ERRORS and isinstance(exception, Http404):
            pass
        server_name = socket.gethostname()
        tb_text     = traceback.format_exc()
        class_name  = exception.__class__.__name__
        checksum    = md5_constructor(tb_text).hexdigest()
        redirected  = False

        if self.covered_by_redirect(request):
            redirected = True

        defaults = dict(
            class_name  = class_name,
            message     = getattr(exception, 'message', ''),
            url         = request.build_absolute_uri(),
            referrer    = request.META.get("HTTP_REFERER", None),
            server_name = server_name,
            traceback   = tb_text,
            redirected  = redirected,
        )

        try:
            Error.objects.create(**defaults)
        except Exception, exc:
            warnings.warn(unicode(exc))

    def covered_by_redirect(self, request):
        class A:pass
        obj = A()
        obj.status_code = 404
        status_code = RedirectFallbackMiddleware().process_response(request, obj).status_code
        if status_code == 301:
            return True
        else:
            return False