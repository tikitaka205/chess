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
        make room def
        TODO
        방만들기, 게임시작 하나의 api로 만들기 방만들어서 들어오는것만 만들면?
        둘다 게임시작누르면 post 게임 만듬
        프론트 백 둘다 white black턴 검증
        만든걸 보여주는게 웹소켓통해서?
        말 움직이면 기록
        지금 입력하면 상대에도 보인다 근데 그 메세지를 내가 조절이 불가 가공이
        """
        # 유저를 들고오려면 get해서 들고와서 사용
        user_id=request.data.get('user_id')
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
            instance=serializer.save(board_state=board_state, player_1=user, turn=user)
            instance_id=instance.id
            return Response({"board_state":board_state,"game_id":instance_id},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # move=request.data.get('move')
    
    # ready:0=False 1=True
    # player_ready_check and player_2 save
    # 내가 1이면 1레디 2가 없으면 저장하고 2도 레디 
    def put(self, request):
        # print(request.data.get('user_id'))
        # print("game_id",request.data.get('game_id'))
        game_id=int(request.data.get('game_id'))
        user_id=int(request.data.get('user_id'))
        game=get_object_or_404(ChessLog, id=game_id)
        chess_instance=Chess()
        chess_instance.create_board()
        chess_instance.set_game()
        board_state=chess_instance.board
        # print(game.player_1_ready)
        # print(game.player_2_ready)
        # print(game.player_1_ready and game.player_2_ready)
        if game.player_1.id==user_id and game.player_1_ready==False:
            game.player_1_ready=True
            game.save()
            print(game.player_1_ready)
            print("1")
            data={
            "player":"player_1",
            "board_state":board_state,
            "ready_state":"game_start"
            }
            if game.player_1_ready and game.player_2_ready:
                return Response(data,status=status.HTTP_200_OK)
            return Response({"ready_state":"player_1_True"},status=status.HTTP_200_OK)

        elif game.player_1.id==user_id and game.player_1_ready==True:
            game.player_1_ready=False
            game.save()
            print(game.player_1_ready)
            print("2")
            if game.player_1_ready and game.player_2_ready:
                return Response({"board_state":board_state,"ready_state":"game_start"},status=status.HTTP_200_OK)
            return Response({"ready_state":"player_1_False"},status=status.HTTP_200_OK)

        elif game.player_1.id!=user_id and game.player_2==None:
            game.player_2=user_id
            game.player_2_ready=True
            game.save()
            print("3")
            if game.player_1_ready and game.player_2_ready:
                return Response({"player":"player_2","board_state":board_state,"ready_state":"game_start"},status=status.HTTP_200_OK)
            return Response({"ready_state":"player_2_True"},status=status.HTTP_200_OK)
            
        elif game.player_1.id!=user_id and game.player_2_ready==True:
            game.player_2_ready=False       
            game.save()
            print("4")
            data={
            "player":"player_2",
            "board_state":board_state,
            "ready_state":"game_start"
            }
            if game.player_1_ready and game.player_2_ready:
                return Response(data,status=status.HTTP_200_OK)
            return Response({"ready_state":"player_2_False"},status=status.HTTP_200_OK)

        # print(game.player_1_ready)
        # print(game.player_2_ready)
        # if game.player_1_ready and game.player_2_ready:
        #     return Response({"ready_state":"game_start"},status=status.HTTP_200_OK)
        # else:
        #     print("false")
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

    # and game.player_1_ready=='1'
    # delete game
    def delete(self, request):
        pass

