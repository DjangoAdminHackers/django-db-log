from django.conf.urls.defaults import *

urlpatterns = patterns('djangodblog.views',
   (r'^error/$', 'view_admin_aggregates_customer'),
)