from rest_framework import serializers
from .models import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    # User cannot see and change sender of its own message while creating
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'recipient'] # Users are not allowed to edit recipient or sender


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
