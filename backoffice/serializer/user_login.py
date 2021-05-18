from rest_framework import serializers

from backoffice.utils.validator import password_validator, access_level_validator


class UserLoginAddSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=50)
    password = serializers.CharField(
        min_length=6, validators=[password_validator])
    name = serializers.CharField(max_length=250)
    access_level = serializers.IntegerField(
        required=False, validators=[access_level_validator])
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=18)
