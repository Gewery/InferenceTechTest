from rest_framework import serializers
from .models import Message
from rest_framework.authentication import TokenAuthentication


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'


class MessageDetailSerializer(serializers.ModelSerializer):
    # sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'recipient']


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
