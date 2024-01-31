from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# def index(request):
#     return render(request, "chat/index.html")

# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})

class ChatView(APIView):

    def post(self, request, room_name):
        room_name=room_name
        print("room_name",room_name)
        return Response(room_name,status=status.HTTP_200_OK)

#인덱스에서 번호치면 룸으로 연결되면서 room_name을 전달함 전달하면서 js에서 뭐 하는듯
#지금부터 할거는 js에서 바로 room js 연결
#지금 숫자보내면 소켓을 만드는게 안되는중
#화면바꾸고 원래처럼