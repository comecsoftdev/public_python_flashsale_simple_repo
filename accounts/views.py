import jwt

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenRefreshSerializer as JWTokenRefreshSerializer

from accounts.models import FlashSaleUser
from accounts.serializer import SignInSerializer

from flashsale.misc.lib.exceptions import ArgumentWrongError, RefreshTokenVerificationError


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


class SignOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()

        data = {'msg': 'successfully sign out'}
        return Response(data)


class RefreshTokenView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = JWTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.compare_tokens(request)
        except KeyError:
            raise ArgumentWrongError(_('token and refresh should be provided'))
        except Exception as e:
            raise RefreshTokenVerificationError(e.__str__())

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data

        data = {'token': key['access'], }
        return Response(data)

    def compare_tokens(self, request):
        decoded_refresh = self.decode_token(request.data['refresh'])
        # set verify = False to allow time-expired token
        decoded_token = self.decode_token(request.data['token'], verify=False)

        if decoded_refresh['user_id'] != decoded_token['user_id'] or \
                not FlashSaleUser.objects.filter(id=decoded_token['user_id']).exists():
            raise RefreshTokenVerificationError(_('Refresh or Token verification Error'))

    def decode_token(self, token, verify=True):
        decoded = jwt.decode(token, settings.SIMPLE_JWT_SIGNING_KEY, leeway=10,
                             algorithms=[settings.SIMPLE_JWT_ALGORITHM], options={'verify_exp': verify})

        return decoded
