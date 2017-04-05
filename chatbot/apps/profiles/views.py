from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import UserCreationForm


class MyProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, request, **kwargs):
        return {
            'user': request.user
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class RegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)
