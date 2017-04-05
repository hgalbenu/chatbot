from django.views.generic import TemplateView


class MyProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, request, **kwargs):
        return {
            'user': request.user
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)
