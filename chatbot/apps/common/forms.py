from django import forms
from django.conf import settings

from chatbot.apps.profiles.constants import MODULE_ID_TO_FIELD_MAPPING


class MotionAIWebHookForm(forms.Form):
    # camelCase var names are frowned upon in Python, but motion.ai sends the fields as such.
    moduleID = forms.IntegerField()
    replyData = forms.CharField(required=False)
    session = forms.CharField()
    secret = forms.CharField()

    def clean(self):
        cleaned_data = super(MotionAIWebHookForm, self).clean()

        # Check whether the received secret key corresponds to the one defined for our motion.ai chat bot.
        secret = cleaned_data.get('secret')
        if secret != settings.MOTION_AI_SECRET_KEY:
            raise forms.ValidationError('Invalid secret.')

        # Check whether the received module_id is a valid one as defined in module to field mapping.
        module_id = cleaned_data.get('moduleID')
        if module_id not in MODULE_ID_TO_FIELD_MAPPING.keys():
            raise forms.ValidationError('Invalid module id.')
