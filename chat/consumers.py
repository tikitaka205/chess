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
        print("=======text_data",text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
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
        
            #data parsing
            horse = text_data_json["horse"]
            user_id = text_data_json["user_id"]
            board = text_data_json["board"]
            board_state=json.loads(board)

            # #preprocessing for horse move
            pattern = re.compile(r'([a-z][1-8][a-z][A-Z])|([a-z][1-8])')
            matches = pattern.findall(horse)
            horse_move = ["".join(match) for match in matches if any(match)]
            is_valid_input_str = Chess.is_valid_input_str(horse)

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
            if is_valid_input_str[0]:
                from_positon=horse_move[0]
                to_position=horse_move[1]
                horse_type=horse_move[0][3]

                if horse_type=="P":
                    #여기 폰 대각선이동일때는 공격으로 함수
                    #if PAWN move diagonal use attack def
                    isValid_from, i_from, j_from=Chess.transform_str_to_num(from_positon[:2])
                    print("======",from_positon[:2])
                    print("==========",i_from, j_from)
                    isValid_to, i_to, j_to=Chess.transform_str_to_num(to_position)
                    dif_i=i_to-i_from
                    dif_j=j_to-j_from
                    isValid_diagonal=abs(dif_i)==abs(dif_j)

                    if isValid_diagonal:
                        result=Chess.attack_pawn(from_positon,to_position,board_state)
                    else:
                        result=Chess.move_pawn(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print(board_state)

                elif horse_type=="B":
                    result=Chess.move_bishop(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print("alarm",alarm)
                    print("result",result)
                    print("board_state",board_state)

                elif horse_type=="N":
                    result=Chess.move_knight(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("board_state",board_state)

                elif horse_type=="R":
                    result=Chess.move_rook(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("board_state",board_state)

                elif horse_type=="K":
                    result=Chess.move_king(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("board_state",board_state)

                elif horse_type=="Q":
                    result=Chess.move_queen(from_positon,to_position,board_state)
                    board_state=result[1]
                    alarm=result[2]
                    print(alarm)
                    print(result)
                    print("board_state",board_state)

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
                self.room_group_name, {"type": "chat.message", "board_state":board_state, "alarm":alarm ,"type_name":"board_state"}
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


