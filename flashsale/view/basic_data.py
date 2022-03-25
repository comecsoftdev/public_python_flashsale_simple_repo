from django.db.models import Prefetch

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import FlashSaleUser, USER_TYPE_USER, USER_TYPE_OWNER

from flashsale.models.store import Store
from flashsale.serializer.basic_data import FlashSaleUserDetailSerializer, CategoryDetailSerializer


class GetInitUserDataView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FlashSaleUserDetailSerializer

    def post(self, request, *args, **kwargs):
        # compare 2 queries below
        # queryset = FlashSaleUser.objects.filter(id=request.user.id).first()
        queryset = FlashSaleUser.objects.prefetch_related(
             Prefetch('store', queryset=Store.objects.all().select_related('category')), 'store__product', ) \
             .filter(id=request.user.id).first()

        serializer = self.get_serializer(queryset)

        data = {'user_info': serializer.data, }

        return Response(data)


class GetCategoryView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategoryDetailSerializer

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        from flashsale.misc.lib.cache import get_category_cache

        data = {'category': get_category_cache(), }
        return Response(data)
