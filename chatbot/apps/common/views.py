# Create your views here.
import json
import decimal

from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.utils import timezone

from forms import MotionAIWebHookForm
from chatbot.apps.profiles.models import UserProfile
from chatbot.apps.profiles.constants import MODULE_ID_TO_FIELD_MAPPING


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, request, **kwargs):
        return {
            'user': request.user
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class MotionAIWebHookView(View):
    def post(self, request):
        form = MotionAIWebHookForm(request.POST)
        print form.errors
        if form.is_valid():
            data = form.cleaned_data
            module_id = data['module_id']
            reply_data = data['reply_data']

            if MODULE_ID_TO_FIELD_MAPPING[module_id] == 'total_debt':
                # Convert the string to a Decimal before using the form cleaned_data to update the user's profile.
                reply_data = decimal.Decimal(reply_data)
            if MODULE_ID_TO_FIELD_MAPPING[module_id] == 'date_of_birth':
                reply_data = timezone.datetime.strptime(reply_data, "%Y-%m-%dT%H:%M:%S.%fZ")

            profile = UserProfile.objects.first()
            setattr(profile, MODULE_ID_TO_FIELD_MAPPING[module_id], reply_data)
            profile.save()

            return HttpResponse(status=204)

        # Return form errors as json, mostly for testing.
        return HttpResponse(status=400, content=json.dumps(form.errors), content_type='application/json')
