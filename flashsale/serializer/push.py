from rest_framework import serializers

from flashsale.models.push import PushDevice


class PushDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushDevice
        fields = ('registration_id', 'type', )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        setattr(instance, 'is_active', True)
        instance.save()
        return instance
