# i,j의 위치
chess_board_cells=8
EMPTY='00'
KING='K'
QUEEN='Q'
BISHOP='B'
KNIGHT='N'
ROOK='R'
PAWN='P'

EMPTY='00'
KING='K'
QUEEN='Q'
BISHOP='B'
KNIGHT='N'
ROOK='R'
PAWN='P'

BLACK='b'
WHITE='w'

b="BLACK"
W="WHITE"
class Chess:
    def __init__(self):
        self.board=[]

    def create_board(self):
        board=[]
        if not self.board:
            for i in range(chess_board_cells):
                row=[]
                for s in range(chess_board_cells):
                    row.append(EMPTY)
                board.append(row)
        self.board=board
        # self.set_game()
        print("create_board")

    def print_board(self):
        for i in range(chess_board_cells):
            for s in range(chess_board_cells):
                print(self.board[i][s], end=" ")
            print()

    def erase_board(self):
        for i in range(chess_board_cells):
            for s in range(chess_board_cells):
                self.board[i][s]=EMPTY

    @classmethod
    def is_valid_input_str(cls,position_str):
        # print("position_str[1]",type(position_str))
        # print("position_str[1]",len(position_str))
        # print("position_str[1]",position_str[0])
        # print("position_str[1]",position_str[1])
        print(position_str)
        if len(position_str)!= 11:
            print("cant pass len")
            return False, "check your position"
        elif not position_str[1].isalpha() or position_str[1].lower() not in 'abcdefgh':
            print("position_str[0][0]",position_str[1])
            return False, "check your position"
        elif not position_str[2].isdigit() or int(position_str[2]) not in range(1, 9):
            print("position_str[0][0]",position_str[1])
            return False, "check your position"
        elif position_str[4] not in "P,Q,K,B,R,N":
            print("position_str[0][0]",position_str[1])
            return False, "check your position"
        else:
            return True, "good move"

    @classmethod
    def is_valid_position_str(cls,position_str):
        if len(position_str)!=2:
            print("not two digits of string. check your input")
            return False
        else:
            if ord(position_str[0]) >= ord('a') and ord(position_str[0]) <= ord('h'):
                if int(position_str[1]) >=1 and int(position_str[1])<=8:
                    return True
                    
    #input 'a8',BLACK+ROOK
    #x축 알파벳 y축 숫자 
    #transform a7->i=0 j=6
    #사람들이 보트판 보고 a7하면 여기서는 ij로 바꾸고 수정함 00부터 시작 00 01 02
    @classmethod
    def transform_str_to_num(cls, position_str):
        if cls.is_valid_position_str(position_str):
            i=chess_board_cells-int(position_str[1])
            j=ord(position_str[0])-ord('a')
            # print("j",j)
            # print("i",i)
            return True, i, j
        else:
            return False,0,0

    @classmethod
    def transform_num_to_str(cls, i, j):
        letter = chr(j + ord('a'))
        number = str(chess_board_cells - i)
        return letter + number

    #말 위치와 타입이 유효하다면 세팅
    def set_cell(self,position_str,horse_type_str):
        isVaild, i, j=self.transform_str_to_num(position_str)
        if isVaild:
            self.board[i][j]=horse_type_str
            return True
        else:
            return False

    #모든 말 세팅
    def set_game(self):
        print("set_game")
        self.set_cell('a1',WHITE+ROOK)
        self.set_cell('b1',WHITE+KNIGHT)
        self.set_cell('c1',WHITE+BISHOP)
        self.set_cell('d1',WHITE+KING)
        self.set_cell('e1',WHITE+QUEEN)
        self.set_cell('f1',WHITE+BISHOP)
        self.set_cell('g1',WHITE+KNIGHT)
        self.set_cell('h1',WHITE+ROOK)
        #체스판 수 만큼 폰 세팅
        for x in range(chess_board_cells):
            #위치 알파벳을 숫자로 변경해서 다음 알파벳을 입력
            position_str=chr(ord('a')+x)
            self.set_cell(position_str+'7',BLACK+PAWN)

        self.set_cell('a8',BLACK+ROOK)
        self.set_cell('b8',BLACK+KNIGHT)
        self.set_cell('c8',BLACK+BISHOP)
        self.set_cell('d8',BLACK+KING)
        self.set_cell('e8',BLACK+QUEEN)
        self.set_cell('f8',BLACK+BISHOP)
        self.set_cell('g8',BLACK+KNIGHT)
        self.set_cell('h8',BLACK+ROOK)
        
        for x in range(chess_board_cells):
            position_str=chr(ord('a')+x)
            self.set_cell(position_str+'2',WHITE+PAWN)

        # self.print_board()

    #TODO 지금자리와 옮기는자리 같으면 안된다 #완
    #TODO 옮기려는 부분이 체스판 밖이 아닐까 #완
    #TODO i는 변하지만 j는 변하지 않는다 #완
    #TODO 움직이려는 곳에 말이 있으면 안된다 #완
    #TODO 조건을 만족하면 움직일 것이다 #완
    #TODO 반복문으로 장애물 확인 #완
    #TODO 공격할때와 처음움직일때의 조건 다른거 구현
    #TODO 상대방 공격
    #들어오는 조건을 계속 생각해보자
    #move_pawn('a7bP','a6')
    @classmethod
    def move_pawn(cls, from_positon, to_position, board):
        if from_positon[:-2] ==to_position:
            return False, board, "you moved same position."
        horse_color= from_positon[-2]
        if horse_color== 'w':
            horse_color="WHITE"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isJPositionSame=j_from==j_to
        isIPositionSame=i_from!=i_to
        isGoPositonEmpty=board[i_to][j_to]==EMPTY
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:] #position check vaild
        isValid = isValid_to and isValid_from and isJPositionSame and isIPositionSame and isGoPositonEmpty and isValid_pick_horse
        isVaild_first_move_black=from_positon[1]=="7"
        isVaild_first_move_white=from_positon[1]=="2"
        print("move_pawn", i_from, j_from, i_to, j_to) #여기서 i j 는 실제 0,0을 의미
        if isValid:
            dif=i_to-i_from
            print("valid")
            if from_positon[-2]==BLACK:
                # print("black")
                if dif >= 1 and dif <= 2 and isVaild_first_move_black:  #if=1 or 2 로 해도 될듯?
                    # print("1,2칸 움직임")
                    #앞에 말이 막고있는지 확인
                    # is_okay=True

                    for i in range(1, dif+1): #항상 그냥 숫자만 적지말고 연관된 숫자를 활용하자
                        if board[i_from + i][j_from]!=EMPTY:
                            # is_okay=False
                            # break
                            return False, board, "My chess piece is there."
                        else:
                            board[i_from][j_from]=EMPTY
                            print("원래있던 자리 지움")
                            board[i_to][j_to]=from_positon[2] + PAWN
                            print("제대로 움직임")
                            print(board)
                            return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"
                elif dif == 1 and not isVaild_first_move_black:
                    for i in range(1, dif+1):
                        if board[i_from + i][j_from]!=EMPTY:
                            return False, board, "Pawns can move two squares only on their initial move."
                        else:
                            board[i_from][j_from]=EMPTY
                            board[i_to][j_to]=from_positon[2] + PAWN
                            return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"                
                else:
                    return False, board, "can't move position"
            if from_positon[-2]==WHITE:
                # print("WHITE")
                if dif >= -2 and dif <= -1 and isVaild_first_move_white:
                    for i in range(1, abs(dif)+1):
                        if board[i_from - i][j_from]!=EMPTY:
                            return False, board, "My chess piece is there."
                        else:
                            board[i_from][j_from]=EMPTY
                            board[i_to][j_to]=from_positon[2] + PAWN
                            # print("white움직임")
                            return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"
                elif dif == -1 and not isVaild_first_move_white:
                    for i in range(1, abs(dif)+1):
                        if board[i_from - i][j_from]!=EMPTY:
                            return False, board, "Pawns can move two squares only on their initial move."
                        else:
                            board[i_from][j_from]=EMPTY
                            board[i_to][j_to]=from_positon[2] + PAWN
                            return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"                    
                else:
                    return False, board, "can't move position"
        else:
            print("invalid")
            return False, board, "check your position"

    #폰 공격 대각선인데 먼저 대각선으로 움직이는지 확인해야겠네
    #넘겨올때 대각선인거 확인하고 들어옴
    #대각선이면 어택으로 가는 로직 블랙이면 아래로 화이트면 위로
    #이걸 컨슈머에서 컨트롤해서 이 함수를 쓰게
    @classmethod
    def attack_pawn(cls, from_positon, to_position, board):
        horse_color= from_positon[-2]
        #프론트 TTS
        if horse_color== 'w':
            horse_color="WHITE"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        dif_i=i_to-i_from
        dif_j=j_to-j_from
        isIDifVaild=dif_i<=1 and -1<=dif_i
        isJDifVaild=dif_j<=1 and -1<=dif_j
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        isValid=isValid_from and isValid_to and isIDifVaild and isJDifVaild and isValid_pick_horse
        if isValid:
            print("PAWN attack valid")
            if from_positon[-2]==BLACK:
                isPositonNotEmptyVaild=board[i_to][j_to][0]=='w'
                isIValid=dif_i==1
                isJValid=dif_j==1 or -1
                if isPositonNotEmptyVaild and isIValid and isJValid:
                    board[i_from][j_from]=EMPTY
                    board[i_to][j_to] = from_positon[2] + PAWN
                    return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"
                else:
                    print("PAWN invalid")
                    return False, board, "check your position"

            elif from_positon[-2]==WHITE:
                isPositonNotEmptyVaild=board[i_to][j_to][0]=='b'
                isIValid=dif_i==-1
                isJValid=dif_j==1 or -1
                if isPositonNotEmptyVaild and isIValid and isJValid:
                    board[i_from][j_from]=EMPTY
                    board[i_to][j_to] = from_positon[2] + PAWN
                    return True, board, f"{horse_color} PAWN {from_positon[:2]},{to_position}로 이동"
                else:
                    print("PAWN invalid")
                    return False, board, "check your position"
            else:
                return False, board, "check your position"

        else:
            return False, board, "check your position"

            
    #TODO 종 횡으로 움직임 #완료
    #TODO 같은자리 움직임 금지 #완료
    #TODO 체스판 안의 범위로 이동 #완료
    #TODO 말이 없는 자리를 입력하면 말이 생김 #완료
    #TODO 말이 가는 포지션까지 다른말이 있으면 안된다 #완료
    #TODO 공격하는 말이 나의 말이면 안된다
    #TODO 움직이는 곳에 상대말이 있다면 제거
    #TODO 룩은 위아래오른쪽왼쪽 다 움직일 수 있다
    #move_rook('a7bR','a6')
    @classmethod
    def move_rook(cls, from_positon, to_position, board):
        horse_color= from_positon[-2]
        if horse_color== 'w':
            horse_color="WHITE"
            horse_color_op="BLACK"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        isVaild_same_positon = i_from!=i_to or j_from!=j_to
        isVaild_horizon=i_from == i_to and j_from != j_to
        isVaild_vertical=i_from != i_to and j_from == j_to
        isVaild=isValid_from and isValid_to and isVaild_same_positon and isValid_pick_horse
        print(board[i_from][j_from])
        print(from_positon[2:])
        print(isValid_pick_horse)
        print(isValid_from)
        print(isValid_to)
        print(isVaild_same_positon)
        if isVaild:
            is_ok=True
            if isVaild_horizon:
                print("horizon",isVaild_horizon)
                dif=j_to-j_from
                if dif<0:
                    re=int(1)
                else:
                    re=int(-1)
                #1칸 움직일때는 무조건 통과할듯?
                for i in range(1,abs(dif)):
                    if i < dif:
                        if board[i_from][j_from-(re*i)] != EMPTY:
                            print("horizon 움직임 실패")
                            is_ok=False
                            return False, board, "말의 이동위치로 가기 전 방해물이 있습니다"
                #움직이는 위치 전까지 방해물이 없다면
                if is_ok==True:
                    #그리고 가는곳이 비어있다면
                    if board[i_to][j_to] == EMPTY:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + ROOK
                        return True, board, f"{horse_color} ROOK을 {from_positon[:2]} 에서 {to_position}로 이동"
                    #가는곳에 나의말이 있다
                    elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                        return False, board, "말의 이동위치에 나의 말이 있습니다"
                    #가는곳에 상대방의 말이 있다
                    else:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + ROOK
                        return True, board, f"{horse_color} ROOK 을 {from_positon[:2]} 에서 {to_position}로 이동하며 {board[i_to][j_to+i][1]}을 잡았습니다"

            elif isVaild_vertical:
                print("vertical",isVaild_vertical)
                dif=i_to-i_from
                #움직임이 아래면 + 위로올라가면 dif -
                if dif<0:
                    re=int(1)
                else:
                    re=int(-1)
                for i in range(1,abs(dif)):
                    if i < abs(dif):
                        print("i",i)
                        print("re",re)
                        print("dif",dif)
                        print("i",board[i_from-(re*i)][j_from])
                        if board[i_from-(re*i)][j_from] != EMPTY:
                            print("vertical 움직임 실패")
                            is_ok=False
                            return False, board, "말의 이동위치로 가기 전 방해물이 있습니다"
                #움직이는 위치 전까지 방해물이 없다면
                if is_ok==True:
                    #그리고 가는곳이 비어있다면
                    if board[i_to][j_to] == EMPTY:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + ROOK
                        return True, board, f"{horse_color} ROOK을 {from_positon[:2]} 에서 {to_position}로 이동"
                    #가는곳에 나의말이 있다
                    elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                        return False, board, "말의 이동위치에 나의 말이 있습니다"
                    #가는곳에 상대방의 말이 있다
                    else:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + ROOK
                        return True, board, f"{horse_color} ROOK 을 {from_positon[:2]} 에서 {to_position}로 이동하며 상대방의{board[i_to][j_to][1]}을 잡았습니다"
            #가로 세로로 움직이는 경우가 아닐때
            else:
                return False, board, "ROOK은 대각선으로 이동할 수 없습니다"
        #여기를 세분화 하면 정보를 많이 줄 수 있다 에러에 대한
        else:
            if isVaild_same_positon==False:
                return False, board, "같은 자리로 움직일 수 없습니다."
            elif isValid_pick_horse==False:
                return False, board, "이동하려는 체스말이 그 자리에 없습니다."
            else:
                return False, board, "선택 불가능한 위치 이거나 움직일 수 없는 위치 입니다"

    #같은자리 금지
    #대각선 다른말의 유무
    #절대값 같아야함
    #i차이 j차이가 같아야 한다
    #a1 b2 c3 d4
    @classmethod
    def move_bishop(cls,from_positon, to_position, board):
        horse_color= from_positon[-2]
        if horse_color=='w':
            horse_color=WHITE
        else:
            horse_color=BLACK
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        dif_i=i_to-i_from
        dif_j=j_to-j_from
        isValid_diagonal=abs(dif_i)==abs(dif_j)
        isValid=isValid_from and isValid_to and isValid_diagonal and isValid_pick_horse
        print("isValid_pick_horse",isValid_pick_horse)
        print("from_positon[2:]",from_positon[2:])
        #대각선 ++ +- -+ -- 네가지
        is_ok=True
        if isValid:
            print("come in BISHOP vaild route")
            #dif_i dif_j의 차이
            #dif i 가 양수면 아래로 음수면 위로
            #dif j 가 양수면 오른쪽 음수면 왼쪽
            #[i,j]=[+,+]오른쪽 아래 [+,-]왼쪽 아래 [-,+] 오른쪽 위[-,-] 왼쪽 위
            #위왼쪽 이동
            if dif_i>0 and dif_j>0:
                for i in range(1,abs(dif_i)):
                    if board[i_from+i][j_from+i]!=EMPTY:
                        is_ok=False
                        print("bishop ++ move false")
                        break
            #위오른쪽 이동
            elif dif_i<0 and dif_j>0:
                for i in range(1,abs(dif_i)):
                    if board[i_from-i][j_from+i]!=EMPTY:
                        is_ok=False
                        print("bishop +- move false")
                        break
            #왼쪽아래 이동
            elif dif_i>0 and dif_j<0:
                for i in range(1,abs(dif_i)):
                    if board[i_from+i][j_from-i]!=EMPTY:
                        is_ok=False
                        print("bishop -+ move false")
                        break
            #왼쪽위 이동
            elif dif_i<0 and dif_j<0:
                for i in range(1,abs(dif_i)):
                    if board[i_from-i][j_from-i]!=EMPTY:
                        is_ok=False
                        print("bishop -- move false")
                        break

            if is_ok==True:
                #그리고 가는곳이 비어있다면
                if board[i_to][j_to] == EMPTY:
                    board[i_from][j_from]=EMPTY
                    board[i_to][j_to] = from_positon[2] + BISHOP
                    return True, board, f"{horse_color} BISHOP 을 {from_positon[:2]} 에서 {to_position}로 이동"
                #가는곳에 나의말이 있다
                elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                    return False, board, "말의 이동위치에 나의 말이 있습니다"
                #가는곳에 상대방의 말이 있다
                else:
                    board[i_from][j_from]=EMPTY
                    board[i_to][j_to] = from_positon[2] + BISHOP
                    return True, board, f"{horse_color} BISHOP 을 {from_positon[:2]} 에서 {to_position}로 이동하며 {board[i_to][j_to][1]}을 잡았습니다"

        #vaild 통과 불가
        else:
            if isValid_diagonal==False:
                return False, board, "BISHOP은 대각선으로만 움직일 수 있습니다."
            elif isValid_pick_horse==False:
                return False, board, "이동하려는 체스말이 그 자리에 없습니다."
            else:
                return False, board, "선택 불가능한 위치 이거나 움직일 수 없는 위치 입니다"


    #'b2wN,c3' +1+2 +1
    #한칸 가고 대각선
    #i,j 네방향 + 옆으로 두가지씩 8개의 경우의 수
    #움직임 범위 1이상 2이하
    @classmethod
    def move_knight(cls,from_positon, to_position, board):
        horse_color= from_positon[-2]
        if horse_color== 'w':
            horse_color="WHITE"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        dif_i=i_to-i_from #종의 움직임
        dif_j=j_to-j_from #횡의 움직임
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        isVaild_position_1=abs(dif_i)==1 and abs(dif_j)==2
        isVaild_position_2=abs(dif_i)==2 and abs(dif_j)==1
        isValid=isVaild_position_1 or isVaild_position_2 and (isValid_from and isValid_to and isValid_pick_horse)
        if isValid:
            print("KNIGHT valid")
            print("KNIGHT move")
            
            #나이트 움직임
            if board[i_to][j_to] == EMPTY:
                board[i_from][j_from]=EMPTY
                board[i_to][j_to] = from_positon[2] + KNIGHT
#######
                print("board",board)
                print("board",type(board))
                result = cls.isVaild_check('d1wK', board)
                if result is not None:
                    isValid_check, tip = result
                    print("isValid_check",isValid_check)
                    print("tip",tip)
                else:
                    #현재 플레이어 색 비교해서 내꺼 움직이면 체크인지 확인
                    #내꺼 체크면 나한테만 못움직인다 알려주기
                    #상대방기준 체크이면 알려주기
                    print("result",result)
                    # print("tip",tip)
#########
                return True, board, f"{horse_color} KNIGHT 을 {from_positon[:2]} 에서 {to_position}로 이동"
            
            #가는곳에 나의말이 있다
            elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                return False, board, "말의 이동위치에 나의 말이 있습니다"
            
            #가는곳에 상대방의 말이 있다 공격
            else:
                board[i_from][j_from]=EMPTY
                board[i_to][j_to] = from_positon[2] + KNIGHT
                return True, board, f"{horse_color} KNIGHT 을 {from_positon[:2]} 에서 {to_position}로 이동하며 {board[i_to][j_to][1]}을 잡았습니다"

        else:
            if isVaild_position_1==False or isVaild_position_2==False:
                return False, board, "KNIGHT가 움직일 수 있는 위치가 아닙니다"
            elif isValid_pick_horse==False:
                return False, board, "이동하려는 체스말이 그 자리에 없습니다."
            else:
                return False, board, "선택 불가능한 위치 이거나 움직일 수 없는 위치 입니다"


    #TODO to_position이동시 체크가 되면 안된다
    #TODO 여기서 같은팀 공격불가 기능 만들어보자
    #TODO 공격 기능도 만들어보자
    #TODO 캐슬링
    #TODO 무승부?
    #TODO 상대방이 체크했을때 알림
    #움직였을때 모두체크 그리고 다른말들이 움직였을때 체크
    #흰말 움직이면 흰말체크, 검은말 체크 
    @classmethod
    def move_king(cls,from_positon, to_position, board):

        horse_color= from_positon[-2]
        if horse_color== 'w':
            horse_color="WHITE"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        dif_i=i_to-i_from
        dif_j=j_to-j_from
        isVaild_same_positon = i_from!=i_to or j_from!=j_to
        isValid_move=abs(dif_i)<2 and abs(dif_j)<2
        isValid=isValid_move and isVaild_same_positon and isValid_pick_horse and isValid_from and isValid_to
        if isValid:
            board[i_from][j_from]=EMPTY
            board[i_to][j_to] = from_positon[2] + KING
            return True, board, f"{horse_color} KING {from_positon[:2]},{to_position}로 이동"
        else:
            print("KING isValid_move",isValid_move)
            print("KING isVaild_same_positon",isVaild_same_positon)
            print("KING isValid_pick_horse",isValid_pick_horse)
            print(board)
            print(board[i_from][j_from])
            print(i_from)
            print(j_from)
            print(from_positon[2:])
            print("KING invalid")
            return False, board, "check your position"

    @classmethod
    def move_queen(cls,from_positon, to_position, board):
        horse_color= from_positon[-2]
        if horse_color== 'w':
            horse_color="WHITE"
        else:
            horse_color="BLACK"
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isVaild_same_positon = i_from!=i_to or j_from!=j_to
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        isVaild_horizon=i_from == i_to and j_from != j_to
        isVaild_vertical=i_from != i_to and j_from == j_to
        dif_i=i_to-i_from
        dif_j=j_to-j_from
        isValid_diagonal=abs(dif_i)==abs(dif_j)
        isVaild=isVaild_same_positon and isValid_pick_horse and isValid_from and isValid_to
        if isVaild:
            print("isVaild",isVaild)
            is_ok=True
            if isVaild_horizon:
                print("horizon",isVaild_horizon)
                dif=j_to-j_from
                if dif<0:
                    re=int(1)
                else:
                    re=int(-1)
                #1칸 움직일때는 무조건 통과할듯?
                for i in range(1,abs(dif)):
                    if i < dif:
                        if board[i_from][j_from-(re*i)] != EMPTY:
                            print("horizon 움직임 실패")
                            is_ok=False
                            return False, board, "말의 이동위치로 가기 전 방해물이 있습니다"
                #움직이는 위치 전까지 방해물이 없다면
                if is_ok==True:
                    #그리고 가는곳이 비어있다면
                    if board[i_to][j_to] == EMPTY:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN
                        return True, board, f"{horse_color} QUEEN {from_positon[:2]} 에서 {to_position}로 이동"
                    #가는곳에 나의말이 있다
                    elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                        return False, board, "말의 이동위치에 나의 말이 있습니다"
                    #가는곳에 상대방의 말이 있다
                    else:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN
                        return True, board, f"{horse_color} QUEEN 을 {from_positon[:2]} 에서 {to_position}로 이동하며 {board[i_to][j_to+i][1]}을 잡았습니다"

            elif isVaild_vertical:
                print("vertical",isVaild_vertical)
                dif=i_to-i_from
                #움직임이 아래면 + 위로올라가면 dif -
                if dif<0:
                    re=int(1)
                else:
                    re=int(-1)
                for i in range(1,abs(dif)):
                    if i < abs(dif):
                        print("i",i)
                        print("re",re)
                        print("dif",dif)
                        print("i",board[i_from-(re*i)][j_from])
                        if board[i_from-(re*i)][j_from] != EMPTY:
                            print("vertical 움직임 실패")
                            is_ok=False
                            return False, board, "말의 이동위치로 가기 전 방해물이 있습니다"
                #움직이는 위치 전까지 방해물이 없다면
                if is_ok==True:
                    #그리고 가는곳이 비어있다면
                    if board[i_to][j_to] == EMPTY:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN
                        return True, board, f"{horse_color} QUEEN {from_positon[:2]} 에서 {to_position}로 이동"
                    #가는곳에 나의말이 있다
                    elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                        return False, board, "말의 이동위치에 나의 말이 있습니다"
                    #가는곳에 상대방의 말이 있다
                    else:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN
                        return True, board, f"{horse_color} QUEEN 을 {from_positon[:2]} 에서 {to_position}로 이동하며 상대방의{board[i_to][j_to][1]}을 잡았습니다"            

            elif isValid_diagonal:
                print("QUEEN diagonal vaild")
                if dif_i>0 and dif_j>0:
                    for i in range(1,abs(dif_i)):
                        if board[i_from+i][j_from+i]!=EMPTY:
                            is_ok=False
                            print("QUEEN ++ move")
                            break
                #위오른쪽 이동
                elif dif_i<0 and dif_j>0:
                    for i in range(1,abs(dif_i)):
                        if board[i_from-i][j_from+i]!=EMPTY:
                            is_ok=False
                            print("QUEEN +- move")
                            break
                #왼쪽아래 이동
                elif dif_i>0 and dif_j<0:
                    for i in range(1,abs(dif_i)):
                        if board[i_from+i][j_from-i]!=EMPTY:
                            is_ok=False
                            print("QUEEN -+ move")
                            break
                #왼쪽위 이동
                elif dif_i<0 and dif_j<0:
                    for i in range(1,abs(dif_i)):
                        if board[i_from-i][j_from-i]!=EMPTY:
                            is_ok=False
                            print("QUEEN -- move")
                            break

                if is_ok==True:
                    #그리고 가는곳이 비어있다면
                    if board[i_to][j_to] == EMPTY:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN

                        print("board",board)
                        print("board",type(board))
                        result = cls.isVaild_check('d1wK', board)
                        if result is not None:
                            isValid_check, tip = result
                            print("isValid_check",isValid_check)
                            print("tip",tip)
                        else:
                            #현재 플레이어 색 비교해서 내꺼 움직이면 체크인지 확인
                            #내꺼 체크면 나한테만 못움직인다 알려주기
                            #상대방기준 체크이면 알려주기
                            print("result",result)
                            # print("tip",tip)





                        return True, board, f"{horse_color} QUEEN 을 {from_positon[:2]} 에서 {to_position}로 이동"
                    #가는곳에 나의말이 있다
                    elif board[i_from][j_from][0]==board[i_to][j_to][0]:
                        return False, board, "말의 이동위치에 나의 말이 있습니다"
                    #가는곳에 상대방의 말이 있다
                    else:
                        board[i_from][j_from]=EMPTY
                        board[i_to][j_to] = from_positon[2] + QUEEN
                        return True, board, f"{horse_color} QUEEN 을 {from_positon[:2]} 에서 {to_position}로 이동하며 {board[i_to][j_to][1]}을 잡았습니다"                
            else:
                return False, board, "이동할 수 없는 위치 입니다."

        else:
            if isVaild_same_positon==False:
                return False, board, "같은 자리로 움직일 수 없습니다"
            elif isValid_pick_horse==False:
                return False, board, "이동하려는 체스말이 그 자리에 없습니다."
            else:
                return False, board, "선택 불가능한 위치 이거나 움직일 수 없는 위치 입니다"

    # 체크일때 True 그리고 체크인 말의 위치와 그 정보데이터 리턴하자
    # 말이 체크지 위치주고 그위치에 다른색 말이 공격할 수 있는게 있는지 다 돌려보는 함수
    @classmethod
    def isValid_check(cls, positon, board, attack_color = None):
        #00이 면 패스 같은팀 뭐 11이면 왼 오 아래 위 따로 확인
        print(positon) #a5wQ   
        print(positon[:2]) #a5wQ   
        isValid_from, i_positon, j_positon=cls.transform_str_to_num(positon[:2])
        horse_color= board[i_positon][j_positon][0]
        print(horse_color) #w

        # 체크메이트를 막을때 00 일경우에 색이없는데 공격자 색을 보내줌
        if attack_color is None:
            if horse_color == "w":
                op_color = "b"
            elif horse_color == "b":
                op_color = "w"
        else:
            horse_color = attack_color
        print(op_color)#b
        print(i_positon)
        print(j_positon)
        #TODO 직선 체크 R,Q
        left = int(8-(8-j_positon))
        right = int(8-j_positon)
        up = int(8-(8-i_positon))
        down = int(8-i_positon)
        #왼쪽
        # if i_positon + 2 < len(board) and j_positon + 1 < len(board[0]):
        if j_positon - 1 >= 0:
            for i in range(1,left+1):
                print(left)
                print("왼쪽 확인중")
                print("board[i_positon][j_positon]",board[i_positon][j_positon])
                print("board[i_positon][j_positon][0]",board[i_positon][j_positon][0])
                if board[i_positon][j_positon-i][0]==horse_color:
                    print("같은편이라서 괜찮")
                    break
                    # return True, "같은편이라서 괜찮"
                elif board[i_positon][j_positon-i]!=EMPTY:
                    if board[i_positon][j_positon-i]==op_color+"R" or board[i_positon][j_positon-1]==op_color+"Q":
                        print("board[i_positon][j_positon-i]==op_color+R",board[i_positon][j_positon-i]==op_color+"Q")
                        return True, board[i_positon][j_positon-i], i_positon, j_positon-i, "위치에서 체크입니다"
                else:
                    pass
        if j_positon + 1 < 8:
            for i in range(1,right+1):
                print(right)
                print("오른쪽 확인중")
                print("board[i_positon][j_positon][0]",board[i_positon][j_positon][0])
                if board[i_positon][j_positon+i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon][j_positon+i]!=EMPTY:
                    if board[i_positon][j_positon+i]==op_color+"R" or board[i_positon][j_positon+1]==op_color+"Q":
                        return True, board[i_positon][j_positon+i], i_positon, j_positon+i, "위치에서 체크입니다"

                else:
                    pass
        if i_positon - 1 >= 0:
            for i in range(1,up+1):
                print("위 확인중")
                if board[i_positon-i][j_positon][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon]!=EMPTY:
                    if board[i_positon-i][j_positon]==op_color+"R" or board[i_positon-i][j_positon]==op_color+"Q":
                        return True, board[i_positon-i][j_positon], i_positon-i, j_positon, "위치에서 체크입니다"
                else:
                    pass

        print("아래 시작전")
        if i_positon + 1 < 8:
            for i in range(1,down+1):
                print("아래 확인중")
                if board[i_positon+i][j_positon][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon]!=EMPTY:
                    if board[i_positon+i][j_positon]==op_color+"R" or board[i_positon+i][j_positon]==op_color+"Q":
                        return True, board[i_positon+i][j_positon], i_positon+i, j_positon, "위치에서 체크입니다"
                else:
                    pass

        #TODO 대각선 체크 Q,B
        #오른쪽 아래
        #왼쪽 아래
        #왼쪽 위
        #오른쪽 위
        #00 30
        #30이면 33에서 계산하는것과 같은 오른쪽아래의 개수임
        #옮기고 내 킹 계산 내가 킹을 옮겼다면 옮긴 킹위치데이터 줘야함
        #내가 다른말 움직여도 내꺼하고 상대방체크임 내가 뭘 피해서 공격하는거 생각하면 그사람 턴에 다 계산
        #00 11 22 33 44 숫자 큰걸로 같게만든 위치와 확인하는 수 같다
        # large_min=max(i_positon,j_positon)
        # diagonal_position=8-large_positon
        # print("large_positon",large_positon)
        # print("diagonal_position",diagonal_position)
        print("++대각 확인전")

        #오른쪽 아래 대각선
        if j_positon + 1 <= 8:
            for i in range(1, min(7 - i_positon, 7 - j_positon)):
                print("대각선")
                if board[i_positon+i][j_positon+i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon+i]!=EMPTY:
                    if board[i_positon+i][j_positon+i]==op_color+"B" or board[i_positon+i][j_positon+i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon+i][j_positon+i], i_positon+i, j_positon+i, "위치에서 체크입니다"
                else:
                    pass

        #왼쪽 아래 대각선
        if i_positon + 1 <= 8:
            print("+-대각 확인전")
            for i in range(1, min(7 - i_positon, j_positon) + 1):
                print("대각선 확인중")
                if board[i_positon+i][j_positon-i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon-i]!=EMPTY:
                    if board[i_positon+i][j_positon-i]==op_color+"B" or board[i_positon+i][j_positon-i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon+i][j_positon-i], i_positon+i, j_positon-i, "위치에서 체크입니다"
                else:
                    pass

        #왼쪽 위 대각선
        if i_positon + 1 <= 8:
            print("--대각 확인전")
            for i in range(1, min(i_positon, j_positon) + 1):
                if board[i_positon-i][j_positon-i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon-i]!=EMPTY:
                    if board[i_positon-i][j_positon-i]==op_color+"B" or board[i_positon-i][j_positon-i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon-i][j_positon-i], i_positon-i, j_positon-i, "위치에서 체크입니다"
                else:
                    pass

        #오른쪽 위 대각선
        if j_positon + 1 <= 8:
            print("-+대각 확인전")
            for i in range(1, min(i_positon, 7 - j_positon) + 1):
                print(i)
                if board[i_positon-i][j_positon+i][0]==horse_color:
                    print("break4")
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon+i]!=EMPTY:
                    print("대각선 확인중 00이 아님!")
                    print(board[i_positon-i][j_positon+i])
                    print(op_color+"B")
                    print(board[i_positon-i][j_positon+i]==op_color+"Q")
                    if board[i_positon-i][j_positon+i]==op_color+"B" or board[i_positon-i][j_positon+i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon-i][j_positon+i], i_positon-i, j_positon+i, "위치에서 체크입니다"
                    else:
                        print("왜 여기로?")
                else:
                    print("else")
                    pass

        #TODO 나이트8개
        if i_positon + 2 < len(board) and j_positon + 1 < len(board[0]):
            if board[i_positon+2][j_positon+1]==op_color+"N":
                return True, board[i_positon+2][j_positon+1], i_positon+2, j_positon+1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 2 < len(board) and j_positon - 1 < len(board[0]):
            if board[i_positon+2][j_positon-1]==op_color+"N":
                return True, board[i_positon+2][j_positon-1], i_positon+2, j_positon-1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 2 < len(board) and j_positon + 1 < len(board[0]):
            if board[i_positon-2][j_positon+1]==op_color+"N":
                return True, board[i_positon-2][j_positon+1], i_positon-2, j_positon+1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 2 < len(board) and j_positon - 1 < len(board[0]):
            if board[i_positon-2][j_positon-1]==op_color+"N":
                return True, board[i_positon-2][j_positon-1], i_positon-2, j_positon-1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 1 < len(board) and j_positon + 2 < len(board[0]):
            if board[i_positon+1][j_positon+2]==op_color+"N":
                return True, board[i_positon+1][j_positon+2], i_positon+1, j_positon+2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 1 < len(board) and j_positon + 2 < len(board[0]):
            if board[i_positon-1][j_positon+2]==op_color+"N":
                return True, board[i_positon-1][j_positon+2], i_positon-1, j_positon+2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 1 < len(board) and j_positon - 2 < len(board[0]):
            if board[i_positon+1][j_positon-2]==op_color+"N":
                return True, board[i_positon+1][j_positon-2], i_positon+1, j_positon-2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 1 < len(board) and j_positon - 2 < len(board[0]):
            if board[i_positon-1][j_positon-2]==op_color+"N":
                return True, board[i_positon-1][j_positon-2], i_positon-1, j_positon-2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"

        #TODO 상대폰
        if horse_color=="w":
            if board[i_positon-1][j_positon-1]==op_color+"P":
                return True, board[i_positon-1][j_positon-1], i_positon-1, j_positon-1, "위치에서 체크입니다"
            if board[i_positon-1][j_positon+1]==op_color+"P":
                return True, board[i_positon-1][j_positon+1], i_positon-1, j_positon+1, "위치에서 체크입니다"
        else:
            if board[i_positon+1][j_positon-1]==op_color+"P":
                return True, board[i_positon+1][j_positon-1], i_positon+1, j_positon-1, "위치에서 체크입니다"
            if board[i_positon+1][j_positon+1]==op_color+"P":
                return True, board[i_positon+1][j_positon+1], i_positon+1, j_positon+1, "위치에서 체크입니다"

    #체크메이트에 사용하는 킹이 움직일 수 있는 자리 판독
    @classmethod
    def isValid_king_move(cls, i_positon, j_positon):
        vaild_move=[]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                move_i, move_j = i_positon + i, j_positon + j
                # 체스판 범위 내에 있는지 확인
                if 0 <= move_i < 8 and 0 <= move_j < 8:
                    vaild_move.append((move_i, move_j))
        return vaild_move

    # 체크메이트 말로 막을 수 있는지 확인
    @classmethod
    def bolck_position(i_attack, j_attack, i_positon, j_positon):
        valid_move = []

        # 공격말 위치  먼저 넣기
        valid_move.append((i_attack, j_attack))

        # 수직으로 이동하는 경우
        if j_attack == j_positon:
            if i_attack < i_positon:
                step = 1
            else:
                step = -1
            for i in range(i_attack + step, i_positon, step):
                valid_move.append((i, j_attack))

        # 수평으로 이동하는 경우
        elif i_attack == i_positon:
            if j_attack < j_positon:
                step = 1
            else:
                step = -1
            for j in range(j_attack + step, i_positon, step):
                valid_move.append((i_attack, j))

        # 대각선으로 이동하는 경우
        elif abs(i_positon - i_attack) == abs(j_positon - j_attack):
            if i_attack < i_positon:
                step_i = 1
            else:
                step_i = -1
            if j_attack < j_positon:
                step_j = 1
            else:
                step_j = -1
            i, j = i_attack + step_i, j_attack + step_j
            while (i, j) != (i_positon, j_positon):
                valid_move.append((i, j))
                i += step_i
                j += step_j

        return valid_move

    #내꺼 체크 확인 내가 움직였으니
    #아니면 움직이는데 움직여서 상대방 체크를 했다
    #근데 모든곳에 움직여도 체크다 = 체크메이트
    #그럼 체크일때 모든 함수에 체크메이트 확인기능 넣어야함
    # if isVaild_check==True
    # 움직이고 체크 확인하고 내꺼 체크면 못움직인다
    # 내꺼 체크아니면 상대방 체크확인
    # 상대방 체크면 체크메이트 확인 = 이과정을 모든 피스 움직임에 넣음
    # 내 체크일때는 false로 체크다 못움직인다
    # 상대방이 체크다? 바로 체크메이트
    # 체크는 지금 말의 위치,  색으로 상대방 색 정함
    # 그럼 이것도 보내는 사람이랑 비교해서 보낸사람 체크일때는 그냥 반환하고 상대방 체크확인시 이 함수 넣기
    # 위치를 안다 블랙 화이트 움직인 사람의 색을안다 - 턴사용가능, 지금 턴구현 해놓은건 프론트 플레이어 1 2
    # 내체크 일때는 체크메이트 확인 x 상대 움직일때만 체크메이트 확인
    # 옮기고의 보드
    # 내 킹 상대 킹 함수를 따로만들까? 움직였을때 vs 내가 쓰고있는 함수를 함수안에서 쓰기
    
    # 킹과 상대 체크말 사이에 낄 수 있는지 확인해야함
    # 나이트는 무조건 공격해서 막을 수 있음
    # 대각선이나 직선은 따로해서 비숍 퀸은 대각선 막아야하고
    # 직선은 퀸 룩
    # 대각에 폰
    # 움직일 수 있는위치 확인했는데 상대방을 먹으면서 갈 수도 있음 
    # 사이에 공간없이 퀸이 대각에서 체크하는 경우는 지금으로써는 먹었을때 체크인지 확인해야함 먹고 체크를 하기때문에 이건 지금도 가능일듯?
    # 옮겼을때 체크가 아니면 
    # 지금 내가 체크를 했어 그럼 모든자리 둘러보며 (판 안의 범위) 모든위치 움직였을때 확인하고 있기때문에 체크메이트 아님
    # 그럼 여기서도 같은팀이 있다면 못움직인다 이게 구현이 되어있나? 다막혀있고 대각선으로 움직이면 죽음 대각에 퀸 있어서
    # 그위치에 팀이면 count 올려야함 못가니까
    # 지금은 갇혀있으면 내팀? (기능 추가해야하지만) 카운트 되고 대각으로 움직이면 체크라서 카운트 끝
    # 그 전에 사이 칸 하나당 테스트를 하는거지 올 수 있는애 있어?
    # 구석 킹일때 생각해보면 두칸 내팀 막혀있고 근데 걔가 또 먹을 수 있다면?
    # 일단 먹을 수 있으면 카운트 안되게 해서 체크메이트 안되고
    # 멀리서 체크다 이때는 사이에 모든 경우의수 생각해야함 이칸에 올수있는애 있나?
    # 각 칸에서 전부 직선에 퀸 룩 있나요 나이트 있나요 비숍있나요 캐슬링 가능한가요 폰은 색에따라 2칸움직임도 생각

    # 체크 - 도망갈자리 체크 - 도망못가네 막을 수 있어? 체크 - 없어?체크 막을때 가운데를 막거나 먹을 수 있는거 생각
    # 체크한 말과 킹의 사이의 모든 칸
    # 이건 도망갈 수 없음을 알고 막을 수 있는지 보는 마지막 희망임
    # 그래서 체크당한 위치에서 막는거 확인
    # 킹 퀸 이걸로할까 어짜피 체크는 확실해서 아니다 상관없이 그냥 거리해서 안에있는 좌표 찾자
    # 나이트는 공격해서 없애야함 각 자리에서 공격할 수 있는 말이 있는지 확인
    # 체크 함수를 사용해서 그위치에 올 수 있는걸 모두 계산했으니 근데 색이 다른걸 함 해보자
    @classmethod
    #TODO 폰 첫움직임이면 두칸 움직여서 막을 수 있음 직선으로 먹는건 불가능
    def isValid_block_checkmate(cls, i_attack, j_attack, i_positon, j_positon, board):
        attack_color=board[i_attack][j_attack][0]
        attack_horse=board[i_attack][j_attack][1]
        horse_color=board[i_positon][j_positon][0]
        horse=board[i_positon][j_positon][1]
        
        # 나이트는 공격해서 막을 수 있음
        # 나이트 자리에서 체크받을 수 있는지 확인
        if attack_horse == "N":
            str = cls.transform_num_to_str(i_attack, j_attack)
            # 체크함수 같이 못쓸 것 같은데 - 색을가려 - 색 파라미터 넣어줌
            # 체크냐? True 이면 막을 수 있다
            is_valid, check_position, check_i_positon, check_j_positon = cls.isValid_check(str, board, attack_color)
            if is_valid:
                return True, "block_checkmate"

        # 나머지는 위치를 생각해보고 일단
        # 체크인거 확인했으니 그 체크가 뭔지 알 수 있을까?
        # 체크함수 썼을때 00이면 상대색을 알수가 없어 - 색 파라미터 넣어줌
        elif attack_horse == "R" or attack_horse == "Q" or attack_horse == "B":
            #bolck_position 함수로 막을 수있는 함수 불러옴 공격자 자신의 위치까지
            position=cls.bolck_position(i_attack, j_attack, i_positon, j_positon)
            for i, s in position:
                str = cls.transform_num_to_str(i, s)
                is_valid, check_position, check_i_positon, check_j_positon = cls.isValid_check(str, board, attack_color)
                if is_valid:
                    return True, "block_checkmate"
        # 폰은 움직이는거랑 공격하는거 둘 다 생각해야할 듯
        # 공격자가 폰일때는 먹어서 방어밖에 안된다
        elif attack_horse == "P":
            str = cls.transform_num_to_str(i_attack, j_attack)
            is_valid, check_position, check_i_positon, check_j_positon = cls.isValid_check(str, board, attack_color)
            if is_valid:
                return True, "block_checkmate"
        else:
            print("말로 체크 막기에서 예외가 있다??")

    # 체크메이트를 킹을 움직여서 피해본다
    # 고민하는게 체크할때 내꺼 체크확인과 상대방 체크확인 나눌지
    # 체크 걸고 체크이면 체크메이트 바로 확인
    @classmethod
    def isValid_checkmate(cls, i_positon, j_positon, board):
        # 킹 움직임 8개의 경우의 수
        # i_positon, j_positon 킹의 위치
        vaild_move=cls.isValid_king_move(i_positon, j_positon)
        # list[[0,1],[1,0],[1,1]]
        # false 가 체크일 경우임
        check_count=0
        for i in vaild_move:
            # 왕의 위치에서 체크인지 확인
            # 움직일 수 있는위치인지도 확인해야함 이건 폰움직이고 그런게 아니라서
            # 옆이 내 말이면 그냥 넘어감 체크 확인 x
            # 지금 체크코드는 움직인 위치에서 확인 상대방 움직이지 않은 위치에서 체크 그냥 그위치 있을때 체크냐 아니냐 확인하는거임
            # 내가 움직이고 하는 체크는 움직일수 있는 위치에 움직인거임
            # 가만히 있는 체크확인에서는 모두 움직일 수있다고 판단될수도 있다 - move함수 안쓰고 확인하는거기 때문에
            # 세군데중 두군데가 내꺼면 카운트 해야함

            #체크확인 말과 옮긴위치에 있는말의 색이 같다면 못가는 곳이기 때문에 check_count+1
            if board[i_positon+i][j_positon+i][0]==board[i_positon][j_positon][0]:
                check_count+=1
            # 옮긴곳이 내편이 아니다 먹은것도 가정(먹고 체크아닌경우니까) 체크확인 체크면 +1
            elif board[i_positon+i][j_positon+i][0]!=board[i_positon][j_positon][0]:
                isValid_check, attack_horse, i_attack, j_attack, tip=cls.isValid_check(i_positon+i, j_positon+i, board)
                if isValid_check:
                    check_count+=1
            else:
                print("킹 움직여서 체크메이트에서 예외")

        # 가능한 자리에 모두 옮겨 봤지만 체크다 = checkmate True
        if check_count==len(vaild_move):
            #마지막으로 막아서 죽여서 체크메이트를 막을수 있나?
            isValid_block_checkmate, mes=cls.isValid_block_checkmate(attack_horse, i_attack, j_attack,i_positon, j_positon,board)
            #막을 수 있다면
            if isValid_block_checkmate:
                return False, "block checkmate"

            else:
                return True, "checkmate"

###############################################################################################3
    # 체크일때 True 그리고 체크인 말의 위치와 그 정보데이터 리턴하자
    # 말이 체크지 위치주고 그위치에 다른색 말이 공격할 수 있는게 있는지 다 돌려보는 함수
    # 옮긴 다음에 상대의 입장에서 체크체크
    # 상대를 어케 구별할건데 = 말 움직인다 - 움직인 보드에서 내꺼랑 니 킹위치 확인한다(체크면 못옮겨)(니 체크면 체크메이트 확인할거야 ) - 전달자 id랑 캐시 플레이어 1,2 확인 1이면 화이트 = 흰색 킹위치 검열 = 검은색 킹위치 검열
    # 내꺼는 움직였을때 체크이면 안되고 - 내가 움직인거 기준 - 안된다
    # 상대는 내가 움직인 말에 체크인지 확인하는 것 - 내가 움직인거 기준 - 체크일때 달라지는 거임 - 체크면 알림 그리고 상대 무조건 피하고 막아야함 - 체크메이트인지 판단

    # 두가지 기능 체크확인, 체크메이트 막을 수 있는지 확인할때 씀(이걸쓸지 그냥 체크쓸지? 모르겠네)
    @classmethod
    def isValid_op_check(cls, positon, board, attack_color = None):
        #00이 면 패스 같은팀 뭐 11이면 왼 오 아래 위 따로 확인
        print(positon) #a5wQ   
        print(positon[:2]) #a5wQ

        #a2wP -> i 7 j 1
        # 1 킹 위치 들어옴
        isValid_from, i_positon, j_positon=cls.transform_str_to_num(positon[:2])
        horse_color= board[i_positon][j_positon][0]
        print(horse_color) #w

        # 2 체크메이트를 막을때 00 일경우에 색이없는데 공격자 색을 보내줌
        if attack_color is None:
            if horse_color == "w":
                op_color = "b"
            elif horse_color == "b":
                op_color = "w"
        else:
            horse_color = attack_color
        print(op_color)#b
        print(i_positon)
        print(j_positon)

        # 직선 체크 R,Q
        left = int(8-(8-j_positon))
        right = int(8-j_positon)
        up = int(8-(8-i_positon))
        down = int(8-i_positon)
        # 왼쪽
        if j_positon - 1 >= 0:
            for i in range(1,left+1):
                print(left)
                print("왼쪽 확인중")
                print("board[i_positon][j_positon]",board[i_positon][j_positon])
                print("board[i_positon][j_positon][0]",board[i_positon][j_positon][0])
                if board[i_positon][j_positon-i][0]==horse_color:
                    print("같은편이라서 괜찮")
                    break
                    # return True, "같은편이라서 괜찮"
                elif board[i_positon][j_positon-i]!=EMPTY:
                    if board[i_positon][j_positon-i]==op_color+"R" or board[i_positon][j_positon-1]==op_color+"Q":
                        print("board[i_positon][j_positon-i]==op_color+R",board[i_positon][j_positon-i]==op_color+"Q")
                        return True, board[i_positon][j_positon-i], i_positon, j_positon-i, "위치에서 체크입니다"
                else:
                    pass
        if j_positon + 1 < 8:
            for i in range(1,right+1):
                print(right)
                print("오른쪽 확인중")
                print("board[i_positon][j_positon][0]",board[i_positon][j_positon][0])
                if board[i_positon][j_positon+i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon][j_positon+i]!=EMPTY:
                    if board[i_positon][j_positon+i]==op_color+"R" or board[i_positon][j_positon+1]==op_color+"Q":
                        return True, board[i_positon][j_positon+i], i_positon, j_positon+i, "위치에서 체크입니다"

                else:
                    pass
        if i_positon - 1 >= 0:
            for i in range(1,up+1):
                print("위 확인중")
                if board[i_positon-i][j_positon][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon]!=EMPTY:
                    if board[i_positon-i][j_positon]==op_color+"R" or board[i_positon-i][j_positon]==op_color+"Q":
                        return True, board[i_positon-i][j_positon], i_positon-i, j_positon, "위치에서 체크입니다"
                else:
                    pass

        print("아래 시작전")
        if i_positon + 1 < 8:
            for i in range(1,down+1):
                print("아래 확인중")
                if board[i_positon+i][j_positon][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon]!=EMPTY:
                    if board[i_positon+i][j_positon]==op_color+"R" or board[i_positon+i][j_positon]==op_color+"Q":
                        return True, board[i_positon+i][j_positon], i_positon+i, j_positon, "위치에서 체크입니다"
                else:
                    pass

        #대각선 체크 Q,B
        #오른쪽 아래
        #왼쪽 아래
        #왼쪽 위
        #오른쪽 위
        #00 30
        #30이면 33에서 계산하는것과 같은 오른쪽아래의 개수임
        #옮기고 내 킹 계산 내가 킹을 옮겼다면 옮긴 킹위치데이터 줘야함
        #내가 다른말 움직여도 내꺼하고 상대방체크임 내가 뭘 피해서 공격하는거 생각하면 그사람 턴에 다 계산
        #00 11 22 33 44 숫자 큰걸로 같게만든 위치와 확인하는 수 같다
        # large_min=max(i_positon,j_positon)
        # diagonal_position=8-large_positon
        # print("large_positon",large_positon)
        # print("diagonal_position",diagonal_position)
        print("++대각 확인전")

        # 오른쪽 아래 대각선
        if j_positon + 1 <= 8:
            for i in range(1, min(7 - i_positon, 7 - j_positon)):
                print("대각선")
                if board[i_positon+i][j_positon+i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon+i]!=EMPTY:
                    if board[i_positon+i][j_positon+i]==op_color+"B" or board[i_positon+i][j_positon+i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon+i][j_positon+i], i_positon+i, j_positon+i, "위치에서 체크입니다"
                else:
                    pass

        # 왼쪽 아래 대각선
        if i_positon + 1 <= 8:
            print("+-대각 확인전")
            for i in range(1, min(7 - i_positon, j_positon) + 1):
                print("대각선 확인중")
                if board[i_positon+i][j_positon-i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon+i][j_positon-i]!=EMPTY:
                    if board[i_positon+i][j_positon-i]==op_color+"B" or board[i_positon+i][j_positon-i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon+i][j_positon-i], i_positon+i, j_positon-i, "위치에서 체크입니다"
                else:
                    pass

        # 왼쪽 위 대각선
        if i_positon + 1 <= 8:
            print("--대각 확인전")
            for i in range(1, min(i_positon, j_positon) + 1):
                if board[i_positon-i][j_positon-i][0]==horse_color:
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon-i]!=EMPTY:
                    if board[i_positon-i][j_positon-i]==op_color+"B" or board[i_positon-i][j_positon-i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon-i][j_positon-i], i_positon-i, j_positon-i, "위치에서 체크입니다"
                else:
                    pass

        # 오른쪽 위 대각선
        if j_positon + 1 <= 8:
            print("-+대각 확인전")
            for i in range(1, min(i_positon, 7 - j_positon) + 1):
                print(i)
                if board[i_positon-i][j_positon+i][0]==horse_color:
                    print("break4")
                    # return True, "같은편이라서 괜찮"
                    break
                elif board[i_positon-i][j_positon+i]!=EMPTY:
                    print("대각선 확인중 00이 아님!")
                    print(board[i_positon-i][j_positon+i])
                    print(op_color+"B")
                    print(board[i_positon-i][j_positon+i]==op_color+"Q")
                    if board[i_positon-i][j_positon+i]==op_color+"B" or board[i_positon-i][j_positon+i]==op_color+"Q":
                        print("대각 체크있음")
                        return True, board[i_positon-i][j_positon+i], i_positon-i, j_positon+i, "위치에서 체크입니다"
                    else:
                        print("왜 여기로?")
                else:
                    print("else")
                    pass

        # 나이트8개
        if i_positon + 2 < len(board) and j_positon + 1 < len(board[0]):
            if board[i_positon+2][j_positon+1]==op_color+"N":
                return True, board[i_positon+2][j_positon+1], i_positon+2, j_positon+1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 2 < len(board) and j_positon - 1 < len(board[0]):
            if board[i_positon+2][j_positon-1]==op_color+"N":
                return True, board[i_positon+2][j_positon-1], i_positon+2, j_positon-1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 2 < len(board) and j_positon + 1 < len(board[0]):
            if board[i_positon-2][j_positon+1]==op_color+"N":
                return True, board[i_positon-2][j_positon+1], i_positon-2, j_positon+1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 2 < len(board) and j_positon - 1 < len(board[0]):
            if board[i_positon-2][j_positon-1]==op_color+"N":
                return True, board[i_positon-2][j_positon-1], i_positon-2, j_positon-1, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 1 < len(board) and j_positon + 2 < len(board[0]):
            if board[i_positon+1][j_positon+2]==op_color+"N":
                return True, board[i_positon+1][j_positon+2], i_positon+1, j_positon+2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 1 < len(board) and j_positon + 2 < len(board[0]):
            if board[i_positon-1][j_positon+2]==op_color+"N":
                return True, board[i_positon-1][j_positon+2], i_positon-1, j_positon+2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon + 1 < len(board) and j_positon - 2 < len(board[0]):
            if board[i_positon+1][j_positon-2]==op_color+"N":
                return True, board[i_positon+1][j_positon-2], i_positon+1, j_positon-2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"
        if i_positon - 1 < len(board) and j_positon - 2 < len(board[0]):
            if board[i_positon-1][j_positon-2]==op_color+"N":
                return True, board[i_positon-1][j_positon-2], i_positon-1, j_positon-2, "위치에서 체크입니다"
            else:
                return False, "같은편이나 다른종류의 말"

        # 상대폰
        if horse_color=="w":
            if board[i_positon-1][j_positon-1]==op_color+"P":
                return True, board[i_positon-1][j_positon-1], i_positon-1, j_positon-1, "위치에서 체크입니다"
            if board[i_positon-1][j_positon+1]==op_color+"P":
                return True, board[i_positon-1][j_positon+1], i_positon-1, j_positon+1, "위치에서 체크입니다"
        else:
            if board[i_positon+1][j_positon-1]==op_color+"P":
                return True, board[i_positon+1][j_positon-1], i_positon+1, j_positon-1, "위치에서 체크입니다"
            if board[i_positon+1][j_positon+1]==op_color+"P":
                return True, board[i_positon+1][j_positon+1], i_positon+1, j_positon+1, "위치에서 체크입니다"


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

            #                 if dif_i>0 and dif_j>0:
            #     for i in range(1,abs(dif_i)):
            #         if board[i_from+i][j_from+i]!=EMPTY:
            #             is_ok=False
            #             print("bishop ++ move false")
            #             break
            # #위오른쪽 이동
            # elif dif_i<0 and dif_j>0:
            #     for i in range(1,abs(dif_i)):
            #         if board[i_from-i][j_from+i]!=EMPTY:
            #             is_ok=False
            #             print("bishop +- move false")
            #             break
            # #왼쪽아래 이동
            # elif dif_i>0 and dif_j<0:
            #     for i in range(1,abs(dif_i)):
            #         if board[i_from+i][j_from-i]!=EMPTY:
            #             is_ok=False
            #             print("bishop -+ move false")
            #             break
            # #왼쪽위 이동
            # elif dif_i<0 and dif_j<0:
            #     for i in range(1,abs(dif_i)):
            #         if board[i_from-i][j_from-i]!=EMPTY:
            #             is_ok=False
            #             print("bishop -- move false")
            #             break

