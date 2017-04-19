from datetime import datetime

from django.forms.models import ModelForm
from django.forms import fields, widgets

from .models import UserProfile, ExpertNoteTemplate
from ..common.fields import NameModelChoiceField


# Choices for status change select fields - will map display values to user status timestamp field names.
USER_STATUS_MAPPING = {
    'None': 'None',
    '1 - Waiting Data Review': 'waiting_data_review_at',
    '2 - Waiting Expert Review': 'waiting_expert_review_at',
    '3a - Waiting User Schedule': 'waiting_user_schedule_at',
    '3b - Waiting User Answers': 'waiting_user_answers_at',
    '3c - Question Answered': 'question_answered_at',
    '4 - Waiting Consultation': 'waiting_consultation_at',
    '5 - Completed': 'completed_at',
}
USER_STATUS_CHOICES = {key: key for key in USER_STATUS_MAPPING.keys()}.items()

USER_CONCLUSION_MAPPING = {
    'None': 'None',
    'No Action Required': 'no_action_required_at',
    'CRN Settlement': 'crn_settlement_at',
    'Settlement Referral': 'settlement_referral_at',
    'Bankruptcy Referral': 'bankruptcy_referral_at',
    'Student Loan Referral': 'student_loan_referral_at',
    'Debt Defense Referral': 'debt_defense_referral_at',
    'Credit Counseling Referral': 'credit_counseling_referral_at',
    'Other Action Required': 'other_action_required_at',
}
USER_CONCLUSION_CHOICES = {key: key for key in USER_CONCLUSION_MAPPING.keys()}.items()


class UserProfileForm(ModelForm):
    user_status = fields.ChoiceField(label='User Status', choices=USER_STATUS_CHOICES, required=False)
    conclusion = fields.ChoiceField(label='Conclusion', choices=USER_CONCLUSION_CHOICES, required=False)
    situationDetail = fields.CharField(label='situationDetail', widget=widgets.Textarea(), required=False)
    basic_hardship = fields.CharField(label='basic_hardship', required=False)
    expert_note = fields.CharField(label='expert_note', widget=widgets.Textarea(), required=False)
    expert_note_template_name = NameModelChoiceField(label='Template', required=False,
                                                     queryset=ExpertNoteTemplate.objects.all(),
                                                     empty_label='None', to_field_name="body")
    is_married = fields.NullBooleanField(label='Is married', required=False, widget=widgets.CheckboxInput())
    additional_income = fields.NullBooleanField(label='Additional income', required=False,
                                                widget=widgets.CheckboxInput())
    additional_income_consistent = fields.NullBooleanField(label='Additional income consistent', required=False,
                                                           widget=widgets.CheckboxInput())

    class Meta:
        model = UserProfile
        exclude = [
            'id',
            'session_id',
            'botId',
            'intercom_user_id',
            'heavenly_request',
            'heavenly_response',
            'action',
            'heavenly_updated_at',
            'user',
            'waiting_data_review_at',
            'waiting_expert_review_at',
            'waiting_user_schedule_at',
            'waiting_user_answers_at',
            'question_answered_at',
            'waiting_consultation_at',
            'completed_at',
            'no_action_required_at',
            'crn_settlement_at',
            'settlement_referral_at',
            'bankruptcy_referral_at',
            'student_loan_referral_at',
            'debt_defense_referral_at',
            'credit_counseling_referral_at',
            'other_action_required_at',
        ]

    def save(self, commit=True):
        # Override save in order to populate corresponding status timestamps on user, only if changed.
        selected_user_status_choice = self.cleaned_data.pop('user_status', None)
        selected_conclusion_choice = self.cleaned_data.pop('conclusion', None)
        expert_note_template_name = self.cleaned_data.pop('expert_note_template_name', None)

        if 'user_status' in self.changed_data:
            setattr(self.instance, 'user_status', selected_user_status_choice)

            if selected_user_status_choice != 'None':
                setattr(self.instance, USER_STATUS_MAPPING[selected_user_status_choice], datetime.now())

        if 'conclusion' in self.changed_data:
            setattr(self.instance, 'conclusion', selected_conclusion_choice)

            if selected_conclusion_choice != 'None':
                setattr(self.instance, USER_CONCLUSION_MAPPING[selected_conclusion_choice], datetime.now())

        # Also save expert note template if changed
        if 'expert_note_template_name' in self.changed_data:
            template_name = expert_note_template_name.name if expert_note_template_name is not None else 'None'
            setattr(self.instance, 'expert_note_template_name', template_name)

        return super(UserProfileForm, self).save(commit)
