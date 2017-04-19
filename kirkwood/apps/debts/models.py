import uuid
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from ..common.model_fields import LongCharField
from ..common.utils import get_number


class Debt(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creditor_name = LongCharField(_('creditor name'), blank=True, null=True)
    collection_agency = LongCharField(_('collection agency'), blank=True, null=True)
    type = LongCharField(_('type'), blank=True, null=True)
    status = LongCharField(_('status'), blank=True, null=True)
    money_movement = LongCharField(_('money movement'), blank=True, null=True)

    last_paid_at = models.DateField(_('last paid at'), blank=True, null=True)

    balance = models.DecimalField(_('balance'), decimal_places=2, max_digits=18, blank=True, null=True)
    interest_rate = models.DecimalField(_('interest rate'), decimal_places=2, max_digits=18, blank=True, null=True)
    monthly_payment = models.DecimalField(_('monthly payment'), decimal_places=2, max_digits=18, blank=True, null=True)

    user_profile = models.ForeignKey('profiles.UserProfile', verbose_name=_('user profile'), related_name='debts',
                                     help_text=_('The user profile that this debt belongs to.'))

    @property
    def days_behind(self):
        if self.last_paid_at is None:
            return None
        return (datetime.date.today() - self.last_paid_at).days

    def save(self, **kwargs):
        # TODO: Refactor this
        setattr(self, 'balance', get_number(getattr(self, 'balance')))
        setattr(self, 'interest_rate', get_number(getattr(self, 'interest_rate')))
        setattr(self, 'monthly_payment', get_number(getattr(self, 'monthly_payment')))
        return super(Debt, self).save(**kwargs)

    def __str__(self):
        return 'Debt ' + self.creditor_name

