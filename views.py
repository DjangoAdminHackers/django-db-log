# -*- coding: utf-8

import datetime
import os
import traceback

from django.contrib.auth.decorators import login_required
from django.db.models import connection
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template


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

    # Use pure ORM to be compaible with Django 1.0.x which doesn't support aggregates
    cursor = connection.cursor()

    date_clause = get_query_date_clause(active_timespan)

    if active_rownum == 7:
        limit_clause = ''
    else:
        limit_clause = "LIMIT %s" % ['25', '50', '100', '200', '500', '1000', 'ALL'][active_rownum-1]

    if active_tab == 1:
        column_headers = ('Page', 'Num. of errors')
        sql_statement = r"SELECT url, COUNT(*) AS ct FROM djangodblog_error WHERE class_name='Http404' %s GROUP BY url ORDER BY ct DESC %s"
    elif active_tab == 2:
        column_headers = ('Incoming link', 'Num. of errors')
        sql_statement = r"SELECT referrer, COUNT(*) AS ct FROM djangodblog_error WHERE class_name='Http404' %s GROUP BY referrer ORDER BY ct DESC %s"
    else:  # if active_tab == 3:
        column_headers = ('Page', 'Incoming link', 'Num. of errors')
        sql_statement = r"SELECT url, referrer, COUNT(*) AS ct FROM djangodblog_error WHERE class_name='Http404' %s GROUP BY url, referrer ORDER BY ct DESC %s"

    cursor.execute(sql_statement % (date_clause, limit_clause)) # No SQL-injection problem + we don't need quoting here, so Python formatting is OK

    timespans = ['Today', 'Yesterday', 'Last 7 days', 'Last 30 days', 'Last 365 days', 'All the time']

    return HttpResponse(get_template('admin/aggregate_list.html').render(RequestContext(request, {
        'active_tab': active_tab,
        'tabs': ['by requested page', 'by requesting page', 'both',],

        'active_timespan': active_timespan,
        'timespans': timespans,
        'active_timespan_description': timespans[active_timespan],
        
        'active_rownum': active_rownum,
        'rownums': ['25', '50', '100', '200', '500', '1000', 'ALL'],

        'column_headers': column_headers,
        'results': cursor.fetchall(),

        'root_path': '/admin/' # To make Django base template happy and 'Change password'/'Logout/ links work

    })))
