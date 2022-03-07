from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from accounts.models import USER_TYPE_OWNER

from flashsale.misc.lib.exceptions import ArgumentWrongError
from flashsale.models.store import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('category', 'name', 'phone',  'lat', 'lng', 'address', 'address_detail')

    def validate_category(self, value):
        # value is instance of Category & and check if value is leaf node
        if value.is_leaf_node() is False:
            raise ArgumentWrongError(_('argument wrong error - not leaf node'))
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        store = Store.objects.create(**validated_data)

        # this user is store owner, so change type to FieldChoiceType.USER_TYPE_OWNER
        user = validated_data['user']
        user.type = USER_TYPE_OWNER
        user.save(update_fields=['type'])

        return store

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class StoreDetailSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source='category.id', read_only=True)

    class Meta:
        model = Store
        fields = ('id', 'name', 'category', 'phone', 'lat', 'lng', 'address', 'address_detail', 'created')

    def to_representation(self, instance):
        result = super(StoreDetailSerializer, self).to_representation(instance)
        # to remove empty sequence '', [], (), but consider boolean False
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None and result[key]])