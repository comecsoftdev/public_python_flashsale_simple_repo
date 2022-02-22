from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException


class ArgumentWrongError(APIException):
    result_code = 400                           # status.HTTP_400_BAD_REQUEST
    default_detail = _('parameter wrong')
    default_code = 'parameter wrong'


class NoProviderError(APIException):
    result_code = 400
    default_detail = _('There is no provider for oauth')
    default_code = 'No Provider Error'


class OAuthAuthenticationError(APIException):
    result_code = 401
    default_detail = _('OAuth Authentication Error')
    default_code = 'Oauth authentication Error'
