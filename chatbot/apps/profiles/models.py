import uuid

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from .heavenly import Heavenly
from .intercom import Intercom


class UserProfile(TimeStampedModel, Heavenly, Intercom):
    user = models.OneToOneField(User, unique=True, verbose_name='user', related_name='user_profile')

    session_id = models.TextField(_('session id'), primary_key=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    botId = models.PositiveIntegerField(_('bot id'), default=33251)

    knowWhereToStart = models.TextField(_('know where to start'), blank=True, null=True)
    totalDebt = models.TextField(_('total debt'), blank=True, null=True)
    averageInterestRate = models.TextField(_('average interest rate'), blank=True, null=True)
    monthlyDebtPayments = models.TextField(_('monthly debt payments'), blank=True, null=True)
    incomeYN = models.TextField(_('income YN'), blank=True, null=True)
    incomeAmount = models.TextField(_('income amount'), blank=True, null=True)
    incomeConsistency = models.TextField(_('income consistency'), blank=True, null=True)
    situationDetail = models.TextField(_('situation detail'), blank=True, null=True)
    is_married = models.NullBooleanField(_('is married'), blank=True, null=True)
    houseHoldSize = models.TextField(_('household size'), blank=True, null=True)
    homeEquity = models.TextField(_('home equity'), blank=True, null=True)
    ownHome = models.TextField(_('own home'), blank=True, null=True)
    behindOnPayments = models.TextField(_('behind on payments'), blank=True, null=True)
    daysPastDue = models.TextField(_('days past due'), blank=True, null=True)
    firstName = models.TextField(_('first name'), blank=True, null=True)
    questionConsultation = models.TextField(_('question consultation'), blank=True, null=True)
    state = models.TextField(_('state'), blank=True, null=True)
    phoneOrEmail = models.TextField(_('phone or email'), blank=True, null=True)
    phone = models.TextField(_('phone'), blank=True, null=True)

    basic_hardship = models.TextField(_('basic hardship'), blank=True, null=True)
    employment_status = models.TextField(_('employment status'), blank=True, null=True)

    additional_income = models.NullBooleanField(_('additional income'), blank=True, null=True)
    additional_income_consistent = models.NullBooleanField(_('additional income consistent'), blank=True, null=True)
    additional_income_amount = models.TextField(_('additional income amount'), blank=True, null=True)

    credit_score_importance = models.TextField(_('credit score importance'), blank=True, null=True)
    needs_future_student_loan = models.TextField(_('needs future student loan'), blank=True, null=True)
    needs_future_auto_loan = models.TextField(_('needs future auto loan'), blank=True, null=True)
    needs_future_mortgage = models.TextField(_('needs future mortgage'), blank=True, null=True)
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
    user_status = models.TextField(_('conclusion'), blank=True, null=True, default="None")
    # Expert conclusion timestamps
    no_action_required_at = models.DateTimeField(blank=True, null=True)
    crn_settlement_at = models.DateTimeField(blank=True, null=True)
    settlement_referral_at = models.DateTimeField(blank=True, null=True)
    bankruptcy_referral_at = models.DateTimeField(blank=True, null=True)
    student_loan_referral_at = models.DateTimeField(blank=True, null=True)
    debt_defense_referral_at = models.DateTimeField(blank=True, null=True)
    credit_counseling_referral_at = models.DateTimeField(blank=True, null=True)
    other_action_required_at = models.DateTimeField(blank=True, null=True)
    conclusion = models.TextField(_('conclusion'), blank=True, null=True, default="None")

    # Will be included in emails sent due to status changes defined above
    expert_note = models.TextField(_('expert note'), blank=True, null=True)
    # TODO: This is a quick hack to make Intercom emails easier to send, since custom fields can't contain any
    # formatted text. This should probably be a foreign key.
    expert_note_template_name = models.TextField(_('expert note template name'), blank=True, null=True, default="None")

    intercom_user_id = models.TextField(_('intercom user id'), blank=True, null=True)

    heavenly_request = JSONField(_('heavenly_request'), blank=True, null=True)
    heavenly_response = JSONField(_('heavenly_response'), blank=True, null=True)
    action = models.TextField(_('action'), blank=True, null=True)

    heavenly_updated_at = models.DateTimeField(blank=True, null=True)

    current_job = models.OneToOneField('jobs.Job', unique=True, verbose_name=_('current job'),
                                       related_name='current_for')
    current_debt = models.OneToOneField('debts.Debt', unique=True, verbose_name=_('current job'),
                                        related_name='current_for')

    @property
    def profile_url(self):
        return '{}/web/profile/{}'.format(settings.KIRKWOOD_URL, self.id)

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

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, value):
        user = self.user
        user.email = value
        user.save()

    def __str__(self):
        return 'id: {} email: {}'.format(self.id, self.email)


class ExpertNoteTemplate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField(_('name'), blank=True, null=True)
    body = models.TextField(_('body'), blank=True, null=True)
