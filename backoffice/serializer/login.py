from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=50)
    password = serializers.CharField(min_length=6)


class LoginRefreshSerializer(serializers.Serializer):
    user_code = serializers.IntegerField()
    old_token = serializers.CharField(min_length=25)
