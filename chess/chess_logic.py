# i,j의 위치
chess_board_cells=8
EMPTY='00'
KING='K'
QUEEN='Q'
BISHOP='B'
KNIGHT='N'
ROOK='R'
PAWN='P'

BLACK='b'
WHITE='w'


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

    # @classmethod
    # def vaild_pick_horse(cls, from_positon, to_position, board):
    #     isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
    #     isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
    #     board[i_from][j_from]=from_positon[2:]

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
            return False
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isJPositionSame=j_from==j_to
        isIPositionSame=i_from!=i_to
        isGoPositonEmpty=board[i_to][j_to]==EMPTY
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        isValid = isValid_to and isValid_from and isJPositionSame and isIPositionSame and isGoPositonEmpty and isValid_pick_horse
        print("move_pawn", i_from, j_from, i_to, j_to) #여기서 i j 는 실제 0,0을 의미
        if isValid:
            dif=i_to-i_from
            print("valid")
            if from_positon[-2]==BLACK:
                # print("black")
                if dif >= 1 and dif <= 2: #if=1 or 2 로 해도 될듯?
                    # print("1,2칸 움직임")
                    #앞에 말이 막고있는지 확인
                    # is_okay=True
                    for i in range(1, dif+1): #항상 그냥 숫자만 적지말고 연관된 숫자를 활용하자
                        if board[i_from + i][j_from]!=EMPTY:
                            # is_okay=False
                            # break
                            return False, board, "can't move position"
                        else:
                            board[i_from][j_from]=EMPTY
                            print("원래있던 자리 지움")
                            board[i_to][j_to]=from_positon[2] + PAWN
                            print("제대로 움직임")
                            print(board)
                            return True, board, f"{j_to},{i_to}로 이동"
                else:
                    print("한칸 이상 움직임")
                    return False
            if from_positon[-2]==WHITE:
                # print("WHITE")
                if dif >= -2 and dif <= -1:
                    for i in range(1, abs(dif)+1):
                        if board[i_from - i][j_from]!=EMPTY:
                            return False, board, "can't move position"
                        else:
                            board[i_from][j_from]=EMPTY
                            board[i_to][j_to]=from_positon[2] + PAWN
                            # print("white움직임")
                            return True, board, f"{j_to},{i_to}로 이동"
                else:
                    return False
        else:
            print("invalid")
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
                print("호리즌",isVaild_horizon)
                dif=j_to-j_from
                for i in range(1,abs(dif)+1):
                    # i_from이 a1 이면 i,j는 0부터 해서 i=7 j=0이 된다
                    #여기서 조건이 되면 + 된다면 위, 오른쪽 - 되면 아래, 왼쪽
                    #위로 움직이면 i_dif가 -된다
                    #6-8 =-2움직임 = 위
                    #8-6 = 2움직임 = 아래
                    if i < dif:
                        if board[i_from][j_from+i] != EMPTY:
                            print("horizon 움직임 실패")
                            is_ok=False
                            break

            elif isVaild_vertical:
                print("버티컬",isVaild_vertical)
                dif=i_to-i_from
                for i in range(1,abs(dif)+1):
                    #룩이 위로움직냐 아래로 움직이냐
                    #룩 위로 움직임
                    if i > dif:
                        if board[i_from-i][j_from] != EMPTY:
                            #전부다 확인하고 그 조건이 맞으면 옮겨야함
                            #5에서 0으로 이동 dif=-5
                            #0-7범위 여기범위에서는
                            #b3 b8이 뚫린다 범위 체크다시 확인
                            #5->0
                            #0-5까지 확인
                            print("i",i)
                            print("vertical 위 움직임 실패")
                            is_ok=False
                            break
            if is_ok:
                    board[i_from][j_from]=EMPTY
                    board[i_to][j_to] = from_positon[2] + ROOK
                    return True, board, f"{j_to},{i_to}로 이동"
        else:
            print("룩 vaild 실패")
            return False, board, "check your position"

    #같은자리 금지
    #대각선 다른말의 유무
    #절대값 같아야함
    #i차이 j차이가 같아야 한다
    #a1 b2 c3 d4

    @classmethod
    def move_bishop(cls,from_positon, to_position, board):
        isValid_from, i_from, j_from=cls.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=cls.transform_str_to_num(to_position)
        isValid_pick_horse=board[i_from][j_from]==from_positon[2:]
        print("isValid_pick_horse",isValid_pick_horse)
        print("from_positon[2:]",from_positon[2:])
        dif_i=i_to-i_from
        dif_j=j_to-j_from
        isValid_diagonal=abs(dif_i)==abs(dif_j)
        isValid=isValid_from and isValid_to and isValid_diagonal and isValid_pick_horse
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
                for i in range(1,abs(dif_i)+1):
                    if board[i_from+i][j_from+i]!=EMPTY:
                        is_ok=False
                        print("bishop ++ move false")
                        break
                    else:
                        print("bishop ++ move true")
                        pass
            #위오른쪽 이동
            elif dif_i<0 and dif_j>0:
                for i in range(1,abs(dif_i)+1):
                    if board[i_from-i][j_from+i]!=EMPTY:
                        is_ok=False
                        print("bishop +- move false")
                        break
                    else:
                        print("bishop +- move true")
                        pass
            #왼쪽아래 이동
            elif dif_i>0 and dif_j<0:
                for i in range(1,abs(dif_i)+1):
                    if board[i_from+i][j_from-i]!=EMPTY:
                        is_ok=False
                        print("bishop -+ move false")
                        break
                    else:
                        print("bishop -+ move true")
                        pass
            #왼쪽위 이동
            elif dif_i<0 and dif_j<0:
                for i in range(1,abs(dif_i)+1):
                    if board[i_from-i][j_from-i]!=EMPTY:
                        is_ok=False
                        print("bishop -- move false")
                        break
                    else:
                        print("bishop -- move true")
                        pass
        #vaild 통과 불가
        else:
            return False, board, "check your position"
        #움직이려는 위치가 괜찮다면 이동
        if is_ok==True:
            print("BISHOP move")
            board[i_from][j_from]=EMPTY
            board[i_to][j_to] = from_positon[2] + BISHOP
            return True, board, f"{j_to},{i_to}로 이동"
        else:
            return False, board, "check your position"


    #'b2wN,c3' +1+2 +1
    #한칸 가고 대각선
    #i,j 네방향 + 옆으로 두가지씩 8개의 경우의 수
    #움직임 범위 1이상 2이하
    @classmethod
    def move_knight(cls,from_positon, to_position, board):
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
            board[i_from][j_from]=EMPTY
            board[i_to][j_to] = from_positon[2] + KNIGHT
            return True, board, f"{j_to},{i_to}로 이동"
        else:
            print("KNIGHT invalid")
            return False, board, "check your position"

        #TODO to_position이동시 체크가 되면 안된다
        #TODO 여기서 같은팀 공격불가 기능 만들어보자
        #TODO 공격 기능도 만들어보자
        #TODO 캐슬링


    @classmethod
    def move_king(cls,from_positon, to_position, board):
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
            return True, board, f"{j_to},{i_to}로 이동"
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
                print("호리즌",isVaild_horizon)
                dif=j_to-j_from
                for i in range(1,abs(dif)+1):
                    if i < dif:
                        if board[i_from][j_from+i] != EMPTY:
                            print("horizon 움직임 실패")
                            is_ok=False
                            break

            elif isVaild_vertical:
                print("버티컬",isVaild_vertical)
                dif=i_to-i_from
                for i in range(1,abs(dif)+1):
                    if i > dif:
                        if board[i_from-i][j_from] != EMPTY:
                            print("i",i)
                            print("vertical 위 움직임 실패")
                            is_ok=False
                            break
                        
            elif isValid_diagonal:
                print("QUEEN vaild")
                if dif_i>0 and dif_j>0:
                    for i in range(1,abs(dif_i)+1):
                        if board[i_from+i][j_from+i]!=EMPTY:
                            is_ok=False
                            print("QUEEN ++ move")
                            pass
                if dif_i<0 and dif_j>0:
                    for i in range(1,abs(dif_i)+1):
                        if board[i_from-i][j_from+i]!=EMPTY:
                            is_ok=False
                            print("QUEEN +- move")
                            pass
                if dif_i>0 and dif_j<0:
                    for i in range(1,abs(dif_i)+1):
                        if board[i_from+i][j_from-i]!=EMPTY:
                            is_ok=False
                            print("QUEEN -+ move")
                            pass
                if dif_i<0 and dif_j<0:
                    for i in range(1,abs(dif_i)+1):
                        if board[i_from-i][j_from-i]!=EMPTY:
                            is_ok=False
                            print("QUEEN -- move")
                            pass
            else:
                print("이동가능 위치가 아닙니다")
                return False, board, "check your position"

            if is_ok==True:
                print("QUEEN move")
                board[i_from][j_from]=EMPTY
                board[i_to][j_to] = from_positon[2] + QUEEN
                return True, board, f"{j_to},{i_to}로 이동"
            else:
                print('is_okay=false')
                return False, board, "check your position"

        else:
            print("isVaild",isVaild)
            print("QUEEN invaild")
            return False, board, "check your position"


# chess=Chess()
# chess.set_game() #=Chess().print_board() 체스 클래스에 print_board()라는 함수를 실행
# # chess.move_pawn('a7bP','a5')#폰 아래로 이동
# # chess.move_pawn('b7bP','b5')#폰 아래로 이동
# # chess.move_pawn('a2wP','a4')#폰 위로이동
# # chess.move_rook('a1wR','a3')#룩 위로이동
# # chess.move_rook('a3wR','d3')#룩 오른쪽 이동
# # # chess.move_rook('d3wR','b3')#룩 왼쪽이동
# # chess.move_rook('b3wR','b7'),print("말을 넘어가")#말을 넘어가는 에러
# chess.move_pawn('b2wB','b4')#폰 이동
# chess.move_pawn('e2wB','e4')#폰 이동
# chess.move_bishop('c1wB','a3')#비숍 왼쪽위 이동
# chess.move_knight('b1wN','c3')#나이트 이동
# # chess.move_knight('c3wN','b5')#나이트 이동
# chess.move_queen('e1wQ','e3')#퀸 이동
# chess.move_queen('e3wQ','h6')#퀸 이동
# chess.move_king('d1wQ','b1')#킹이동
# # chess.move_rook('b8wR','b3')#룩 아래이동
# chess.print_board()

# chess.print_board()
# print(chess.print_board)
# chess.set_cell('d3',WHITE+KING)
# chess.set_cell('e3',BLACK+KING)
# chess.set_cell('a8',WHITE+KING)
# Chess().print_board()