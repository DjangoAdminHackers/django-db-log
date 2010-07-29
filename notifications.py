import admin_notifications

def dblog_app_block():
    return """<tr><th scope="row" colspan="3"><a href="/admin/djangodblog/report/?timespan=4">Broken Link Error Report</a><br /></th></tr>"""

admin_notifications.register({
    'app_blocks': [
        ("Tools and Settings", dblog_app_block,),
    ],
    })