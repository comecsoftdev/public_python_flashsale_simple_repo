import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import FlashSaleUser

logger = logging.getLogger(__name__)

DEVICE_TYPES = (
        (u'ios', u'ios'),
        (u'android', u'android'),
        (u'web', u'web')
    )


class PushDevice(models.Model):
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True, help_text=_("Inactive devices will not be sent notifications"))
    user = models.OneToOneField(FlashSaleUser, related_name='push_device', on_delete=models.CASCADE, primary_key=False)
    registration_id = models.TextField(verbose_name=_("Registration token"), max_length=1000)
    type = models.CharField(choices=DEVICE_TYPES, max_length=10)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.registration_id[:10]


class PushMessage(models.Model):
    recipient = models.ForeignKey(FlashSaleUser, related_name='message', on_delete=models.CASCADE, primary_key=False)
    content = models.JSONField(max_length=2000)
    message_body = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
