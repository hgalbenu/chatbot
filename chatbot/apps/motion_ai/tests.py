from decimal import Decimal
from ddt import ddt, data, unpack

from django.test import TestCase
from django.conf import settings

from chatbot.apps.profiles.models import UserProfile
from ..motion_ai.models import MotionAI

SESSION_ID = '123'


@ddt
class MotionAIWebHookFormTestCase(TestCase):
    @data(
        (502697, 'a@getfinguide.com', 'a@getfinguide.com', '1 - Waiting Data Review'),  # email
        (478903, 'Yes', True, 'None'), (478903, 'yes', True, 'None'),  # is_married
        (478903, 'No', False, 'None'), (478903, 'no', False, 'None')
    )
    @unpack
    def test_motion_user(self, module_id, reply, expected, expected_user_status):
        bot_id = list(settings.MOTION_AI_MODULE_MAPPING.keys())[2]
        module_field = settings.MOTION_AI_MODULE_MAPPING.get(bot_id)['User'].get(module_id)
        result = self._send_motion_request(bot_id, module_id, reply)

        self.assertEqual(result.status_code, 200)
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        self.assertEqual(getattr(user_profile, module_field), expected)

        # User should also have his user_status set to '1 - Waiting data review'
        # if the email is provided, or 'None' otherwise.
        self.assertEqual(user_profile.user_status, expected_user_status)

    def test_motion_debt(self):
        # Create user
        bot_id = list(settings.MOTION_AI_MODULE_MAPPING.keys())[2]
        user_email_module_id = 502697
        user_result = self._send_motion_request(bot_id, user_email_module_id, 'a@getfinguide.com') # create user
        self.assertEqual(user_result.status_code, 200)

        # Create first debt
        debt_creditor_module_id = 478927
        creditor_name = 'chase'
        debt_result = self._send_motion_request(bot_id, debt_creditor_module_id, creditor_name) # create debt
        self.assertEqual(debt_result.status_code, 200)
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        first_debt = user_profile.current_debt
        self.assertEqual(first_debt.creditor_name, creditor_name)

        # Update first debt
        debt_interest_rate_module_id = 478933
        interest_rate = '20%'
        debt_result = self._send_motion_request(bot_id, debt_interest_rate_module_id, interest_rate) # create debt
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        second_debt = user_profile.current_debt
        self.assertEqual(second_debt.interest_rate, Decimal(20))
        self.assertEqual(first_debt.id, second_debt.id)

        # Create second debt
        second_creditor_name = 'wells fargo'
        debt_result = self._send_motion_request(bot_id, debt_creditor_module_id, second_creditor_name) # create debt
        self.assertEqual(debt_result.status_code, 200)
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        third_debt = user_profile.current_debt
        self.assertEqual(third_debt.creditor_name, second_creditor_name)
        self.assertNotEqual(first_debt.id, third_debt.id)

        # Update second debt
        debt_balance_module_id = 478929
        second_balance = '$10,000.01 and change'
        debt_result = self._send_motion_request(bot_id, debt_balance_module_id, second_balance) # update balance
        self.assertEqual(debt_result.status_code, 200)
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        third_debt = user_profile.current_debt
        self.assertEqual(third_debt.creditor_name, second_creditor_name)
        self.assertEqual(third_debt.balance, round(Decimal(10000.01), 2))

        # Create job
        job_employer_name_module_id = 478771
        first_job_employer_name = 'Google'
        debt_result = self._send_motion_request(bot_id, job_employer_name_module_id, first_job_employer_name) # create job
        self.assertEqual(debt_result.status_code, 200)
        user_profile = UserProfile.objects.filter(session_id=SESSION_ID).first()
        first_job = user_profile.current_job
        self.assertEqual(first_job.employer_name, first_job_employer_name)

    def test_motion_raw(self):
        bot_id = list(settings.MOTION_AI_MODULE_MAPPING.keys())[0]
        module_id = 402680
        reply = 'test'
        module_field = settings.MOTION_AI_MODULE_MAPPING.get(bot_id)['User'].get(module_id)
        result = self._send_motion_request(bot_id, module_id, reply)
        self.assertEqual(result.status_code, 200)

        motion_ai = MotionAI.objects.filter(session_id=SESSION_ID).first()
        data = self._motion_data(bot_id, module_id, reply)
        self.assertEqual(motion_ai.raw_data, data)

    def _send_motion_request(self, bot_id, module_id, reply):
        data = self._motion_data(bot_id, module_id, reply)
        return self.client.post('/webhook/', data=data)

    def _motion_data(self, bot_id, module_id, reply):
        data = {
            'secret': settings.MOTION_AI_WEBHOOK_SECRET,
            'botID': str(bot_id),
            'to': str(bot_id),
            'moduleID': str(module_id),
            'session': SESSION_ID,
            'reply': reply
        }
        return data
