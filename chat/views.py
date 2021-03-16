from django.shortcuts import render
import uuid


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    username = 'user#'+str(uuid.uuid4().int)[:4]
    return render(request, 'chatroom.html', {
        'room_name': room_name,
        'username': username,
    })
