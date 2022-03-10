from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashsale.misc.lib.exceptions import ArgumentWrongError
from flashsale.misc.lib.permissions import IsUserTypeOwner, IsStoreOwner, IsProductOwner
from flashsale.serializer.product import ProductSerializer, ProductDetailSerializer
from flashsale.models.store import Store
from flashsale.models.product import Product


class RegisterProductView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsUserTypeOwner, IsStoreOwner)
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        store = self.get_object(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(user=request.user)

        product.store = store

        data = {'product': ProductDetailSerializer(product, context={"request": request}).data}
        return Response(data)

    def get_object(self, request):
        try:
            # obj = Store.objects.get(id=request.data['store'])
            obj = Store.objects.select_related('user').get(id=request.data['store'])
        except KeyError:
            raise ArgumentWrongError(_('store should be provided'))
        except ObjectDoesNotExist:
            raise ArgumentWrongError(_('store not exist'))
        self.check_object_permissions(self.request, obj)
        return obj


class UnRegisterProductView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsUserTypeOwner, IsProductOwner)

    def post(self, request, *args, **kwargs):
        product = self.get_object(request)

        # image is deleted in models.signals.post_delete
        product.delete()

        data = {'msg': 'Unregister Product Success', 'product': {"id": int(request.data['product'])}}
        return Response(data)

    def get_object(self, request):
        if 'store' not in request.data:
            raise ArgumentWrongError(_('store should be provided'))

        try:
            obj = Product.objects.select_related('user', 'store', 'store__user').get(id=request.data['product'])
        except KeyError:
            raise ArgumentWrongError(_('product should be provided'))
        except ObjectDoesNotExist:
            raise ArgumentWrongError(_('product not exist'))

        self.check_object_permissions(self.request, obj)
        return obj
