# chat/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Message

def chat_room(request, username):
    users = User.objects.exclude(username=request.user.username)
    messages = Message.objects.filter(
        sender=request.user, recipient__username=username
    ) | Message.objects.filter(
        sender__username=username, recipient=request.user
    )
    return render(request, 'chat/chat_room.html', {
        'users': users,
        'other_user': username,
        'messages': messages
    })
