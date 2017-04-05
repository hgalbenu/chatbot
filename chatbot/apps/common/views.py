# Create your views here.

from django.views.generic import View, TemplateView
from django.http import HttpResponse


class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, request, **kwargs):
        return {
            'user': request.user
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class MotionAIWebHook(View):
    def post(self, request):
        print '*' * 9000
        return HttpResponse(status=200, content='')
