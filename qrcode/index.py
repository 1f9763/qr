#-*- coding:utf-8 -*-
import django
import os
import sys
# def app(environ, start_response):
#     status = '200 OK'
#     headers = [('Content-type', 'text/html')]
#     start_response(status, headers)
#     body=["Welcome to Baidu Cloud!\n"]
#     return django.get_version()
#
# from bae.core.wsgi import WSGIApplication
# application = WSGIApplication(app)

os.environ['DJANGO_SETTINGS_MODULE'] = 'learnbae.settings'

path = os.path.dirname(os.path.abspath(__file__)) + '/learnbae'
if path not in sys.path:
  sys.path.insert(1, path)

from django.core.wsgi import get_wsgi_application
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(get_wsgi_application())

