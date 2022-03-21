import logging

from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from flashsale.models.review import Review, REVIEW_RATING_CHOICES
from flashsale.misc.lib.exceptions import ArgumentWrongError

logger = logging.getLogger(__name__)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('store', 'review', 'rating', 'parent',)

    def validate(self, attrs):
        user = self.context['request'].user
        store = attrs['store']

        # Review is written by user. Owner can't write on his store.
        if 'parent' not in attrs:
            if store.user == user:
                raise ArgumentWrongError(_("Owner can't write review on his store"))

            return attrs
        # Reply is written by owner. only Owner can write reply on his store's review.
        else:
            parent = attrs['parent']

            if parent.store != store:
                raise ArgumentWrongError(_("You are not owner of this review's store or review is not included store"))

            if Review.objects.filter(user=user, store=store, parent=parent).exists():
                raise ArgumentWrongError(_("You already write reply on the review"))

            return attrs

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)

        return review

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ReviewDetailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    picture = serializers.URLField(source='user.picture', read_only=True)
    store = serializers.IntegerField(source='store.id', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    children = SerializerMethodField(source='get_children')

    class Meta:
        model = Review
        fields = ('id', 'email', 'store', 'picture', 'store_name', 'review', 'rating', 'created', 'children', 'parent')
        ref_name = 'Review'

    def get_children(self, obj):
        if "children" in self.context:
            children = self.context['children'].get(obj.id, [])
            serializer = ReviewDetailSerializer(children, many=True, context=self.context)
            return serializer.data
        else:
            return None

    def to_representation(self, instance):
        result = super(ReviewDetailSerializer, self).to_representation(instance)
        hide = self.context.get('hide', True)
        if hide is True:
            result['email'] = result['email'][:3] + '******' + result['email'][-3:]
        return OrderedDict([(key, result[key]) for key in result if (result[key] is not None and result[key]) or key == 'editable'])