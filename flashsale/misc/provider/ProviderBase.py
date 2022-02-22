from abc import ABCMeta, abstractmethod


class ProviderBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify_id_token(self, id_token, email): raise NotImplementedError
