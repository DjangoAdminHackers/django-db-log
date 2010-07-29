from django.contrib import admin
from models import Error
from models import Report

class ErrorAdmin(admin.ModelAdmin):
    name = 'Tools and Settings'
    list_display    = ('class_name', 'message', 'datetime', 'url', 'referrer', 'server_name', 'redirected', )
    list_filter     = ('class_name', 'server_name', 'redirected', )
    date_hierarchy = 'datetime'
    ordering        = ('-datetime',)
    search_fields = ('message', 'server_name', 'url', 'referrer',)
    
admin.site.register(Error, ErrorAdmin)
