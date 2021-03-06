from collections import OrderedDict

from rest_framework import  serializers
from rest_framework.fields import SerializerMethodField

from accounts.models import FlashSaleUser

from flashsale.models.basic_data import Category
from flashsale.serializer.store import StoreDetailSerializer


class FlashSaleUserDetailSerializer(serializers.ModelSerializer):
    store = StoreDetailSerializer(many=True, read_only=True)

    class Meta:
        model = FlashSaleUser
        fields = ('email', 'is_active', 'type', 'created', 'store',)
        read_only_fields = ('created',)

    # to remove null if instance is None
    # https://stackoverflow.com/questions/27015931/remove-null-fields-from-django-rest-framework-response
    def to_representation(self, instance):
        result = super(FlashSaleUserDetailSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None and result[key]])


class CategoryDetailSerializer(serializers.ModelSerializer):
    children = SerializerMethodField(source='get_children')

    class Meta:
        model = Category
        fields = ('id', 'abbr', 'name', 'level', 'children', 'items')
        ref_name = 'Category'

    def get_children(self, obj):
        children = self.context['children'].get(obj.id, [])
        serializer = CategoryDetailSerializer(children, many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        result = super(CategoryDetailSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None and result[key]])
