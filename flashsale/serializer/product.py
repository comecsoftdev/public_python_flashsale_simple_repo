from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from flashsale.misc.lib.exceptions import ArgumentWrongError
from flashsale.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    store = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('id', 'store', 'image', 'name', 'comment', 'price',)

    def validate(self, attrs):
        return attrs

    def validate_image(self, image):
        file_size = image.size
        megabyte_limit = 10         #10M
        if file_size > megabyte_limit * 1024 * 1024:
            raise ArgumentWrongError(_("Max file size is {}MB").format(megabyte_limit))

        return image

    def validate_store(self, value):
        max_product = 10
        if Product.objects.filter(store_id=value).count() >= max_product:
            raise ArgumentWrongError(_('maximum product in store is {}').format(max_product))

        return value

    def create(self, validated_data):
        validated_data['store_id'] = validated_data.pop('store')
        product = Product.objects.create(**validated_data)

        return product

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ProductDetailSerializer(serializers.ModelSerializer):
    store = serializers.IntegerField(source='store.id', read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'store', 'image', 'thumbnail', 'name', 'comment', 'price', 'created',)
        ref_name = 'Product'
