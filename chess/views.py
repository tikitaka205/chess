from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import GameInfoSerializer, ChessMoveSerializer
from .models import ChessLog, User
from rest_framework import status
from .chess_logic import Chess


class ChessView(APIView):
    def get(self, request):
        """
        get chess state
        TODO
        """
        # game_id=request.query_params.get('game_id','')
        board_state=ChessLog.objects.all()
        serializer=GameInfoSerializer(board_state, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        move horse
        TODO
        둘다 게임시작누르면 post 게임 만듬
        프론트 백 둘다 white black턴 검증
        만든걸 보여주는게 웹소켓통해서?
        말 움직이면 기록
        지금 입력하면 상대에도 보인다 근데 그 메세지를 내가 조절이 불가 가공이
        """
        user_id=request.data.get('user_id')
        user=get_object_or_404(User, id=user_id)
        user=get_object_or_404(User, id=user_id)
        print("user",user)
        print("request",user_id)
        print("post")

        #chessgame setting
        chess_instance=Chess()
        chess_instance.create_board()
        chess_instance.set_game()
        board_state=chess_instance.board
        serializer=ChessMoveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board_state=board_state, player_1=user)
            return Response({"board_state":board_state},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # move=request.data.get('move')



