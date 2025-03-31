from rest_framework import serializers
from .models import Building, Users, SmartDevice, Reading, BuildingIncharge


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__" 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('electrical_id', 'username', 'password',
                  'firstname', 'lastname', 'position')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            position=validated_data['position']
        )
        return user


class SmartDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartDevice
        fields = "__all__"


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ('reading_id', 'device', 'reading_timestamp', 'voltage_consumption',
                  'current_consumption', 'power_consumption','energy_consumption')


class BuildingInchargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingIncharge
        fields = "__all__"