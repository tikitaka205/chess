from django.shortcuts import render

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
        self.create_board()

    def create_board(self):
        for i in range(chess_board_cells):
            row=[]
            for s in range(chess_board_cells):
                row.append(EMPTY)
            self.board.append(row)

    def print_board(self):
        for i in range(chess_board_cells):
            for s in range(chess_board_cells):
                print(self.board[i][s], end=" ")
            print()

    def erase_board(self):
        for i in range(chess_board_cells):
            for s in range(chess_board_cells):
                self.board[i][s]=EMPTY

    def is_valid_position_str(self,position_str):
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
    def transform_str_to_num(self, position_str):
        if self.is_valid_position_str(position_str):
            i=chess_board_cells-int(position_str[1])
            j=ord(position_str[0])-ord('a')
            # print("j",j)
            # print("i",i)
            return True, i, j
        else:
            return False,0,0
    
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

        self.print_board()

    #move_pawn('a7bP','a6')
    #제자리에 놓기
    #horse vaild
    #지금자리와 옮기는자리 같으면 안된다
    #옮기려는 부분이 체스판 밖이 아닐까
    #i는 변하지만 j는 변하지 않는다
    #움직이려는 곳에 말이 있으면 안된다
    #조건을 만족하면 움직일 것이다
    #들어오는 조건을 계속 생각해보자
    #반복문으로 장애물 확인
    def move_pawn(self, from_positon, to_position):
        if from_positon[:-2] ==to_position:
            return False
        isValid_from, i_from, j_from=self.transform_str_to_num(from_positon[:2])
        isValid_to, i_to, j_to=self.transform_str_to_num(to_position)
        isJPositionSame=j_from==j_to
        isIPositionSame=i_from!=i_to
        isGoPositonEmpty=self.board[i_to][j_to]==EMPTY
        isValid = isValid_to and isValid_from and isJPositionSame and isIPositionSame and isGoPositonEmpty
        print("move_pawn", i_from, j_from, i_to, j_to) #여기서 i j 는 실제 0,0을 의미
        if isValid:
            dif=i_to-i_from
            print("dif",dif)
            if from_positon[-2]==BLACK:
                print("black")
                if dif >= 1 and dif <= 2: #if=1 or 2 로 해도 될듯?
                    print("1,2칸 움직임")
                    #앞에 말이 막고있는지 확인
                    # is_okay=True
                    for i in range(1, dif+1): #항상 그냥 숫자만 적지말고 연관된 숫자를 활용하자
                        if self.board[i_from + i][j_from]!=EMPTY:
                            # is_okay=False
                            # break
                            return False
                        else:
                            self.board[i_from][j_from]=EMPTY
                            print("원래있던 자리 지움")
                            self.board[i_to][j_to]=from_positon[2] + PAWN
                            print("제대로 움직임")
                            return True
                else:
                    print("한칸 이상 움직임")
                    return False
            if from_positon[-2]==WHITE:
                print("WHITE")
                if dif >= -2 and dif <= -1:
                    for i in range(1, abs(dif)+1):
                        if self.board[i_from + i][j_from]!=EMPTY:
                            return False
                        else:
                            self.board[i_from][j_from]=EMPTY
                            self.board[i_to][j_to]=from_positon[0] + PAWN
                            return True
                else:
                    return False
        else:
            return False

chess=Chess()
chess.set_game() #=Chess().print_board() 체스 클래스에 print_board()라는 함수를 실행
chess.move_pawn('a7bP','a5')
chess.print_board()



# chess.print_board()
# print(chess.print_board)
# chess.set_cell('d3',WHITE+KING)
# chess.set_cell('e3',BLACK+KING)
# chess.set_cell('a8',WHITE+KING)
# Chess().print_board()
