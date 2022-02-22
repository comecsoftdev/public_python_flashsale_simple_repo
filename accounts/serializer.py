from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import FlashSaleUser

from flashsale.misc.provider import get_provider


class SignInSerializer(serializers.ModelSerializer):
    id_token = serializers.CharField(required=True, max_length=2048)
    provider = serializers.CharField(required=True, max_length=16)

    class Meta:
        model = FlashSaleUser
        fields = ('id_token', 'provider', 'email')
        # remove unique validator when verifying email.
        # if email already exist and valid token passed, user will be updated with same email and 'is_active':True. refer to create() function
        extra_kwargs = {
            'email': {'validators': []},
        }
        ref_name = None

    # validate token with provider, id_token and email
    def validate(self, attrs):
        id_token = attrs['id_token']
        provider = attrs['provider']
        email = attrs['email']

        # skip verification of id_token, if settings.TEST_MODE_ON is True
        if settings.TEST_MODE_ON is False:
            provider = get_provider(provider)
            user_info = provider.verify_id_token(id_token, email)
            attrs['display_name'] = user_info['name']
            attrs['picture'] = user_info['picture']
        else:
            get_provider(provider)
            attrs['display_name'] = email[: email.find("@")]
            attrs['picture'] = None

        return attrs

    # save user model.
    def create(self, validated_data):
        # no need to set password, because FlashSaleUser doesn't use password
        validated_data['is_active'] = True
        validated_data.pop('id_token')
        validated_data.pop('provider')

        user = FlashSaleUser.objects.create(**validated_data)

        # create JWT token for user
        refresh = RefreshToken.for_user(user)

        return refresh, user

    # if email already exists, just update user model with 'is_active'= True
    def update(self, instance, validated_data):
        validated_data['is_active'] = True
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        refresh = RefreshToken.for_user(instance)

        return refresh, instance
