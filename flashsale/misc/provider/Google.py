from django.conf import settings

from django.utils.translation import gettext_lazy as _

from google.oauth2 import id_token
from google.auth.transport import requests

from flashsale.misc.provider.ProviderBase import ProviderBase
from flashsale.misc.lib.exceptions import OAuthAuthenticationError


# refer to https://developers.google.com/identity/sign-in/web/backend-auth
class Google(ProviderBase):
    def verify_id_token(self, token, email):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.FLASHSALE_GOOGLE_CLIENT_ID)

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise OAuthAuthenticationError(_('Google OAuth Authentication Error.. iss error'))
            if id_info['email'] != email:
                raise OAuthAuthenticationError(_('Google OAuth Authentication Error.. different email address'))
        except OAuthAuthenticationError as inst:
            raise OAuthAuthenticationError(inst.detail)
        except Exception as e:
            raise OAuthAuthenticationError(_('Google OAuth Authentication Error. ' + e.__str__()))

        user_info = {'email': id_info['email'], 'name': id_info.get('name', None), 'picture': id_info.get('picture', None)}

        return user_info
