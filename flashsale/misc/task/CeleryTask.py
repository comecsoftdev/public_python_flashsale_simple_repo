# pip install pyfcm
import sys
import os
from pathlib import Path
from celery import Celery
from django.conf import settings
from pyfcm import FCMNotification

BASE_DIR = str(Path(__file__).resolve().parent.parent.parent.parent)

# set the default Django settings module for the 'celery' program.
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

if sys.platform.startswith('win32'):
    from lbsfaou import load_environment

    # 1. Celery 4.0+ does not officially support Windows yet.(value error not enough values to unpack (expected 3 got 0))
    #    add 'FORKED_BY_MULTIPROCESSING', '1' for development/test purposes.
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    # load environment variable in .private/debug/.env
    load_environment()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lbsfaou.settings')

app = Celery('CeleryTask')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task
def send_new_message_push_notification(**kwargs):
    from flashsale.models.push import PushDevice

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
