import json

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from flashsale.misc.lib.exceptions import ArgumentWrongError
from flashsale.serializer.push import PushDeviceSerializer
from flashsale.models.push import PushDevice, PushMessage


class RegisterPushDeviceView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PushDeviceSerializer

    def post(self, request, *args, **kwargs):
        device = PushDevice.objects.filter(user=request.user).first()
        serializer = self.get_serializer(data=request.data) if device is None else self.get_serializer(device, data=request.data)
        serializer.is_valid(raise_exception=True)
        device = serializer.save(user=request.user)

        data = {'device_id': device.id}
        return Response(data)


# register push message for test only
class RegisterPushMessageView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if 'content' not in request.data or 'message' not in request.data:
            raise ArgumentWrongError(_('content and message should be provided'))

        content = json.loads(request.data['content'])

        print(content)

        if settings.TEST_MODE_ON is True:
            PushMessage.objects.create(recipient=request.user, content=content,
                                       message_body=request.data['message'])

        data = {'msg': 'success'}
        return Response(data)
