import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room, Message


@login_required
def rooms(request):
    rooms_objects = Room.objects.all()
    return render(request, 'room/rooms.html', {"rooms": rooms_objects})


@login_required
def room(request, slug):
    room_objects = Room.objects.get(slug=slug)
    messages_objects = Message.objects.filter(room=room_objects)
    for message in messages_objects:
        print(message.content)

    return render(request, 'room/room.html', {'room': room_objects, 'messages': messages_objects})
