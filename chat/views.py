from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import ChessLog, User
from rest_framework.generics import get_object_or_404

class ChatView(APIView):
    pass
    # def post(self, request):
    #     user_id=request.data.get('user_id')
    #     user=create(ChessLog, player_1=user_id)
    #     print("user",user)
    #     print("request",user_id)
    #     print("post")

    #     #chessgame setting
    #     chess_instance=Chess()
    #     chess_instance.create_board()
    #     chess_instance.set_game()
    #     board_state=chess_instance.board
    #     serializer=ChessMoveSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(board_state=board_state, player_1=user)
    #         return Response({"board_state":board_state},status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    #     # ChessLog.create()
    #     # print("room_name",room_name)
    #     # return Response(room_name,status=status.HTTP_200_OK)

#인덱스에서 번호치면 룸으로 연결되면서 room_name을 전달함 전달하면서 js에서 뭐 하는듯
#지금부터 할거는 js에서 바로 room js 연결
#지금 숫자보내면 소켓을 만드는게 안되는중
#화면바꾸고 원래처럼