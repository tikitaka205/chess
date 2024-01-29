from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import GameInfoSerializer, ChessMoveSerializer
from .models import ChessLog
from rest_framework import status
from .chess_logic import Chess


class ChessView(APIView):
    def get(self, request):
        """
        get chess state
        """
        # game_id=request.query_params.get('game_id','')
        board_state=ChessLog.objects.all()
        serializer=GameInfoSerializer(board_state, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        move horse
        """
        board_state=Chess().board
        # print(board_state)
        serializer=ChessMoveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board_state=board_state)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # move=request.data.get('move')



