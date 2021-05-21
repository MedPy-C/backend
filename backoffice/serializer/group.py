from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    slug_name = serializers.SlugField(max_length=40)
    about = serializers.CharField(max_length=500)
