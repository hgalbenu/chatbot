from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from .forms import MotionAIWebHookForm
from chatbot.apps.profiles.models import UserProfile
from chatbot.apps.profiles.constants import MODULE_ID_TO_FIELD_MAPPING


class MotionAIWebHookFormTestCase(TestCase):
    def test_form_errors(self):
        # Required data not sent at all, so form should be invalid
        form_data = {
            'something': 'something'
        }
        form = MotionAIWebHookForm(data=form_data)

        expected_errors = {
            'reply': [u'This field is required.'],
            'secret': [u'This field is required.'],
            'session': [u'This field is required.'],
            'replyData': [u'This field is required.'],
            'moduleID': [u'This field is required.']
        }

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, expected_errors)

        # Try to pass an invalid secret key, invalid session and module id which does not exist.
        form_data = {
            'reply': 'some_raw_reply',
            'secret': 'some_wrong_secret',
            'session': 'some_session_that_does_not_exist',
            'replyData': 'some_reply_data',
            'moduleID': '1234'
        }
        form = MotionAIWebHookForm(data=form_data)

        expected_errors = {
            'secret': [u'Invalid secret.'],
            'session': [u'Invalid session token.'],
            'moduleID': [u'Invalid module id.']
        }
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, expected_errors)

        # Use secret key defined in settings and a correct moduleID. However, the session token can never be actually
        # valid, since we have no users (or profiles) to which it may be linked.
        form_data = {
            'reply': 'some_raw_reply',
            'secret': settings.MOTION_AI_SECRET_KEY,
            'session': 'some_session_that_does_not_exist',
            'replyData': 'some_reply_data',
            'moduleID': MODULE_ID_TO_FIELD_MAPPING.keys()[0]
        }
        form = MotionAIWebHookForm(data=form_data)
        expected_errors = {
            'session': [u'Invalid session token.'],
        }

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, expected_errors)

    def test_form_with_some_correct_data(self):
        # First, create a User and a User Profile.
        test_user = User.objects.create_user(username='test_user', password='pass')
        UserProfile.objects.create(user=test_user)

        form_data = {
            'reply': 'some_raw_reply',
            'secret': settings.MOTION_AI_SECRET_KEY,
            'session': '4411_custom_%s' % str(test_user.user_profile.id),
            'replyData': 'some_reply_data',
            'moduleID': MODULE_ID_TO_FIELD_MAPPING.keys()[0]
        }
        form = MotionAIWebHookForm(data=form_data)

        self.assertTrue(form.is_valid())
