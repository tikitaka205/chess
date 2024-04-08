import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from .models import ChessLog
# from rest_framework import status
from chess.chess_logic import Chess
from user.models import User
from chess.models import ChessLog
import ast
import json
import re
from django.db.models import Q
import timeit
import redis

# 레디스 연결 설정
redis_host = 'localhost'
redis_port = 6379
redis_password = None

# 레디스 클라이언트 생성
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        print("컨슈머 에서 연결")
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    #상대가 보내면 바로 나에게 보임
    def receive(self, text_data):
        """
        실시간 메세지 보냈을때 구별, 처리
        """
        # print("=======text_data",text_data)
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        # text_data_json["player_1"]
        if text_data_json["type"]=="message":
            message = text_data_json["message"]
            # print("receive에서메세지",message)
            # print("receive에서메세지",text_data_json)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": message,"type_name":"message"}
            )

        if text_data_json["type"]=="start":
            """
            다른사람에게 게임시작 알림
            put요청으로 플레이어 확인되면 띄워주세요 요청이 오는거임
            여기서 리버스를 보내주기만 하는거지
            """
            alarm="GAME START"
            board_state = text_data_json["board"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "chat.message", 
                    "board_state":board_state, 
                    "alarm":alarm ,
                    "type_name":"board_state"}
            )

        #          'a7bP','a6'
        if text_data_json["type"]=="horse":
            """
            말을 옮기는 메세지
            캐시를 사용하기위해 아이디를 가져옴
            """
            #룸번호 유저
            #룸번호로 방 플레이어, 턴 보고 응답
            #체스  
            #           'a7bP','a5'
            #           'c8bB','a6'
            #           'b1wN','c3'
            #           'a8bR','a6'
            #           'e2wP','e4'
            #           'e1wQ','e3'          퀸
            #           'd1wK','e2'          킹
        
            # data parsing
            horse = text_data_json["horse"]
            user_id = text_data_json["user_id"]
            room_id = text_data_json["room_id"]
            redis_board_state=redis_client.hget(room_id,"board_state")
            redis_turn=int(redis_client.hget(room_id,"turn"))
            redis_player_1=int(redis_client.hget(room_id,"player_1"))
            redis_player_2=int(redis_client.hget(room_id,"player_2"))
            redis_white_k=redis_client.hget(room_id,"white_king")
            redis_black_k=redis_client.hget(room_id,"black_king")
            # print("redis_player_1",redis_player_1)
            # print("redis_player_1",type(redis_player_1))
            # decoded_redis_turn = json.loads(redis_turn) if redis_turn else None
            # decoded_player_1 = json.loads(redis_player_1) if redis_player_1 else None
            # decoded_player_2 = json.loads(redis_player_2) if redis_player_2 else None
            # decoded_redis_white_k = json.loads(redis_white_k) if redis_white_k else None
            # decoded_redis_black_k = json.loads(redis_black_k) if redis_black_k else None

            # json
            board_state = json.loads(redis_board_state) if redis_board_state else None

            # print("decoded_redis_turn",decoded_redis_turn)
            # print("decoded_redis_turn",type(decoded_redis_turn))
            # print("redis_turn",redis_turn)
            # print("redis_turn",type(redis_turn))
            # print("redis_player_1",redis_player_1)
            # print("redis_player_1",type(redis_player_1))
            # print("redis_board_state",redis_board_state)
            # print("redis_board_state",redis_board_state)
            # print("redis_board_state",type(redis_board_state))
            # print("board_state",board_state)
            # print("board_state",type(board_state))
            # #preprocessing for horse move
            pattern = re.compile(r'([a-z][1-8][a-z][A-Z])|([a-z][1-8])')
            matches = pattern.findall(horse)
            horse_move = ["".join(match) for match in matches if any(match)]
            is_valid_input_str = Chess.is_valid_input_str(horse)
            isValid_turn=redis_turn==user_id
            if is_valid_input_str[0]:
                from_positon=horse_move[0]
                to_position=horse_move[1]
                horse_type=horse_move[0][3]

                # 턴바꾸기
                if user_id==redis_player_1:
                    print("유저 1이네")
                    change_turn=redis_player_2
                    my_king=redis_white_k
                elif user_id==redis_player_2:
                    print("유저 2네")
                    change_turn=redis_player_1
                    my_king=redis_black_k
                print("my_king위치:",my_king)
                # 유저의 턴이고 폰일때
                # print("redis_turn",redis_turn, user_id)
                # print("redis_turn",type(redis_turn))
                # print("redis_turn",type(user_id))
                # print("redis_turn",redis_turn==user_id)
                # print("isValid_turn",isValid_turn)
                if horse_type=="P" and isValid_turn:
                    # print("======",from_positon[:2])
                    # print("==========",i_from, j_from)

                    #if PAWN move diagonal use attack def
                    isValid_from, i_from, j_from=Chess.transform_str_to_num(from_positon[:2])
                    isValid_to, i_to, j_to=Chess.transform_str_to_num(to_position)
                    dif_i=i_to-i_from
                    dif_j=j_to-j_from
                    isValid_diagonal=abs(dif_i)==abs(dif_j)

                    # 대각선으로 움직임
                    # 레디스 저장시에는 제이슨해서 넣고
                    # 체크할때는 리스트로
                    # 레디스에서 가져와서는 제이슨
                    if isValid_diagonal:
                        result=Chess.attack_pawn(from_positon,to_position,board_state)
                        new_board_state=result[1]
                        # print("new_board_state",type(new_board_state))
                        alarm=result[2]
                    else:
                        result=Chess.move_pawn(from_positon,to_position,board_state)
                        new_board_state=result[1]
                        # print("new_board_state",type(new_board_state))
                        alarm=result[2]
                    json_new_board_state=json.dumps(new_board_state)
                    # return True, board[i_positon][j_positon-i], i_positon, j_positon-i, "위치에서 체크입니다"
                    # 옮긴 보드에서 내 킹 체크확인
                    # print("json_new_board_state 확인",json_new_board_state)
                    # print("json_new_board_state 확인",type(json_new_board_state))
                    # print("new_board_state 확인",new_board_state)
                    # print("new_board_state 확인",type(new_board_state))
                    isValid_check=Chess.isValid_check(my_king, new_board_state)
                    print("체크 확인",isValid_check)
                    # 옮긴 보드에서 상대방 체크 확인

                    # 턴 바꿔야하고 유저 확인해야하고 맞으면 바꾸기
                    # 상대 아이디를 알아야하는데 아이디 확인하려면 그냥 1,2?
                    # 플레이어가 1이면 t 2이면 f로?
                    # 여기서 체크위치도 확인
                    
                    redis_new_data={
                        "board_state":json_new_board_state,
                        "turn":change_turn
                    }
                    redis_client.hmset(room_id, redis_new_data)
                    print(alarm)
                    print(result)
                    # print(new_board_state)

                elif horse_type=="B" and isValid_turn:
                    result=Chess.move_bishop(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    print("alarm",alarm)
                    print("result",result)
                    print("new_board_state",new_board_state)

                elif horse_type=="N" and isValid_turn:
                    result=Chess.move_knight(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("new_board_state",new_board_state)

                elif horse_type=="R" and isValid_turn:
                    result=Chess.move_rook(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("new_board_state",new_board_state)

                elif horse_type=="K" and isValid_turn:
                    result=Chess.move_king(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("new_board_state",new_board_state)

                elif horse_type=="Q" and isValid_turn:
                    result=Chess.move_queen(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("new_board_state",new_board_state)
                else:
                    # 턴 아닐때 따로 알려주면 좋을텐데
                    new_board_state=board_state
                    alarm="당신의 차레가 아닙니다"



                #움직인 후 체스판을 캐시에 저장
                #db에 저장하는것 비교해보자
                # 가장 최근에 생성된 체스 게임 기록을 가져옴
                # start_time = timeit.default_timer()
                # user=User.objects.get(id=user_id)
                # for i in range(1):
                #     latest_chess_game = ChessLog.objects.filter(Q(player_1=user_id) | Q(player_2=user_id)).order_by('-created_at').first()
                #     latest_chess_game.board_state=board_state
                #     latest_chess_game.turn=user
                #     latest_chess_game.save()
                # end_time = timeit.default_timer()
                # print(end_time - start_time)

                # user1_room_id = "room1"
                # user1_room_data = {
                #     "user_id": user_id,
                #     "chessboard": str(board_state),
                #     "turn": user_id,
                # }
                
                # set_room_data(user1_room_id,user1_room_data)
                # start_time_redis = timeit.default_timer()
                # get_room=get_room_data("room1")
                # for i in range(1):
                #     get_room_chessboard=get_room.get("chessboard",None)
                #     update_room_data(user1_room_id, "chessboard", str(board_state))
                # end_time_redis = timeit.default_timer()
                # print(get_room_chessboard)
                # print(end_time_redis - start_time_redis)

            else:
                alarm=is_valid_input_str[1]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
            )

    # Receive message from room group
    # 이것도 같은 내용으로 뜸
    def chat_message(self, event):
        if event["type_name"]=="board_state":
            # print("board_state 에서 event",event)
            board_state = event["board_state"]
            type_name = event["type_name"]
            alarm = event["alarm"]
            self.send(text_data=json.dumps({"board_state": board_state,"type_name":type_name,"alarm":alarm}))
        if event["type_name"]=="message":
            message = event["message"]
            type_name = event["type_name"]
            self.send(text_data=json.dumps({"message": message,"type_name":type_name}))


def set_room_data(room_id, room_data):
    redis_client.hmset(room_id, room_data)

def get_room_data(room_id):
    return redis_client.hgetall(room_id)

def update_room_data(room_id, key, value):
    redis_client.hset(room_id, key, value)


