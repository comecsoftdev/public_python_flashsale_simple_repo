import logging

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from accounts.models import FlashSaleUser
from flashsale.misc.task.CeleryTask import send_new_message_push_notification

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


@receiver(models.signals.post_save, sender=PushMessage)
def send_new_message_notification(sender, **kwargs):
    message = kwargs['instance']

    device_id = message.recipient.push_device.id
    device_type = message.recipient.push_device.type
    device_registration_id = message.recipient.push_device.registration_id

    res = send_new_message_push_notification.delay(device_id=device_id, device_type=device_type,
                                                   device_registration_id=device_registration_id,
                                                   content=message.content, message_body=message.message_body)
    res = res.get()

    if res is None or res.get('success', 0) == 0:
        logger.debug('send_new_message_notification fail {} {}'.format(message.recipient.id, message.content))
    else:
        logger.debug('send_new_message_notification success {} {}'.format(message.recipient.id, message.content))

