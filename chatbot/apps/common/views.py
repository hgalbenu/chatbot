from jinja2 import Environment

from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse


# Jinja2 environment config
def environment(**options):
    env = Environment(**options)
    env.globals.update({
       'static': staticfiles_storage.url,
       'url_for': reverse,
    })
    return env


def home_page(request):
    return HttpResponse('kirkwood')
