import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from ..common.model_fields import LongCharField


class Job(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employer_name = LongCharField(_('employer name'), blank=True, null=True)
    employment_length = LongCharField(_('employment length'), blank=True, null=True)
    income_consistency = LongCharField(_('income consistency'), blank=True, null=True)

    income = models.DecimalField(_('income'), decimal_places=2, max_digits=18, blank=True, null=True)

    user_profile = models.ForeignKey('profiles.UserProfile', verbose_name=_('user profile'), related_name='jobs',
                                     help_text=_('The user profile that this job belongs to.'))

    def __str__(self):
        return 'Job ' + self.employer_name
