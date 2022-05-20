from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# def index(request):
#   return render(request, 'chat/index.html')

# def room(request, room_name):
#     return render(request, 'room.html', {
#         'room_name': room_name
#     })

def index(request):
  return render(request, 'index.html')



def room(request):
  # username = request.GET.get('username', 'Anonymous')
  return render(request, 'room.html')

  # return render(request, 'chat/room.html', {'room_name': room_name, 'username': username})
