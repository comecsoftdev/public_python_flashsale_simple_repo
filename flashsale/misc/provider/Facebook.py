import facebook

from django.utils.translation import gettext_lazy as _

from social_django.utils import load_strategy, load_backend

from flashsale.misc.provider.ProviderBase import ProviderBase
from flashsale.misc.lib.exceptions import OAuthAuthenticationError


# https://facebook-sdk.readthedocs.io/en/latest/index.html
class Facebook(ProviderBase):
    def verify_id_token(self, id_token, email):
        try:
            strategy = load_strategy()
            backend = load_backend(strategy=strategy, name='facebook',
                                   redirect_uri=None)

            profile = backend.user_data(id_token)

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
