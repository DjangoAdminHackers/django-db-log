# -*- coding: utf-8

import datetime
import os
import traceback
import urllib2
try:
    import simplejson
except:
    from django.utils import simplejson

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import connection
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site

from models import Error

FULL_SITE_URL = 'http://'+settings.SITE_DOMAIN

def get_query_date_clause(num):
    date_clause = ""

    if num == 0: # Today
        date_clause = "AND DATE(datetime) = CURDATE()"
    elif num == 1: # Yesterday
        date_clause = "AND DATE(datetime) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
    elif num in [2, 3, 4]:  # last 7, 30, 365 days
        date_clause = "AND DATE(datetime) >= DATE_SUB(CURDATE(), INTERVAL %d DAY)" % [7, 30, 365][num-2]

    return date_clause

def coerce_int(input, max_val, min_val=0, default_val=1):
    try:
        ret = max(min_val, min(max_val, int(input)))
    except (ValueError, TypeError):
        ret = default_val

    return ret


def view_admin_aggregates_customer(request):
    if not request.user.is_staff:
        return HttpResponse('You are no allowed to browse this page!', status=403)

    active_tab = coerce_int(
        input=request.GET.get('tab', 1),
        max_val=3,
    )
    active_timespan = coerce_int(
        input=request.GET.get('timespan', 5),
        max_val=5
    )
    active_rownum = coerce_int(
        input=request.GET.get('rownum', 1),
        max_val=7
    )
    active_redirected = coerce_int(
        input=request.GET.get('redirected', 1),
        max_val=3
    )

    # Use pure ORM to be compaible with Django 1.0.x which doesn't support aggregates
    cursor = connection.cursor()

    date_clause = get_query_date_clause(active_timespan)

    if active_rownum == 7:
        limit_clause = ''
    else:
        limit_clause = "LIMIT %s" % ['25', '50', '100', '200', '500', '1000', 'ALL'][active_rownum-1]

    redirected_choices = ['All', 'True', 'False']
    verbose_redirected_choices = ['All', 'Yes', 'No']
    if active_redirected == 1:
        redirected_clause = ''
    else:
        redirected_clause = 'AND redirected = %s' % redirected_choices[active_redirected-1]

    if active_tab == 1:
        column_headers = ('Page', 'Num. of errors', 'Fix')
        sql_statement = r"SELECT url, COUNT(*) AS ct, 0, redirected FROM djangodblog_error WHERE class_name='Http404' %s %s GROUP BY url ORDER BY ct DESC %s"
    elif active_tab == 2:
        column_headers = ('Incoming link', 'Num. of errors')
        sql_statement = r"SELECT referrer, COUNT(*) AS ct FROM djangodblog_error WHERE class_name='Http404' %s %s GROUP BY referrer ORDER BY ct DESC %s"
    else:  # if active_tab == 3:
        column_headers = ('Page', 'Incoming link', 'Num. of errors', 'Fix')
        sql_statement = r"SELECT url, COUNT(*) AS ct, referrer, redirected FROM djangodblog_error WHERE class_name='Http404' %s %s GROUP BY url, referrer ORDER BY ct DESC %s"

    cursor.execute(sql_statement % (redirected_clause, date_clause, limit_clause)) # No SQL-injection problem + we don't need quoting here, so Python formatting is OK

    timespans = ['Today', 'Yesterday', 'Last 7 days', 'Last 30 days', 'Last 365 days', 'All the time']

    return HttpResponse(get_template('admin/aggregate_list.html').render(RequestContext(request, {
        'active_tab': active_tab,
        'tabs': ['by requested page', 'by requesting page', 'both',],

        'active_timespan': active_timespan,
        'timespans': timespans,
        'active_timespan_description': timespans[active_timespan],
        
        'active_rownum': active_rownum,
        'rownums': ['25', '50', '100', '200', '500', '1000', 'ALL'],

        'active_redirected': active_redirected,
        'redirected_choices':verbose_redirected_choices, 

        'column_headers': column_headers,
        'results': cursor.fetchall(),

        'root_path': '/admin/' # To make Django base template happy and 'Change password'/'Logout/ links work

    })))
    
class RedirectForm(forms.ModelForm):
    
    #site = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Redirect
        widgets = { 'new_path' : forms.TextInput(), }
        
def trim_host(url):
    if url:
        return url.replace(FULL_SITE_URL, '')
    else:
        return url

def create_redirect(request):
    
    if request.method == 'POST':
        
        next = request.GET['next']
        form = RedirectForm(request.POST)
        if form.is_valid():
            
            redirect = form.save()
            
            all_errors = Error.objects.filter(url = FULL_SITE_URL+form.cleaned_data['old_path']).update(redirected = True)
            request.user.message_set.create(message="Successfully created a redirect from %s to %s" % (redirect.old_path, redirect.new_path))
            return HttpResponseRedirect(next)
            
    else:
        
        old_path = request.GET.get('old_path', None)
        
        url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+old_path)
        
        response = urllib2.urlopen(urllib2.Request(url, None, {'Referer': 'localhost'}))
        try:
            results = simplejson.load(response)['responseData']['results']
            suggested_urls = [trim_host(x['url']) for x in results if x['url'].startswith(FULL_SITE_URL)]
            new_path = suggested_urls[0]
        except:
            new_path = None

        form = RedirectForm(instance = Redirect(
            old_path=trim_host(old_path),
            new_path=trim_host(new_path),
            site=Site.objects.all()[0]),
        )

    context = {
        'form': form,
        'old_url': trim_host(old_path),
        'new_url': new_path,
        'next': request.META.get("HTTP_REFERER", None),
        'suggested_urls': suggested_urls[1:],
        'full_site_url': FULL_SITE_URL,
    }
    
    return render_to_response('admin/create_redirect.html', context, RequestContext(request))
