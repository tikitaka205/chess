import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from .models import ChessLog
# from rest_framework import status
from chess.chess_logic import Chess
import ast
import json
import re


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
        # print(text_data)
        text_data_json = json.loads(text_data)
        # text_data_json["player_1"]
        if text_data_json["type"]=="message":
            message = text_data_json["message"]
            # print("receive에서메세지",message)
            # print("receive에서메세지",text_data_json)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": message,"type_name":"message"}
            )

        #          'a7bP','a6'
        if text_data_json["type"]=="horse":
            horse = text_data_json["horse"]
            board_2 = text_data_json["board"]

            #preprocessing for parsing
            #[부터 시작해서 끝에 ]인데 왜 성공?
            board_make_flag = board_2.replace('[[','.[')
            board_make_flag_2 = board_make_flag.replace(']]','].')
            pattern = re.compile(r"\[.*?\]")
            data_list_strs = re.findall(pattern, board_make_flag_2)
            board_state = [eval(lst) for lst in data_list_strs]

            #preprocessing for horse move
            pattern = re.compile(r'([a-z][1-8][a-z][A-Z])|([a-z][1-8])')
            matches = pattern.findall(horse)
            horse_move = ["".join(match) for match in matches if any(match)]
            is_valid_input_str = Chess.is_valid_input_str(horse)
            print("is_valid_input_str",is_valid_input_str)
            # print("is_valid_input_str",is_valid_input_str[0])
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
