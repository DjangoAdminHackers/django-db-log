from django.contrib import admin
from models import Error

class ErrorAdmin(admin.ModelAdmin):
    list_display    = ('class_name', 'message', 'datetime', 'url', 'referrer', 'server_name')
#    list_filter     = ('class_name', 'datetime', 'server_name', 'referrer', )
    ordering        = ('-datetime',)
    search_fields = ('message', 'server_name', 'url', 'referrer',)
    
admin.site.register(Error, ErrorAdmin)
