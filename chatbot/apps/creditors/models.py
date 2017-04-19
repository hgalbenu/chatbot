import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from ..common.model_fields import LongCharField


class Creditor(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = LongCharField(_('name'), blank=True, null=True)
    phone = LongCharField(_('phone'), blank=True, null=True)

    total_debt = models.DecimalField(decimal_places=2, max_digits=25, blank=True, null=True)
    settlement_target_pre = models.DecimalField(_('settlement target pre'), decimal_places=2, max_digits=5, blank=True, null=True)
    settlement_target_post = models.DecimalField(_('settlement target post'), decimal_places=2, max_digits=5, blank=True, null=True)
    risk_level = models.PositiveIntegerField(_('risk level'), blank=True, null=True)

    def __str__(self):
        return 'Creditor ' + self.name
