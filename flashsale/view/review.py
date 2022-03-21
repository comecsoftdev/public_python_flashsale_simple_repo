from collections import defaultdict

from django.utils.translation import gettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashsale.misc.lib.exceptions import ArgumentWrongError, NoPermissionToAccess
from flashsale.misc.lib.pagination import CustomPagination
from flashsale.misc.lib.permissions import IsReviewOwner
from flashsale.serializer.review import ReviewSerializer, ReviewDetailSerializer
from flashsale.models.review import Review


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


class GetReviewsView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        # {1: [], 2:[], 3:[], ...}
        # All replies included in the review of id 1, 2, 3, ...
        children_dict = defaultdict(list)

        pagination = CustomPagination()

        queryset = Review.objects.select_related('user', 'store').filter(store_id=request.data['store'],
                                                                         parent_id=None,).order_by('-created')
        page = pagination.paginate_queryset(queryset, request)
        children = Review.objects.select_related('parent', 'user', 'store').filter(parent_id__in=[p.id for p in page])

        for child in children:
            if child.parent is not None:
                # Add replies to the same review
                # {1: [{replay}, {replay}], 2: [{replay}, {replay}], ...}
                children_dict[child.parent.id].append(child)

        serializer = ReviewDetailSerializer(page, many=True, context={'children': children_dict})

        review = pagination.get_paginated_response(serializer.data)

        data = {'review': review, }
        return Response(data)
