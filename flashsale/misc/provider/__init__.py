from flashsale.misc.provider import Google, ProviderBase, Facebook

from flashsale.misc.lib.exceptions import NoProviderError


def get_provider(provider):
    provider = provider.lower()
    if provider == 'google':                    # Google OAuth2
        return Google.Google()
    elif provider == 'facebook':                # FaceBook OAuth2
        return Facebook.Facebook()
    else:
        raise NoProviderError()
