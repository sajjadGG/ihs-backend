from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request , 'chat/index.html')

def room(request , first , last ):
    print("in view")
    print(request.user)
    return render(request , 'chat/room.html')