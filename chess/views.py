from django.shortcuts import render


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
# Create your views here.
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

chess=Chess()
# chess.create_board()
print(chess.board)