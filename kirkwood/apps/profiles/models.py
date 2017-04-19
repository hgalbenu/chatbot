import uuid

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from ..common.model_fields import LongCharField
from ..common.utils import get_number

from .heavenly import Heavenly
from .intercom import Intercom


class UserProfile(TimeStampedModel, Heavenly, Intercom):
    # TODO: This is going to be nullable for now, since we won't be using auth just yet - make non nullable
    user = models.OneToOneField(User, null=True, unique=True, verbose_name='user', related_name='user_profile')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = LongCharField(_('session id'), unique=True, default=uuid.uuid4)

    botId = models.PositiveIntegerField(_('bot id'), default=33251)

    # TODO: Should probably remove this from here, duplicated from user for easier handling
    email = models.EmailField(_('email address'), blank=True, null=True, max_length=2048)

    knowWhereToStart = LongCharField(_('know where to start'), blank=True, null=True)
    totalDebt = LongCharField(_('total debt'), blank=True, null=True)
    averageInterestRate = LongCharField(_('average interest rate'), blank=True, null=True)
    monthlyDebtPayments = LongCharField(_('monthly debt payments'), blank=True, null=True)
    incomeYN = LongCharField(_('income YN'), blank=True, null=True)
    incomeAmount = LongCharField(_('income amount'), blank=True, null=True)
    incomeConsistency = LongCharField(_('income consistency'), blank=True, null=True)
    situationDetail = LongCharField(_('situation detail'), blank=True, null=True)
    is_married = models.NullBooleanField(_('is married'), blank=True, null=True)
    houseHoldSize = LongCharField(_('household size'), blank=True, null=True)
    homeEquity = LongCharField(_('home equity'), blank=True, null=True)
    ownHome = LongCharField(_('own home'), blank=True, null=True)
    behindOnPayments = LongCharField(_('behind on payments'), blank=True, null=True)
    daysPastDue = LongCharField(_('days past due'), blank=True, null=True)
    firstName = LongCharField(_('first name'), blank=True, null=True)
    questionConsultation = LongCharField(_('question consultation'), blank=True, null=True)
    state = LongCharField(_('state'), blank=True, null=True)
    phoneOrEmail = LongCharField(_('phone or email'), blank=True, null=True)
    phone = LongCharField(_('phone'), blank=True, null=True)

    basic_hardship = LongCharField(_('basic hardship'), blank=True, null=True)
    employment_status = LongCharField(_('employment status'), blank=True, null=True)

    additional_income = models.NullBooleanField(_('additional income'), blank=True, null=True)
    additional_income_consistent = models.NullBooleanField(_('additional income consistent'), blank=True, null=True)
    additional_income_amount = LongCharField(_('additional income amount'), blank=True, null=True)

    credit_score_importance = LongCharField(_('credit score importance'), blank=True, null=True)
    needs_future_student_loan = LongCharField(_('needs future student loan'), blank=True, null=True)
    needs_future_auto_loan = LongCharField(_('needs future auto loan'), blank=True, null=True)
    needs_future_mortgage = LongCharField(_('needs future mortgage'), blank=True, null=True)
    revenue_potential = models.DecimalField(_('revenue potential'), decimal_places=2, max_digits=18, blank=True, null=True)

    # These timestamps will probably need to be modelled in a more robust fashion,
    # but for now, this is by far the easiest solution which also allows easy
    # filtering/reporting/etc to be performed using Intercom/Metabase
    # User status timestamps
    waiting_data_review_at = models.DateTimeField(blank=True, null=True)
    waiting_expert_review_at = models.DateTimeField(blank=True, null=True)
    waiting_user_schedule_at = models.DateTimeField(blank=True, null=True)
    waiting_user_answers_at = models.DateTimeField(blank=True, null=True)
    question_answered_at = models.DateTimeField(blank=True, null=True)
    waiting_consultation_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    user_status = LongCharField(_('conclusion'), blank=True, null=True, default="None")
    # Expert conclusion timestamps
    no_action_required_at = models.DateTimeField(blank=True, null=True)
    crn_settlement_at = models.DateTimeField(blank=True, null=True)
    settlement_referral_at = models.DateTimeField(blank=True, null=True)
    bankruptcy_referral_at = models.DateTimeField(blank=True, null=True)
    student_loan_referral_at = models.DateTimeField(blank=True, null=True)
    debt_defense_referral_at = models.DateTimeField(blank=True, null=True)
    credit_counseling_referral_at = models.DateTimeField(blank=True, null=True)
    other_action_required_at = models.DateTimeField(blank=True, null=True)
    conclusion = LongCharField(_('conclusion'), blank=True, null=True, default="None")

    # Will be included in emails sent due to status changes defined above
    expert_note = LongCharField(_('expert note'), blank=True, null=True)
    # TODO: This is a quick hack to make Intercom emails easier to send, since custom fields can't contain any
    # formatted text. This should probably be a foreign key.
    expert_note_template_name = LongCharField(_('expert note template name'), blank=True, null=True, default="None")

    intercom_user_id = LongCharField(_('intercom user id'), blank=True, null=True)

    heavenly_request = JSONField(_('heavenly_request'), blank=True, null=True)
    heavenly_response = JSONField(_('heavenly_response'), blank=True, null=True)
    action = LongCharField(_('action'), blank=True, null=True)

    heavenly_updated_at = models.DateTimeField(blank=True, null=True)

    current_job = models.OneToOneField('jobs.Job', blank=True, null=True, verbose_name=_('current job'),
                                       related_name='current_for')
    current_debt = models.OneToOneField('debts.Debt', blank=True, null=True, verbose_name=_('current job'),
                                        related_name='current_for')

    @property
    def created_at(self):
        return self.created

    @property
    def updated_at(self):
        return self.modified

    @property
    def profile_url(self):
        return '{}/profile/{}'.format(settings.KIRKWOOD_URL, self.id)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @full_name.setter
    def full_name(self, value):
        user = self.user
        first_name, last_name = value.split(' ')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    def save(self, **kwargs):
        # TODO: Refactor this
        boolean_mapping = {
            'yes': True,
            'no': False
        }

        for field_name in ['is_married', 'additional_income_consistent', 'additional_income_amount']:
            value = str(getattr(self, field_name)).lower()
            if value in boolean_mapping.keys():
                setattr(self, field_name, boolean_mapping[value])

        setattr(self, 'revenue_potential', get_number(getattr(self, 'revenue_potential')))
        return super(UserProfile, self).save(**kwargs)

    def __str__(self):
        return 'id: {} email: {}'.format(self.id, self.email)


class ExpertNoteTemplate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = LongCharField(_('name'), blank=True, null=True)
    body = LongCharField(_('body'), blank=True, null=True)

    def __str__(self):
        return 'ExpertNoteTemplate ' + self.name
