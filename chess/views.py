from django.shortcuts import render

# i,j의 위치
chess_board_cells=8
EMPTY='000'
KING='k'
QUEEN='q'
BISHOP='b'
KNIGHT='n'
ROOK='r'
PAWN='w'

BLACK='bl'
WHITE='wh'

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
    def transform_str_to_num(self, position_str):
        if self.is_valid_position_str(position_str):
            i=chess_board_cells-int(position_str[1])
            j=ord(position_str[0])-ord('a')
            return True, i, j
        else:
            return False,0,0

    def set_cell(self,position_str,horse_type_str):
        isVaild, i, j=self.transform_str_to_num(position_str)
        if isVaild:
            self.board[i][j]=horse_type_str
            return True
        else:
            return False
chess=Chess()
# chess.print_board()
# print(chess.print_board)
chess.set_cell('d3',WHITE+KING)
chess.set_cell('e3',BLACK+KING)
chess.set_cell('a8',WHITE+KING)
chess.print_board() #=Chess().print_board() 체스 클래스에 print_board()라는 함수를 실행
# Chess().print_board()
    