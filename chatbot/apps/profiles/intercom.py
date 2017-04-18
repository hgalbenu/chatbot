import json
import time

from django.conf import settings


class Intercom(object):

    def _intercom_custom_attributes(self):
        user_dict = self.__dict__.copy()
        for excluded_attr in ['_sa_instance_state', 'heavenly_request', 'heavenly_response', 'current_debt_id', 'current_debt', 'debts', 'current_job_id', 'current_job', 'jobs']:
            user_dict.pop(excluded_attr, None)
        user_dict['id'] = str(self.id)
        for c in ['updated_at', 'created_at', 'heavenly_updated_at', 'no_action_required_at', 'crn_settlement_at', 'settlement_referral_at',
                  'bankruptcy_referral_at', 'student_loan_referral_at', 'debt_defense_referral_at', 'credit_counseling_referral_at',
                  'other_action_required_at', 'waiting_data_review_at', 'waiting_expert_review_at', 'waiting_user_schedule_at',
                  'waiting_user_answers_at', 'question_answered_at', 'waiting_consultation_at', 'completed_at']:
            user_dict[c] = time.mktime(user_dict[c].timetuple()) if user_dict[c] else None
        user_dict['profile_url'] = self.profile_url
        direct_attrs = (
            'email',
            'fistName',
            'phone'
        )
        user_dict = {key: value for key, value in user_dict.items() if key not in direct_attrs}
        custom_attributes = json.loads(json.dumps(user_dict))
        return self._sanitize_intercom(custom_attributes)

    def _intercom_attributes(self):
        return self._sanitize_intercom({
            'email': self.email,
            'name': self.firstName,
            'phone': self.phone
        })

    def _sanitize_intercom(self, data):
        def _sanitize_value(val):
            return val[:255] if isinstance(val, str) else val
        return {k: _sanitize_value(v) for k, v in data.items()}

    def _intercom_client(self):
        from intercom.client import Client
        token = settings.INTERCOM_TOKEN
        if not token:
            return
        intercom = Client(personal_access_token=token)
        return intercom

    def delete_intercom(self):
        from intercom import errors as IntercomErrors
        if not self.intercom_user_id:
            print('Intercom delete - no intercom_user_id')
            return
        intercom = self._intercom_client()
        if not intercom:
            return
        try:
            response = intercom.users.submit_bulk_job(delete_items=[{'id': self.intercom_user_id}])
            print('Intercom delete', response)
        except IntercomErrors.IntercomError as err:
            print('Intercom delete error', err)

    def to_intercom(self):
        from intercom import errors as IntercomErrors
        """
        Sends the full user data to intercom
        """
        if not self.email:
            return

        intercom = self._intercom_client()
        if not intercom:
            return

        attributes = self._intercom_attributes()
        custom_attributes = self._intercom_custom_attributes()
        intercom_payload = {**attributes, **{'custom_attributes': custom_attributes}}
        print('Intercom', intercom_payload)
        intercom_user = None
        try:
            intercom_user = intercom.users.find(email=self.email)
            for key, value in attributes.items():
                setattr(intercom_user, key, value)
            for key, value in custom_attributes.items():
                intercom_user.custom_attributes[key] = value
            intercom.users.save(intercom_user)
        except IntercomErrors.ResourceNotFound:
            intercom_user = intercom.users.create(**intercom_payload)
            self._create_intercom_note()
        except IntercomErrors.IntercomError as err:
            print('Intercom error', err)
        if intercom_user:
            self.intercom_user_id = intercom_user.id

    def _create_intercom_note(self):
        if not self.situationDetail:
            return
        intercom = self._intercom_client()
        if not intercom:
            return
        note = intercom.notes.create(
            body='situationDetail: ' + self.situationDetail,
            email=self.email)

    @property
    def intercom_url(self):
        if not self.intercom_user_id:
            return None
        intercom_app_id = settings.INTERCOM_APP_ID
        return 'https://app.intercom.io/a/apps/{}/users/{}/all-conversations'.format(intercom_app_id, self.intercom_user_id)