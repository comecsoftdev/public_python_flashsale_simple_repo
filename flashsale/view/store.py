from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import FlashSaleUser

from flashsale.misc.lib.exceptions import ArgumentWrongError
from flashsale.misc.lib.permissions import IsUserTypeOwner, IsStoreOwner
from flashsale.models.store import Store
from flashsale.serializer.basic_data import FlashSaleUserDetailSerializer
from flashsale.serializer.store import StoreSerializer


class RegisterStoreView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        #  Below is the same as 'serializer = self.get_serializer(data=request.data)'
        serializer_store = StoreSerializer(data=request.data, context={'request': request})
        serializer_store.is_valid(raise_exception=True)

        serializer_store.save(user=request.user)

        # compare 2 queries below
        # queryset = FlashSaleUser.objects.filter(id=request.user.id).first()
        queryset = FlashSaleUser.objects.prefetch_related(
            Prefetch('store', queryset=Store.objects.all().select_related('category')), 'store__product', ) \
            .filter(id=request.user.id).first()

        # if owner & store info registered normally, send user_info to client
        serializer = FlashSaleUserDetailSerializer(queryset, context={"request": request})
        data = {'user_info': serializer.data, }

        return Response(data)


class UnRegisterStoreView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsUserTypeOwner, IsStoreOwner)

    def post(self, request, *args, **kwargs):
        store = self.get_object(request)

        store.delete()

        data = {'msg': 'success'}
        return Response(data)

    def get_object(self, request):
        try:
            obj = Store.objects.get(id=request.data['store'])
        except KeyError:
            raise ArgumentWrongError(_('store should be provided'))
        except ObjectDoesNotExist:
            raise ArgumentWrongError(_('store not exist'))

        self.check_object_permissions(self.request, obj)

        return obj
