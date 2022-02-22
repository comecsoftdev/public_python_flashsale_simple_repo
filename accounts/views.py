from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import FlashSaleUser
from accounts.serializer import SignInSerializer

from flashsale.misc.lib.exceptions import ArgumentWrongError


class SignInView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        user = self.get_object(request)
        if user is None:
            serializer = self.get_serializer(data=request.data)
        else:
            serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh, user_in_db = serializer.save()

        data = {'token': str(refresh.access_token), 'refresh': str(refresh)}
        return Response(data)

    def get_object(self, request):
        try:
            obj = FlashSaleUser.objects.get(email=request.data['email'])
        except KeyError:
            raise ArgumentWrongError(_('email should be provided'))
        except ObjectDoesNotExist:
            obj = None
        return obj
