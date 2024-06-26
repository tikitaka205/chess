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

        # 미들웨어를 연결
        # if self.scope["user"].is_authenticated:
        #     # 인증된 사용자일 경우, 연결을 수락합니다.
        #     self.accept()
        # else:
        #     # 인증되지 않은 사용자일 경우, 연결을 거부하거나 적절한 처리를 합니다.
        #     self.close()

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
    # 상대가 보내면 바로 나에게 보임
    def receive(self, text_data):
        """
        실시간 메세지 보냈을때 구별, 처리
        """
        # print("=======text_data",text_data)
        text_data_json = json.loads(text_data)

        # 알람 다르게
        # user = self.scope['user'].id
        # is_your_turn=True

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
            room_id = text_data_json["game_id"]
            redis_board_state=redis_client.hget(room_id,"board_state")
            board_state = json.loads(redis_board_state) if redis_board_state else None

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "chat.message", 
                    "board_state":board_state, 
                    "alarm":alarm ,
                    "type_name":"board_state"}
            )

        if text_data_json["type"]=="promotion":
            # 딱 하나 들어옴


            promotion_horse = text_data_json["horse"]
            is_valid_input_promotion = Chess.is_valid_input_promotion(promotion_horse)
            user_id = text_data_json["user_id"]
            room_id = text_data_json["room_id"]

            redis_player_1=int(redis_client.hget(room_id,"player_1"))
            redis_player_2=int(redis_client.hget(room_id,"player_2"))
            redis_promotion_position=redis_client.hget(room_id,"promotion_position")
            redis_board_state=redis_client.hget(room_id,"board_state")
            board_state = json.loads(redis_board_state) if redis_board_state else None
            redis_player_1=int(redis_client.hget(room_id,"player_1"))
            print("redis_promotion_position",redis_promotion_position)
            print("redis_promotion_position",type(redis_promotion_position))
            if redis_promotion_position!=None and is_valid_input_promotion[0]==True:
                i_to=int(redis_promotion_position[0])
                j_to=int(redis_promotion_position[1])
                print("i_to",i_to)
                print("j_to",j_to)
                if redis_player_1==user_id:
                    color="w"
                    change_turn=redis_player_2
                else:
                    color="b"
                    change_turn=redis_player_1

                board_state[i_to][j_to]=color+is_valid_input_promotion[1]
                print("color",color+is_valid_input_promotion[1])
                json_new_board_state=json.dumps(board_state)
                redis_new_data={
                    "board_state":json_new_board_state,
                    "turn":change_turn,
                }

                new_board_state=board_state
                alarm=f"{board_state[i_to][j_to]} 로 승급했습니다."
                redis_client.hmset(room_id, redis_new_data)
                redis_client.hdel(room_id, redis_promotion_position)
                # print("receive에서메세지",message)
            else:
                if redis_promotion_position==None:
                    new_board_state=board_state
                    alarm="입력을 확인해주세요 예시 : a2pa4"
                elif is_valid_input_promotion[0]==False:
                    new_board_state=board_state
                    alarm=is_valid_input_promotion[1]


            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
                    )

        #          'a7bP','a6'
        if text_data_json["type"]=="horse":
            """
            말을 옮기는 메세지
            캐시를 사용하기위해 아이디를 가져옴
            """
        
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
            redis_chesslog=redis_client.hget(room_id,"chesslog")
            json_chesslog=json.loads(redis_chesslog) if redis_chesslog else None
            board_state = json.loads(redis_board_state) if redis_board_state else None

            # 50 draw
            if len(json_chesslog)==100:
                alarm="50턴 무승부 입니다"
                new_board_state=board_state
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
                    )
                return

            # 3 turns draw
            if len(json_chesslog)>11: 
                if json_chesslog[-1]==json_chesslog[-5]==json_chesslog[-9] and json_chesslog[-3]==json_chesslog[-7]==json_chesslog[-11]:
                    alarm="같은 수 3회 반복 무승부 입니다"
                    new_board_state=board_state
                    print("무승부 확인")
                    print(json_chesslog[-1]==json_chesslog[-5]==json_chesslog[-9])
                    print(json_chesslog[-3]==json_chesslog[-7]==json_chesslog[-11])
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
                    )
                    return

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

                if redis_turn==redis_player_1:
                    now_turn="white"
                else:
                    now_turn="black"

                # 턴바꾸기
                if user_id==redis_player_1:
                    print("유저 1이네")
                    change_turn=redis_player_2
                    my_king=redis_white_k
                    enemy_king=redis_black_k
                    attack_color="w"
                elif user_id==redis_player_2:
                    print("유저 2네")
                    change_turn=redis_player_1
                    my_king=redis_black_k
                    enemy_king=redis_white_k
                    attack_color="b"

                print("my_king위치:",my_king)

                # 유저의 턴이고 폰일때
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

                    # 움직인 후 내 킹 체크확인
                    json_new_board_state=json.dumps(new_board_state)
                    isValid_check=Chess.isValid_check(my_king, new_board_state)
                    print("체크 확인",isValid_check)
                    if result[0]==True:
                        # 내 킹 체크가 아니다
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            
                            print("isValid_check",isValid_check)

                            # 만약 승급이 가능한 위치라면 일단 캐시 저장하고 입력 받아야함 턴 안바꾸고 입력하라고 함
                            # 프론트에서 한글자면서 프로모션이면 받아서 보드 캐시 들고와서 보고 저장하고 돌려줌
                            if i_to==0 or i_to==7:
                                print("j_toj_toj_to",i_to,j_to)
                                new_board_state = json.loads(json_new_board_state) if json_new_board_state else None
                                redis_new_data={
                                    "board_state":json_new_board_state,
                                    "chesslog":json_chesslog,
                                    "promotion_position":str(i_to)+str(j_to),
                                }
                                alarm="승격하고 싶은 말의 종류를 입력하세요"
                                redis_client.hmset(room_id, redis_new_data)
                                async_to_sync(self.channel_layer.group_send)(
                                self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
                                )
                                return
                            else:
                                redis_new_data={
                                    "board_state":json_new_board_state,
                                    "turn":change_turn,
                                    "chesslog":json_chesslog,
                                }
                                redis_client.hmset(room_id, redis_new_data)
                            # print(list_chesslog)


                            # 상대방 체크냐 확인
                            king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                            isValid_enemy_check=Chess.isValid_check(enemy_king, new_board_state)

                            # not check but stalemate check
                            if isValid_enemy_check[0]==False:
                                pass
                                # king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                                # isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # print("stalemate check",king_checkmate)
                                # alarm="체크메이트는 아니지만 킹이 움직일 수 없어 stalemate 무승부 입니다"
                                
                            
                            # 상대킹 체크라면
                            elif isValid_enemy_check[0]==True:
                                print("isValid_enemy_check",isValid_enemy_check)
                                isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # 체크메이트 확인 체크메이트 아니라면 피하면 끝
                                if isValid_enemy_checkmate[0]==False:
                                    print("isValid_enemy_checkmate",isValid_enemy_checkmate)
                                    alarm=isValid_enemy_checkmate[4]
                                # 체크 메이트라면
                                else:
                                    print("checkmate")
                                    alarm=isValid_enemy_check[4] + "그리고 체크메이트 입니다."
                                    redis=redis_client.hgetall(room_id)
                                    redis_board_state=redis_client.hget(room_id,"board_state")
                                    redis_turn=int(redis_client.hget(room_id,"turn"))
                                    redis_player_1=int(redis_client.hget(room_id,"player_1"))
                                    redis_player_2=int(redis_client.hget(room_id,"player_2"))

                                    if redis_turn==redis_player_1:
                                        lose_user=redis_player_1
                                        lose_color="W"
                                        win_user=redis_player_2
                                    elif redis_turn==redis_player_2:
                                        lose_user=redis_player_2
                                        lose_color="B"
                                        win_user=redis_player_1

                                    game_instance=ChessLog.objects.get(id=room_id)
                                    win_user_instance=User.objects.get(id=win_user)
                                    lose_user_instance=User.objects.get(id=lose_user)

                                    game_instance.result=lose_color+"lose"
                                    game_instance.board_state=new_board_state
                                    win_user_instance.rank+=5
                                    win_user_instance.win+=1
                                    lose_user_instance.rank-=5
                                    lose_user_instance.lose+=1

                                    game_instance.save()
                                    win_user_instance.save()
                                    lose_user_instance.save()

                        # 내 킹 체크되면 못옮긴다
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm=isValid_check[4]
                        else:
                            pass
                    else:
                        pass


                elif horse_type=="B" and isValid_turn:
                    result=Chess.move_bishop(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]

                    json_new_board_state=json.dumps(new_board_state)
                    print("체크 확인",isValid_check)
                    # 일단 말 움직임 괜찮은지 확인
                    if result[0]==True:
                        isValid_check=Chess.isValid_check(my_king, new_board_state)
                        # 내 킹 체크가 아니다
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            print("isValid_check",isValid_check)
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            # print(list_chesslog)

                            redis_new_data={
                                "board_state":json_new_board_state,
                                "turn":change_turn,
                                "chesslog":json_chesslog,
                            }
                            redis_client.hmset(room_id, redis_new_data)

                            # 상대방 체크냐 확인
                            king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                            isValid_enemy_check=Chess.isValid_check(enemy_king, new_board_state)
                            # 아니면 옮기고 끝
                            if isValid_enemy_check[0]==False:
                                print("isValid_enemy_check",isValid_enemy_check)
                                alarm=result[2]
                                pass
                            
                            # 상대킹 체크라면
                            elif isValid_enemy_check[0]==True:
                                print("isValid_enemy_check",isValid_enemy_check)
                                isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # 체크메이트 확인 체크메이트 아니라면 피하면 끝
                                if isValid_enemy_checkmate[0]==False:
                                    print("isValid_enemy_checkmate",isValid_enemy_checkmate)
                                    alarm=isValid_enemy_checkmate[4]
                                # 체크 메이트라면
                                else:
                                    print("checkmate")
                                    alarm=isValid_enemy_check[4] + "그리고 체크메이트 입니다."
                                    redis=redis_client.hgetall(room_id)
                                    redis_board_state=redis_client.hget(room_id,"board_state")
                                    redis_turn=int(redis_client.hget(room_id,"turn"))
                                    redis_player_1=int(redis_client.hget(room_id,"player_1"))
                                    redis_player_2=int(redis_client.hget(room_id,"player_2"))

                                    if redis_turn==redis_player_1:
                                        lose_user=redis_player_1
                                        lose_color="W"
                                        win_user=redis_player_2
                                    elif redis_turn==redis_player_2:
                                        lose_user=redis_player_2
                                        lose_color="B"
                                        win_user=redis_player_1

                                    game_instance=ChessLog.objects.get(id=room_id)
                                    win_user_instance=User.objects.get(id=win_user)
                                    lose_user_instance=User.objects.get(id=lose_user)

                                    game_instance.result=lose_color+"lose"
                                    game_instance.board_state=new_board_state
                                    win_user_instance.rank+=5
                                    win_user_instance.win+=1
                                    lose_user_instance.rank-=5
                                    lose_user_instance.lose+=1

                                    game_instance.save()
                                    win_user_instance.save()
                                    lose_user_instance.save()

                        # 내 킹 체크되면 못옮긴다 원래 체스보드 반납
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm="옮길 수 없는 자리입니다."+isValid_check[4]
                        else:
                            pass
                    else:
                        pass

                    print("alarm",alarm)
                    print("result",result)
                    print("new_board_state",new_board_state)

                elif horse_type=="N" and isValid_turn:
                    result=Chess.move_knight(from_positon,to_position,board_state)
                    print("나이트 움직임 결과",result)
                    alarm=result[2]
                    new_board_state=result[1]
                    json_new_board_state=json.dumps(new_board_state)
                    if result[0]==True:
                        isValid_check=Chess.isValid_check(my_king, new_board_state)
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            print("isValid_check",isValid_check)
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            # print(list_chesslog)

                            redis_new_data={
                                "board_state":json_new_board_state,
                                "turn":change_turn,
                                "chesslog":json_chesslog,
                            }
                            redis_client.hmset(room_id, redis_new_data)

                            # 상대방 체크냐 확인
                            king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                            isValid_enemy_check=Chess.isValid_check(enemy_king, new_board_state)
                            # 아니면 옮기고 끝
                            if isValid_enemy_check[0]==False:
                                print("isValid_enemy_check",isValid_enemy_check)
                                # new_board_state=redis_board_state
                                alarm=result[2]
                            
                            # 상대킹 체크라면
                            elif isValid_enemy_check[0]==True:
                                print("isValid_enemy_check",isValid_enemy_check)
                                isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # 체크메이트 확인 체크메이트 아니라면 피하면 끝
                                if isValid_enemy_checkmate[0]==False:
                                    print("isValid_enemy_checkmate",isValid_enemy_checkmate)
                                    # new_board_state=redis_board_state
                                    alarm=isValid_enemy_checkmate[4]

                                # 체크 메이트라면
                                else:
                                    print("checkmate")
                                    alarm=isValid_enemy_check[4] + "그리고 체크메이트 입니다."
                                    redis=redis_client.hgetall(room_id)
                                    redis_board_state=redis_client.hget(room_id,"board_state")
                                    redis_turn=int(redis_client.hget(room_id,"turn"))
                                    redis_player_1=int(redis_client.hget(room_id,"player_1"))
                                    redis_player_2=int(redis_client.hget(room_id,"player_2"))

                                    if redis_turn==redis_player_1:
                                        lose_user=redis_player_1
                                        lose_color="W"
                                        win_user=redis_player_2
                                    elif redis_turn==redis_player_2:
                                        lose_user=redis_player_2
                                        lose_color="B"
                                        win_user=redis_player_1

                                    game_instance=ChessLog.objects.get(id=room_id)
                                    win_user_instance=User.objects.get(id=win_user)
                                    lose_user_instance=User.objects.get(id=lose_user)

                                    game_instance.result=lose_color+"lose"
                                    game_instance.board_state=new_board_state
                                    win_user_instance.rank+=5
                                    win_user_instance.win+=1
                                    lose_user_instance.rank-=5
                                    lose_user_instance.lose+=1

                                    game_instance.save()
                                    win_user_instance.save()
                                    lose_user_instance.save()

                        # 내 킹 체크되면 못옮긴다
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm=isValid_check[4]
                        else:
                            pass
                        print(alarm)
                        print(result)
                        print("new_board_state",new_board_state)

                elif horse_type=="R" and isValid_turn:
                    result=Chess.move_rook(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]

                    # 움직인 후 내 킹 체크확인
                    json_new_board_state=json.dumps(new_board_state)
                    isValid_check=Chess.isValid_check(my_king, new_board_state)
                    print("체크 확인",isValid_check)
                    if result[0]==True:
                    # 내 킹 체크가 아니다
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            print("isValid_check",isValid_check)
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            # print(list_chesslog)

                            redis_new_data={
                                "board_state":json_new_board_state,
                                "turn":change_turn,
                                "chesslog":json_chesslog,
                            }
                            redis_client.hmset(room_id, redis_new_data)

                            # 상대방 체크냐 확인
                            king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                            isValid_enemy_check=Chess.isValid_check(enemy_king, new_board_state)
                            # 아니면 옮기고 끝
                            if isValid_enemy_check[0]==False:
                                print("isValid_enemy_check",isValid_enemy_check)
                                pass
                            
                            # 상대킹 체크라면
                            elif isValid_enemy_check[0]==True:
                                print("isValid_enemy_check",isValid_enemy_check)
                                isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # 체크메이트 확인 체크메이트 아니라면 피하면 끝
                                if isValid_enemy_checkmate[0]==False:
                                    print("isValid_enemy_checkmate",isValid_enemy_checkmate)
                                    alarm=isValid_enemy_check[4]
                                # 체크 메이트라면
                                else:
                                    print("checkmate")
                                    pass
                                    alarm=isValid_enemy_check[4] + "그리고 체크메이트 입니다."
                                    redis=redis_client.hgetall(room_id)
                                    redis_board_state=redis_client.hget(room_id,"board_state")
                                    redis_turn=int(redis_client.hget(room_id,"turn"))
                                    redis_player_1=int(redis_client.hget(room_id,"player_1"))
                                    redis_player_2=int(redis_client.hget(room_id,"player_2"))

                                    if redis_turn==redis_player_1:
                                        lose_user=redis_player_1
                                        lose_color="W"
                                        win_user=redis_player_2
                                    elif redis_turn==redis_player_2:
                                        lose_user=redis_player_2
                                        lose_color="B"
                                        win_user=redis_player_1

                                    game_instance=ChessLog.objects.get(id=room_id)
                                    win_user_instance=User.objects.get(id=win_user)
                                    lose_user_instance=User.objects.get(id=lose_user)

                                    game_instance.result=lose_color+"lose"
                                    game_instance.board_state=new_board_state
                                    win_user_instance.rank+=5
                                    win_user_instance.win+=1
                                    lose_user_instance.rank-=5
                                    lose_user_instance.lose+=1

                                    game_instance.save()
                                    win_user_instance.save()
                                    lose_user_instance.save()

                        # 내 킹 체크되면 못옮긴다
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm=result[2]
                        else:
                            pass
                    else:
                        pass

                    print(alarm)
                    print(result)
                    print("new_board_state",new_board_state)

                # 킹은 움직이면 레디스 킹위치 업데이트
                elif horse_type=="K" and isValid_turn:
                    result=Chess.move_king(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]

                    # 움직인 후 내 킹 체크확인
                    json_new_board_state=json.dumps(new_board_state)
                    # 킹 옮긴 위치기준으로 체크
                    isValid_check=Chess.isValid_check(to_position, new_board_state)
                    print("체크 확인",isValid_check)
                    if result[0]==True:
                        # 킹 옮겼는데 킹 체크가 아니다
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            print("isValid_check",isValid_check)
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            # print(list_chesslog)
                            if my_king==redis_white_k:
                                redis_new_data={
                                    "board_state":json_new_board_state,
                                    "turn":change_turn,
                                    "white_king":to_position,
                                    "chesslog":json_chesslog,
                                }
                            else:
                                redis_new_data={
                                    "board_state":json_new_board_state,
                                    "turn":change_turn,
                                    "black_king":to_position,
                                    "chesslog":json_chesslog,
                                }
                            redis_client.hmset(room_id, redis_new_data)

                        # 내 킹 체크되면 못 옮긴다
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm=isValid_check[4]
                        else:
                            pass
                    else:
                        alarm=result[2]

                elif horse_type=="Q" and isValid_turn:
                    result=Chess.move_queen(from_positon,to_position,board_state)
                    new_board_state=result[1]
                    alarm=result[2]
                    json_new_board_state=json.dumps(new_board_state)
                    if result[0]==True:
                        isValid_check=Chess.isValid_check(my_king, new_board_state)
                        if isValid_check[0]==False:
                            # 우선 움직일 수는 있으니 저장
                            print("isValid_check",isValid_check)
                            list_chesslog = json.loads(redis_chesslog) if redis_chesslog else None
                            list_chesslog.append(from_positon + to_position)
                            json_chesslog=json.dumps(list_chesslog)
                            # print(list_chesslog)

                            redis_new_data={
                                "board_state":json_new_board_state,
                                "turn":change_turn,
                                "chesslog":json_chesslog,
                            }
                            redis_client.hmset(room_id, redis_new_data)

                            # 상대방 체크냐 확인
                            king_checkmate, enemy_king_i, enemy_king_j=Chess.transform_str_to_num(enemy_king)
                            isValid_enemy_check=Chess.isValid_check(enemy_king, new_board_state)
                            # 아니면 옮기고 끝
                            if isValid_enemy_check[0]==False:
                                print("isValid_enemy_check",isValid_enemy_check)

                            # 상대킹 체크라면
                            elif isValid_enemy_check[0]==True:
                                print("isValid_enemy_check",isValid_enemy_check)
                                isValid_enemy_checkmate=Chess.isValid_checkmate(enemy_king_i, enemy_king_j,new_board_state)
                                # 체크메이트 확인 체크메이트 아니라면 피하면 끝
                                if isValid_enemy_checkmate[0]==False:
                                    print("isValid_enemy_checkmate",isValid_enemy_checkmate)
                                    # new_board_state=redis_board_state
                                    alarm=isValid_enemy_check[4]
                                # 체크 메이트라면
                                # return True, board[i_positon][j_positon-i], i_positon, j_positon-i, f"{cls.transform_num_to_str(i_positon, j_positon-i)} 위치에서 {board[i_positon][j_positon-i][1]}가 체크입니다"
                                # 방 아이디 / 유저 아이디 / 턴 / 보드/  플레이어 레디 / 결과 / 움직임 기록/ 왕 위치
                                else:
                                    # 레디스 데이터 들고 오기
                                    alarm=isValid_enemy_check[4] + "그리고 체크메이트 입니다."
                                    redis=redis_client.hgetall(room_id)
                                    redis_board_state=redis_client.hget(room_id,"board_state")
                                    redis_turn=int(redis_client.hget(room_id,"turn"))
                                    redis_player_1=int(redis_client.hget(room_id,"player_1"))
                                    redis_player_2=int(redis_client.hget(room_id,"player_2"))

                                    if redis_turn==redis_player_1:
                                        lose_user=redis_player_1
                                        lose_color="W"
                                        win_user=redis_player_2
                                    elif redis_turn==redis_player_2:
                                        lose_user=redis_player_2
                                        lose_color="B"
                                        win_user=redis_player_1

                                    game_instance=ChessLog.objects.get(id=room_id)
                                    win_user_instance=User.objects.get(id=win_user)
                                    lose_user_instance=User.objects.get(id=lose_user)

                                    game_instance.result=lose_color+"lose"
                                    game_instance.board_state=new_board_state
                                    win_user_instance.rank+=5
                                    win_user_instance.win+=1
                                    lose_user_instance.rank-=5
                                    lose_user_instance.lose+=1

                                    game_instance.save()
                                    win_user_instance.save()
                                    lose_user_instance.save()

                                    print("체크메이트 들어옴 데이터 불러보자")
                                    print("redis",redis)
                                    print("checkmate")

                        # 내 킹 체크되면 못옮긴다
                        elif isValid_check[0]==True:
                            print("isValid_check",isValid_check)
                            new_board_state=board_state
                            alarm=isValid_enemy_check[4]
                        else:
                            pass
                        print(alarm)
                        print(result)
                        print("new_board_state",new_board_state)
                else:
                    # 턴 아닐때 따로 알려주면 좋을텐데
                    new_board_state=board_state
                    if isValid_turn==False:
                        is_your_turn=False
                        alarm=f"지금은 {now_turn}의 턴입니다."

            else:
                new_board_state=board_state
                alarm=is_valid_input_str[1]

            # is_your_turn==True:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
            )
            # else:
            #     print("user",user)
            #     async_to_sync(self.channel_layer.group_send)(
            #         user, {"type": "chat.message", "board_state":new_board_state, "alarm":alarm ,"type_name":"board_state"}
            #     )

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


