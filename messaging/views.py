from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import Message
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = (IsAuthenticated,)


class MessagesListView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)


class MessagesToUserListView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = self.request.user
        return Message.objects.filter(Q(sender=user) & Q(recipient=pk) | Q(sender=pk) & Q(recipient=user))


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageDetailSerializer
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated, IsSender | IsRecipient, IsOwnerOrReadOnly, )

