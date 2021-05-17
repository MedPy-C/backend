from rest_framework import serializers

from backoffice.utils.validator import password_validator, access_level_validator


class UserLoginAddSerializer(serializers.Serializer):
    user_login = serializers.CharField(min_length=10, max_length=50)
    password = serializers.CharField(
        min_length=8, validators=[password_validator])
    name = serializers.CharField(max_length=250)
    access_level = serializers.IntegerField(
        required=False, validators=[access_level_validator])
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=18)
