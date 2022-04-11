# pip install pyfcm
from django.conf import settings
from pyfcm import FCMNotification

from flashsale.models.push import PushDevice


def send_new_message_push_notification(**kwargs):
    device_id = kwargs.get("device_id")
    device_type = kwargs.get("device_type")
    device_registration_id = kwargs.get("device_registration_id")
    content = kwargs.get("content")
    message_body = kwargs.get('message_body')

    fcm = FCMNotification(api_key=settings.FCM_SERVER_KEY)

    data_message = {
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
        "message": content,
    }

    if device_type == 'android':
        result = fcm.notify_single_device(registration_id=device_registration_id, data_message=data_message, message_body=message_body)

        if result['success'] != 1:
            PushDevice.objects.filter(id=device_id).update(is_active=False)

        return result
