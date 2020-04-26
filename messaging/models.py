from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    body = models.TextField() # Text of a message
    sender = models.ForeignKey(User, related_name='sentMessages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='receivedMessages', on_delete=models.CASCADE)

    def __str__(self):
        return self.sender.username + ' -> ' + self.recipient.username
