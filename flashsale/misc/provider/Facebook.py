import facebook

from django.utils.translation import gettext_lazy as _

from flashsale.misc.provider.ProviderBase import ProviderBase
from flashsale.misc.lib.exceptions import OAuthAuthenticationError


# https://facebook-sdk.readthedocs.io/en/latest/index.html
class Facebook(ProviderBase):
    def verify_id_token(self, id_token, email):
        try:
            graph = facebook.GraphAPI(access_token=id_token)
            args = {'fields': 'id,name,email,picture', }
            profile = graph.get_object('me', **args)

            if profile['email'] != email:
                raise OAuthAuthenticationError(_('Facebook OAuth Authentication Error.. different email address'))
        except Exception as e:
            raise OAuthAuthenticationError(_('Facebook OAuth Authentication Error.') + e.__str__())

        name = profile.get('name', None)

        try:
            picture = profile['picture']['data']['url']
        except KeyError:
            picture = None

        user_info = {'email': profile['email'], 'name': name, 'picture': picture}

        return user_info
