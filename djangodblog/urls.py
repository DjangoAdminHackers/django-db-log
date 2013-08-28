try:
    from django.conf.urls.defaults import *
except:
    from django.conf.urls import *

urlpatterns = patterns('djangodblog.views',
   (r'^report/$', 'view_admin_aggregates_customer'),
   (r'^create_redirect/$', 'create_redirect'),
)