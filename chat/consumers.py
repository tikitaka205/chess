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
        text_data_json["player"]
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
            pattern = re.compile(r'([a-h][1-8][a-h][A-Z])|([a-h][1-8])')
            matches = pattern.findall(horse)
            horse_move = ["".join(match) for match in matches if any(match)]
            from_positon=horse_move[0]
            to_position=horse_move[1]
            horse_color=horse_move[0][2]
            # print("horse_move",horse_move)
            # print("horse_move",horse_move[0])
            # print("horse_move",horse_move[1])
            # print("horse_color",horse_color)
            # print(board_state)

            if horse_color=="b":
                result=Chess.move_pawn(from_positon,to_position,board_state)
                board_state=result[1]
                print(result)
                print(board_state)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "board_state":board_state,"type_name":"board_state"}
            )

    # Receive message from room group
    # 이것도 같은 내용으로 뜸
    def chat_message(self, event):
        if event["type_name"]=="board_state":
            # print("board_state 에서 event",event)
            board_state = event["board_state"]
            type_name = event["type_name"]
            self.send(text_data=json.dumps({"board_state": board_state,"type_name":type_name}))
        if event["type_name"]=="message":
            message = event["message"]
            type_name = event["type_name"]
            self.send(text_data=json.dumps({"message": message,"type_name":type_name}))
