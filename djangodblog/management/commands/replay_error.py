import sys
from django.core.management.base import BaseCommand
import base64
import json

try:
    from requests import Request, Session
except ImportError:
    print "Replaying errors requires requests. `pip install requests`"
    sys.exit(-1)

class Command(BaseCommand):
    def handle(self, *args, **options):
        s = Session()
        if len(args) < 2:
            print "Usage: replay_error <host:port> <portable request>"
            sys.exit(1)

            # self.request('GET', '{base_url}/{url}'.format(
            #     base_url=self.base_url.rstrip('/'),
            #     url=url.lstrip('/'),
            # ),
            # params=params or {},
            # headers=self.base_headers,
            # cookies={
            #     'token': self.token or '',
            # }

        portable = json.loads(base64.b64decode(args[1]))
        req = Request(
            portable['method'],
            'http://{host}{path}'.format(
                host=args[0],
                path=portable['path'],
            ),
            params=portable['get'],
            data=portable['post'],
            cookies=portable['cookies'],
        ).prepare()
        res = s.send(req)
        print res.content
