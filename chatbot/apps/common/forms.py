from django import forms
from django.conf import settings

from chatbot.apps.profiles.constants import MODULE_ID_TO_FIELD_MAPPING
from chatbot.apps.profiles.models import UserProfile


class MotionAIWebHookForm(forms.Form):
    # camelCase var names are frowned upon in Python, but motion.ai sends the fields as such.
    moduleID = forms.IntegerField()
    replyData = forms.CharField()
    session = forms.CharField()
    secret = forms.CharField()

    def clean_secret(self):
        # Check whether the received secret key corresponds to the one defined for our motion.ai chat bot.
        secret = self.cleaned_data.get('secret')
        if secret != settings.MOTION_AI_SECRET_KEY:
            raise forms.ValidationError('Invalid secret.')
        return secret

    def clean_session(self):
        # Check whether the given session token is valid.
        # The session token will be of the form `{bot_id}_custom_{user_id}`
        session = self.cleaned_data.get('session')
        profile_id = session.split('_')[-1]
        if not UserProfile.objects.filter(id=int(profile_id)).exists():
            raise forms.ValidationError('Invalid session token.')
        return session

    def clean_moduleID(self):
        # Check whether the received module_id is a valid one as defined in module to field mapping.
        module_id = self.cleaned_data.get('moduleID')
        if module_id not in MODULE_ID_TO_FIELD_MAPPING.keys():
            raise forms.ValidationError('Invalid module id.')
        return module_id
