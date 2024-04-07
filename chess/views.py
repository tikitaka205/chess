from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import GameInfoSerializer, ChessMoveSerializer
from .models import ChessLog, User
from rest_framework import status
from .chess_logic import Chess
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

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

        #방 아이디 / 유저 아이디 / 턴 / 보드/  플레이어 레디 / 결과 / 움직임 기록/ 왕 위치
        if serializer.is_valid():
            instance=serializer.save(board_state=board_state, player_1=user, turn=user)
            instance_id=instance.id
            room_id=instance_id

            #레디스에 저장하기 위해 json str로 변경
            json_string = json.dumps(board_state)
            print("json_string",json_string)
            print("json_string",type(json_string))
            redis_data={
                "player_1":user_id,
                "player_2":"",
                "board_state":json_string,
                "turn": "player_1",
                "player_1_ready":"",
                "player_2_ready":"",
                "result":"",
                "chesslog":"",
                "player_1_king":"",
                "player_2_king":""
            }
            # 캐시에 해시구조로 저장
            redis_client.hmset(room_id, redis_data)

            # # 데이터 조회
            # pl=redis_client.hget(room_id,"player_1")
            # turn=redis_client.hget(room_id,"turn")
            # get_data=redis_client.hget(room_id,"board_state")
            # # 바이트로 들어온 데이터 str로 decode 후 json.loads 으로 리스트로 변환
            # pr=json.loads(get_data.decode('utf-8'))

            return Response({"board_state":board_state,"game_id":instance_id},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # move=request.data.get('move')
    
    # ready:0=False 1=True
    # player_ready_check and player_2 save
    # 내가 1이면 1레디 2가 없으면 저장하고 2도 레디 
    def put(self, request):
        """
        chess ready
        """
        #플레이어 2 없다면 아이디 나 저장하고 레디로 바꾸고 둘다 레디냐?
        #
        user_id.
        redis_data={
            "player_1_ready":"",
            "player_2_ready":"",
        }
        redis_client.hmset(game_id,)
        game_id=int(request.data.get('game_id'))
        user_id=int(request.data.get('user_id'))
        game=get_object_or_404(ChessLog, id=game_id)
        chess_instance=Chess()
        chess_instance.create_board()
        chess_instance.set_game()
        board_state=chess_instance.board

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
                return Response({"player":"player_1","board_state":board_state,"ready_state":"game_start"},status=status.HTTP_200_OK)
            return Response({"ready_state":"player_1_False"},status=status.HTTP_200_OK)

        elif game.player_1.id!=user_id and game.player_2==None:
            user=get_object_or_404(User,id=user_id)
            game.player_2=user
            game.player_2_ready=True
            game.save()
            print("3")
            if game.player_1_ready and game.player_2_ready:
                return Response({"player":"player_2","board_state":board_state,"ready_state":"game_start"},status=status.HTTP_200_OK)
            return Response({"ready_state":"player_2_True"},status=status.HTTP_200_OK)
            
        elif game.player_1.id!=user_id and game.player_2.id==user_id and game.player_2_ready==True:
            game.player_2_ready=False       
            game.save()
            print("4")
            data={
            "player":"player_2",
            "board_state":board_state,
            "ready_state":"game_start"
            }
            if game.player_1_ready and game.player_2_ready:
                return Response({
                    "player":"player_2",
                    "board_state":board_state,
                    "ready_state":"game_start"},
                    status=status.HTTP_200_OK)
            return Response({"ready_state":"player_2_False"},status=status.HTTP_200_OK)

        elif game.player_1.id!=user_id and game.player_2.id==user_id and game.player_2_ready==False:
            game.player_2_ready=True       
            game.save()
            print("5")
            data={
            "player":"player_2",
            "board_state":board_state,
            "ready_state":"game_start"
            }
            if game.player_1_ready and game.player_2_ready:
                return Response({"player":"player_2","board_state":board_state,"ready_state":"game_start"},status=status.HTTP_200_OK)
            return Response({"ready_state":"player_2_True"},status=status.HTTP_200_OK)

        else:
            print("=====")
            pass

    # delete game
    def delete(self, request):
        pass

