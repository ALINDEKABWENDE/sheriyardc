from django.db import models
from django.contrib.auth.models import User

# ✅ Conversation de chat
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_conversations')  # related_name unique
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation entre {', '.join([user.username for user in self.participants.all()])}"

    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()


# ✅ Message dans une conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', default=1)

    #conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')  # related_name unique
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message de {self.sender.username} à {self.timestamp}"
