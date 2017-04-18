import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField


class MotionAI(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session_id = models.TextField(_('session id'), blank=True, null=True)

    bot_id = models.PositiveIntegerField(_('bot id'), blank=True, null=True)
    module_id = models.PositiveIntegerField(_('module id'), blank=True, null=True)

    reply = models.TextField(_('reply'), blank=True, null=True)

    raw_data = JSONField(_('raw data'), blank=True, null=True)

    @classmethod
    def save_data(cls, data):
        return cls.objects.create(
            session_id=data.get('session'),
            bot_id=data.get('botID'),
            module_id=data.get('moduleID'),
            reply=data.get('reply'),
            raw_data=data
        )

    def __str__(self):
        return 'Raw data for - bot %s, module %s, session %s' % (str(self.bot_id), str(self.module_id), self.session_id)