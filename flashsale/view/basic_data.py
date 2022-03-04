from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import FlashSaleUser, USER_TYPE_USER, USER_TYPE_OWNER
from flashsale.serializer.basic_data import FlashSaleUserDetailSerializer


class GetInitUserDataView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FlashSaleUserDetailSerializer

    def post(self, request, *args, **kwargs):
        if request.user.type == USER_TYPE_USER:
            queryset = FlashSaleUser.objects.filter(id=request.user.id).first()

            serializer = self.get_serializer(queryset)
        elif request.user.type == USER_TYPE_OWNER:
            queryset = FlashSaleUser.objects.filter(id=request.user.id).first()

            serializer = self.get_serializer(queryset)

        data = {'user_info': serializer.data, }

        return Response(data)
