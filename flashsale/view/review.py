import datetime

from django.db.models import Avg, Count
from django.db.models import Q, OuterRef, Subquery, Exists
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from flashsale.misc.lib.exceptions import ArgumentWrongError, NoPermissionToAccess
from flashsale.misc.lib.permissions import IsReviewOwner
from flashsale.serializer.review import ReviewSerializer, ReviewDetailSerializer
from flashsale.models.review import Review
from flashsale.models.store import Store


class RegisterReviewView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(user=request.user)

        return Response({'review': ReviewDetailSerializer(review, context={'request': request}).data})


class UnRegisterReviewView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsReviewOwner)

    def post(self, request, *args, **kwargs):
        review = self.get_object(request)

        review.delete()

        data = {'msg': 'Unregister Review Success', 'review': {"id": int(request.data['review'])}}

        return Response(data)

    def get_object(self, request):
        try:
            obj = Review.objects.select_related('user', 'store', 'store__user', 'parent').get(id=request.data['review'])
        except KeyError:
            raise ArgumentWrongError(_('review should be provided'))

        self.check_object_permissions(self.request, obj)
        return obj
