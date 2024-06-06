"""
chess_bot
"""

import copy  # used to create deep copies of the board

# The board is implemented as a 2d array of strings
board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],  # 0

         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # 1

         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # 2

         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # 3

         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # 4

         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # 5

         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # 6

         ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]  # 7
#          0     1     2     3     4     5     6     7


check = False  # global variable for whether a king is checked
non_progress_counter = 0  # counter for 50 moves draw


class Piece:
    # class for pieces
    def __init__(self, piece_type, value):
        self.type = piece_type  # type of piece ex. wp
        self.value = value

    def movement(self, y, x):
        # list of moves piece can make
        piece_moves = []
        # arrays used to identify which pieces can be captured
        take_black = ["bp", "br", "bb", "bn", "bq", "bk"]
        take_white = ["wp", "wr", "wb", "wn", "wq", "wk"]
        take_general = []

        # pieces that can be capture determined based on color of piece
        if self.type in take_black:
            take_general = take_white
        if self.type in take_white:
            take_general = take_black

        # movement rules for white pawns
        if self.type == "wp":
            if board[y - 1][x] == "  ":
                piece_moves.append((y - 1, x))
                if y == 6 and board[y - 2][x] == "  ":
                    piece_moves.append((y - 2, x))
            if x != 0:
                if board[y - 1][x - 1] in take_black:
                    piece_moves.append((y - 1, x - 1))
            if x != 7:
                if board[y - 1][x + 1] in take_black:
                    piece_moves.append((y - 1, x + 1))

        # movement rules for black pawns
        if self.type == "bp":
            if board[y + 1][x] == "  ":
                piece_moves.append((y + 1, x))
                if y == 1 and board[y + 2][x] == "  ":
                    piece_moves.append((y + 2, x))
            if x != 0:
                if board[y + 1][x - 1] in take_white:
                    piece_moves.append((y + 1, x - 1))
            if x != 7:
                if board[y + 1][x + 1] in take_white:
                    piece_moves.append((y + 1, x + 1))

        # movement rules for knights
        if self.type == "wn" or self.type == "bn":
            if y - 2 >= 0 and x - 1 >= 0:
                if board[y - 2][x - 1] in take_general or board[y - 2][x - 1] == "  ":
                    piece_moves.append((y - 2, x - 1))
            if y - 1 >= 0 and x - 2 >= 0:
                if board[y - 1][x - 2] in take_general or board[y - 1][x - 2] == "  ":
                    piece_moves.append((y - 1, x - 2))
            if y - 2 >= 0 and x + 1 <= 7:
                if board[y - 2][x + 1] in take_general or board[y - 2][x + 1] == "  ":
                    piece_moves.append((y - 2, x + 1))
            if y - 1 >= 0 and x + 2 <= 7:
                if board[y - 1][x + 2] in take_general or board[y - 1][x + 2] == "  ":
                    piece_moves.append((y - 1, x + 2))
            if y + 2 <= 7 and x - 1 >= 0:
                if board[y + 2][x - 1] in take_general or board[y + 2][x - 1] == "  ":
                    piece_moves.append((y + 2, x - 1))
            if y + 1 <= 7 and x - 2 >= 0:
                if board[y + 1][x - 2] in take_general or board[y + 1][x - 2] == "  ":
                    piece_moves.append((y + 1, x - 2))
            if y + 2 <= 7 and x + 1 <= 7:
                if board[y + 2][x + 1] in take_general or board[y + 2][x + 1] == "  ":
                    piece_moves.append((y + 2, x + 1))
            if y + 1 <= 7 and x + 2 <= 7:
                if board[y + 1][x + 2] in take_general or board[y + 1][x + 2] == "  ":
                    piece_moves.append((y + 1, x + 2))

        # movement rules for kings
        if self.type == "wk" or self.type == "bk":
            if y - 1 >= 0:
                if board[y - 1][x] in take_general or board[y - 1][x] == "  ":
                    piece_moves.append((y - 1, x))
            if y + 1 <= 7:
                if board[y + 1][x] in take_general or board[y + 1][x] == "  ":
                    piece_moves.append((y + 1, x))
            if x - 1 >= 0:
                if board[y][x - 1] in take_general or board[y][x - 1] == "  ":
                    piece_moves.append((y, x - 1))
            if x + 1 <= 7:
                if board[y][x + 1] in take_general or board[y][x + 1] == "  ":
                    piece_moves.append((y, x + 1))
            if y - 1 >= 0 and x - 1 >= 0:
                if board[y - 1][x - 1] in take_general or board[y - 1][x - 1] == "  ":
                    piece_moves.append((y - 1, x - 1))
            if y + 1 <= 7 and x - 1 >= 0:
                if board[y + 1][x - 1] in take_general or board[y + 1][x - 1] == "  ":
                    piece_moves.append((y + 1, x - 1))
            if y + 1 <= 7 and x + 1 <= 7:
                if board[y + 1][x + 1] in take_general or board[y + 1][x + 1] == "  ":
                    piece_moves.append((y + 1, x + 1))
            if y - 1 >= 0 and x + 1 <= 7:
                if board[y - 1][x + 1] in take_general or board[y - 1][x + 1] == "  ":
                    piece_moves.append((y - 1, x + 1))

        # movement rules for rooks
        if self.type == "wr" or self.type == "br":
            dead_end_n = False
            dead_end_s = False
            dead_end_w = False
            dead_end_e = False
            for square in range(1, 9):
                if y - square >= 0 and not dead_end_n:
                    if board[y - square][x] == "  ":
                        piece_moves.append((y - square, x))
                    elif board[y - square][x] in take_general:
                        piece_moves.append((y - square, x))
                        dead_end_n = True
                    if board[y - square][x] not in take_general and board[y - square][x] != "  ":
                        dead_end_n = True
                if y + square <= 7 and not dead_end_s:
                    if board[y + square][x] == "  ":
                        piece_moves.append((y + square, x))
                    elif board[y + square][x] in take_general:
                        piece_moves.append((y + square, x))
                        dead_end_s = True
                    if board[y + square][x] not in take_general and board[y + square][x] != "  ":
                        dead_end_s = True
                if x - square >= 0 and not dead_end_w:
                    if board[y][x - square] == "  ":
                        piece_moves.append((y, x - square))
                    elif board[y][x - square] in take_general:
                        piece_moves.append((y, x - square))
                        dead_end_w = True
                    if board[y][x - square] not in take_general and board[y][x - square] != "  ":
                        dead_end_w = True
                if x + square <= 7 and not dead_end_e:
                    if board[y][x + square] == "  ":
                        piece_moves.append((y, x + square))
                    elif board[y][x + square] in take_general:
                        piece_moves.append((y, x + square))
                        dead_end_e = True
                    if board[y][x + square] not in take_general and board[y][x + square] != "  ":
                        dead_end_e = True

        # movement rules for bishops
        if self.type == "wb" or self.type == "bb":
            dead_end_nw = False
            dead_end_sw = False
            dead_end_se = False
            dead_end_ne = False
            for cord in range(1, 9):
                if y - cord >= 0 and x - cord >= 0 and not dead_end_nw:
                    if board[y - cord][x - cord] == "  ":
                        piece_moves.append((y - cord, x - cord))
                    elif board[y - cord][x - cord] in take_general:
                        piece_moves.append((y - cord, x - cord))
                        dead_end_nw = True
                    if board[y - cord][x - cord] not in take_general and board[y - cord][x - cord] != "  ":
                        dead_end_nw = True
                if y + cord <= 7 and x - cord >= 0 and not dead_end_sw:
                    if board[y + cord][x - cord] == "  ":
                        piece_moves.append((y + cord, x - cord))
                    elif board[y + cord][x - cord] in take_general:
                        piece_moves.append((y + cord, x - cord))
                        dead_end_sw = True
                    if board[y + cord][x - cord] not in take_general and board[y + cord][x - cord] != "  ":
                        dead_end_sw = True
                if y + cord <= 7 and x + cord <= 7 and not dead_end_se:
                    if board[y + cord][x + cord] == "  ":
                        piece_moves.append((y + cord, x + cord))
                    elif board[y + cord][x + cord] in take_general:
                        piece_moves.append((y + cord, x + cord))
                        dead_end_se = True
                    if board[y + cord][x + cord] not in take_general and board[y + cord][x + cord] != "  ":
                        dead_end_se = True
                if y - cord >= 0 and x + cord <= 7 and not dead_end_ne:
                    if board[y - cord][x + cord] == "  ":
                        piece_moves.append((y - cord, x + cord))
                    elif board[y - cord][x + cord] in take_general:
                        piece_moves.append((y - cord, x + cord))
                        dead_end_ne = True
                    if board[y - cord][x + cord] not in take_general and board[y - cord][x + cord] != "  ":
                        dead_end_ne = True

        # movement rules for queens
        if self.type == "wq" or self.type == "bq":
            dead_end_n = False
            dead_end_s = False
            dead_end_w = False
            dead_end_e = False
            dead_end_nw = False
            dead_end_sw = False
            dead_end_se = False
            dead_end_ne = False
            for cord in range(1, 9):
                if y - cord >= 0 and x - cord >= 0 and not dead_end_nw:
                    if board[y - cord][x - cord] == "  ":
                        piece_moves.append((y - cord, x - cord))
                    elif board[y - cord][x - cord] in take_general:
                        piece_moves.append((y - cord, x - cord))
                        dead_end_nw = True
                    if board[y - cord][x - cord] not in take_general and board[y - cord][x - cord] != "  ":
                        dead_end_nw = True
                if y + cord <= 7 and x - cord >= 0 and not dead_end_sw:
                    if board[y + cord][x - cord] == "  ":
                        piece_moves.append((y + cord, x - cord))
                    elif board[y + cord][x - cord] in take_general:
                        piece_moves.append((y + cord, x - cord))
                        dead_end_sw = True
                    if board[y + cord][x - cord] not in take_general and board[y + cord][x - cord] != "  ":
                        dead_end_sw = True
                if y + cord <= 7 and x + cord <= 7 and not dead_end_se:
                    if board[y + cord][x + cord] == "  ":
                        piece_moves.append((y + cord, x + cord))
                    elif board[y + cord][x + cord] in take_general:
                        piece_moves.append((y + cord, x + cord))
                        dead_end_se = True
                    if board[y + cord][x + cord] not in take_general and board[y + cord][x + cord] != "  ":
                        dead_end_se = True
                if y - cord >= 0 and x + cord <= 7 and not dead_end_ne:
                    if board[y - cord][x + cord] == "  ":
                        piece_moves.append((y - cord, x + cord))
                    elif board[y - cord][x + cord] in take_general:
                        piece_moves.append((y - cord, x + cord))
                        dead_end_ne = True
                    if board[y - cord][x + cord] not in take_general and board[y - cord][x + cord] != "  ":
                        dead_end_ne = True
                if y - cord >= 0 and not dead_end_n:
                    if board[y - cord][x] == "  ":
                        piece_moves.append((y - cord, x))
                    elif board[y - cord][x] in take_general:
                        piece_moves.append((y - cord, x))
                        dead_end_n = True
                    if board[y - cord][x] not in take_general and board[y - cord][x] != "  ":
                        dead_end_n = True
                if y + cord <= 7 and not dead_end_s:
                    if board[y + cord][x] == "  ":
                        piece_moves.append((y + cord, x))
                    elif board[y + cord][x] in take_general:
                        piece_moves.append((y + cord, x))
                        dead_end_s = True
                    if board[y + cord][x] not in take_general and board[y + cord][x] != "  ":
                        dead_end_s = True
                if x - cord >= 0 and not dead_end_w:
                    if board[y][x - cord] == "  ":
                        piece_moves.append((y, x - cord))
                    elif board[y][x - cord] in take_general:
                        piece_moves.append((y, x - cord))
                        dead_end_w = True
                    if board[y][x - cord] not in take_general and board[y][x - cord] != "  ":
                        dead_end_w = True
                if x + cord <= 7 and not dead_end_e:
                    if board[y][x + cord] == "  ":
                        piece_moves.append((y, x + cord))
                    elif board[y][x + cord] in take_general:
                        piece_moves.append((y, x + cord))
                        dead_end_e = True
                    if board[y][x + cord] not in take_general and board[y][x + cord] != "  ":
                        dead_end_e = True

        # returns a list of moves a piece can make
        return piece_moves


# pieces are defined in dictionary with piece type as the key
pieces = {"wp": Piece("wp", 1), "wr": Piece("wr", 5), "wb": Piece("wb", 3),
          "wq": Piece("wq", 9), "wk": Piece("wk", 11), "wn": Piece("wn", 3),
          "bp": Piece("bp", 1), "br": Piece("br", 5), "bb": Piece("bb", 3),
          "bq": Piece("bq", 9), "bk": Piece("bk", 11), "bn": Piece("bn", 3)
          }

en_passant = [[], []]  # list of locations of pawns that can be captured en passant
castle = [[(7, 0), (7, 4), (7, 7)], [(0, 0), (0, 4), (0, 7)]]


class Move:
    # Define moves based on piece type, start location and destination
    def __init__(self, piece_type, start_pos, destination):
        self.piece = piece_type
        self.start_pos = start_pos
        self.destination = destination


def possible_moves_initial(test_turn, test_board):
    # generates all the legal moves on the board and returns as list
    moves = []
    real_test_board = copy.deepcopy(test_board)
    for cord in range(len(real_test_board)):
        for j in range(len(real_test_board[cord])):
            if real_test_board[cord][j][0] == test_turn:
                local_piece = real_test_board[cord][j]
                position = (cord, j)
                for k in pieces[local_piece].movement(cord, j):
                    moves.append(Move(local_piece, position, k))
    return moves


def special_moves(test_turn, test_board):
    # list of moves with special rules legal on given turn
    special = []
    # determines if any en passant moves are available
    if test_turn == "w":
        for square in range(len(test_board[3])):
            if test_board[3][square] == "wp":
                if square - 1 >= 0:
                    if (3, square - 1) in en_passant[0]:
                        special.append(Move("wp", (3, square), (2, square - 1)))
                if square + 1 <= 7:
                    if (3, square + 1) in en_passant[0]:
                        special.append(Move("wp", (3, square), (2, square + 1)))
    if test_turn == "b":
        for square in range(len(test_board[4])):
            if test_board[4][square] == "bp":
                if square - 1 >= 0:
                    if (4, square - 1) in en_passant[1]:
                        special.append(Move("bp", (4, square), (5, square - 1)))
                if square + 1 <= 7:
                    if (4, square + 1) in en_passant[1]:
                        special.append(Move("bp", (4, square), (5, square + 1)))
    # determines if any castle moves are available
    if not check:
        safe_castle = True
        if turn == "w":
            if (7, 4) in castle[0]:
                if (7, 0) in castle[0]:
                    if test_board[7][1] == "  " and test_board[7][2] == "  " and test_board[7][3] == "  ":
                        for castle_square in range(1, 4):
                            for j in possible_moves_initial("b", test_board):
                                if (7, castle_square) == j.destination:
                                    safe_castle = False
                        if safe_castle:
                            special.append(Move("wk", (7, 4), (7, 2)))
                safe_castle = True
                if (7, 7) in castle[0]:
                    if test_board[7][5] == "  " and test_board[7][6] == "  ":
                        for castle_square in range(5, 7):
                            for j in possible_moves_initial("b", test_board):
                                if (7, castle_square) == j.destination:
                                    safe_castle = False
                        if safe_castle:
                            special.append(Move("wk", (7, 4), (7, 6)))
        if turn == "b":
            if (0, 4) in castle[1]:
                if (0, 0) in castle[1]:
                    if test_board[0][1] == "  " and test_board[0][2] == "  " and test_board[0][3] == "  ":
                        for castle_square in range(1, 4):
                            for j in possible_moves_initial("w", test_board):
                                if (0, castle_square) == j.destination:
                                    safe_castle = False
                        if safe_castle:
                            special.append(Move("bk", (0, 4), (0, 2)))
                safe_castle = True
                if (0, 7) in castle[1]:
                    if test_board[0][5] == "  " and test_board[0][6] == "  ":
                        for castle_square in range(5, 7):
                            for j in possible_moves_initial("w", test_board):
                                if (0, castle_square) == j.destination:
                                    safe_castle = False
                        if safe_castle:
                            special.append(Move("bk", (0, 4), (0, 6)))
    # returns a list of moves to be added to normal moves
    return special


def checking(check_turn, a_board):
    # looks at end of turn for check on other player
    king_pos = (8, 8)
    check_board = []
    if check_turn == "w":
        # finds opponent king on board
        for cord in range(len(a_board)):
            for j in range(len(a_board[cord])):
                if a_board[cord][j] == "bk":
                    king_pos = (cord, j)
                    check_board = copy.deepcopy(a_board)

        # move is check if destination is kings position
        for move in possible_moves_initial("w", check_board):
            if move.destination == king_pos:
                return True
        return False
    if check_turn == "b":
        for cord in range(len(a_board)):
            for j in range(len(a_board[cord])):
                if a_board[cord][j] == "wk":
                    king_pos = (cord, j)
                    check_board = copy.deepcopy(a_board)
        for move in possible_moves_initial("b", check_board):
            if move.destination == king_pos:
                return True
        return False


def edit_board(board_1, move, promotion="q"):
    temp_board = board_1.copy()
    # starting position of moved piece will always become empty
    temp_board[move.start_pos[0]][move.start_pos[1]] = "  "
    # pawns have special cases for en passant and promotion
    if move.piece == "wp":
        if move.destination[1] != move.start_pos[1]:
            if temp_board[move.destination[0]][move.destination[1]] == "  ":
                temp_board[move.destination[0] + 1][move.destination[1]] = "  "
        if move.destination[0] == 0:
            temp_board[move.destination[0]][move.destination[1]] = "w" + promotion
    if move.piece == "bp":
        if move.destination[1] != move.start_pos[1]:
            if temp_board[move.destination[0]][move.destination[1]] == "  ":
                temp_board[move.destination[0] - 1][move.destination[1]] = "  "
        if move.destination[0] == 7:
            temp_board[move.destination[0]][move.destination[1]] = "b" + promotion
    # kings have special cases for castling
    if move.piece == "wk":
        if move.destination[1] - move.start_pos[1] == 2:
            temp_board[move.destination[0]][move.destination[1] + 1] = "  "
            temp_board[move.destination[0]][move.destination[1] - 1] = "wr"
        if move.destination[1] - move.start_pos[1] == -2:
            temp_board[move.destination[0]][move.destination[1] - 2] = "  "
            temp_board[move.destination[0]][move.destination[1] + 1] = "wr"
    if move.piece == "bk":
        if move.destination[1] - move.start_pos[1] == 2:
            temp_board[move.destination[0]][move.destination[1] + 1] = "  "
            temp_board[move.destination[0]][move.destination[1] - 1] = "br"
        if move.destination[1] - move.start_pos[1] == -2:
            temp_board[move.destination[0]][move.destination[1] - 2] = "  "
            temp_board[move.destination[0]][move.destination[1] + 1] = "br"
    # destination always contains the piece that moved there
    temp_board[move.destination[0]][move.destination[1]] = move.piece
    # return new board state
    return temp_board


def legal_moves(move_list, current_turn, board_2):
    """
    This function returns a new move list based on whether moves cause
    the players own king to be in check, which is illegal
    """
    new_move_list = []
    if current_turn == "w":
        for move in move_list:
            current_board = copy.deepcopy(board_2)
            test_board = copy.deepcopy(edit_board(current_board, move))
            if not checking("b", test_board):
                new_move_list.append(move)
    if current_turn == "b":
        for move in move_list:
            current_board = copy.deepcopy(board_2)
            test_board = copy.deepcopy(edit_board(current_board, move))
            if not checking("w", test_board):
                new_move_list.append(move)
    return new_move_list


def end_game(board_3, this_turn):
    # looks at end of turn for draw or win

    next_turn = ""
    if this_turn == "w":
        next_turn = "b"
    if this_turn == "b":
        next_turn = "w"
    # cases where next player has no moves
    if len(legal_moves(possible_moves_initial(next_turn, board_3) + special_moves(next_turn, board_3), next_turn,
                       board_3)) == 0:
        # checkmate if no moves and in check
        if check and this_turn == "w":
            for row in board_3:
                print(row)
                print("  ")
            print("Checkmate! White wins!")
            return 1
        if check and this_turn == "b":
            for row in board_3:
                print(row)
                print("  ")
            print("Checkmate! Black wins!")
            return 1
        # stalemate in no moves and not in check
        if not check:
            for row in board_3:
                print(row)
                print("  ")
            print("Stalemate. The game is a draw.")
            return 1
    # draw if there has been 50 moves with no capture or pawn move (not implemented)
    if non_progress_counter == 50:
        for row in board_3:
            print(row)
            print("  ")
        print("50 move rule. The game is a draw.")
        return 1
    return 0


def en_passant_edit(move):
    # adds en passant list if a pawn was moved up 2 squares
    if move.piece == "wp" and move.destination[0] == 4 and move.start_pos[0] == 6:
        en_passant[1].append(move.destination)
    if move.piece == "bp" and move.destination[0] == 3 and move.start_pos[0] == 1:
        en_passant[0].append(move.destination)


def castle_edit(move):
    # removes possible castles if king or rook move
    if move.piece == "wr" and move.start_pos == (7, 0):
        if (7, 0) in castle[0]:
            castle[0].remove((7, 0))
    if move.piece == "wr" and move.start_pos == (7, 7):
        if (7, 7) in castle[0]:
            castle[0].remove((7, 7))
    if move.piece == "br" and move.start_pos == (0, 0):
        if (0, 0) in castle[1]:
            castle[1].remove((0, 0))
    if move.piece == "br" and move.start_pos == (0, 7):
        if (0, 7) in castle[1]:
            castle[1].remove((0, 7))
    if move.piece == "wk" and move.start_pos == (7, 4):
        if (7, 4) in castle[0]:
            castle[0].remove((7, 4))
    if move.piece == "bk" and move.start_pos == (0, 4):
        if (0, 4) in castle[1]:
            castle[1].remove((0, 4))


if __name__ == "__main__":
    # white starts
    turn = "w"
    player = ""
    game_status = 0
    # main game loop
    while game_status == 0:
        # each turn starts with a print of the current board
        for i in range(len(board)):
            print(board[i], " " + str(i))
            print("  ")
        print("  0     1     2     3     4     5     6     7")
        # player string is determined for prompting user
        if turn == "w":
            player = "white"
        if turn == "b":
            player = "black"
            # move is set to illegal for while loop
        legal_move = False
        # prompts for user to enter move details
        move_piece = input(player + " select piece type to move(ex: wp): ")
        y_1, x_1 = input("What is the position of this piece?(ex: y x): ").split()
        y_1, x_1 = int(y_1), int(x_1)
        y_2, x_2 = input("Where do you want to move it?(ex: y x): ").split()
        y_2, x_2 = int(y_2), int(x_2)
        # determine if move is in list of legal moves
        candidate_move = Move(move_piece, (y_1, x_1), (y_2, x_2))
        b_board = copy.deepcopy(board)
        for i in legal_moves(possible_moves_initial(turn, b_board) + special_moves(turn, b_board), turn, b_board):
            if move_piece == i.piece and (y_1, x_1) == i.start_pos and (y_2, x_2) == i.destination:
                legal_move = True
        # if move is not legal enter while loop until legal move is received
        while not legal_move:
            print("This is not a legal move.")
            move_piece = input(player + " select piece type to move(ex: wp): ")
            y_1, x_1 = input("What is the position of this piece?(ex: y x): ").split()
            y_1, x_1 = int(y_1), int(x_1)
            y_2, x_2 = input("Where do you want to move it?(ex: y x): ").split()
            y_2, x_2 = int(y_2), int(x_2)
            candidate_move = Move(move_piece, (y_1, x_1), (y_2, x_2))
            for i in legal_moves(possible_moves_initial(turn, b_board) + special_moves(turn, b_board), turn, b_board):
                if move_piece == i.piece and (y_1, x_1) == i.start_pos and (y_2, x_2) == i.destination:
                    legal_move = True
        # updates en passant and castle status based on move made
        en_passant_edit(candidate_move)
        castle_edit(candidate_move)
        # update board and check for checks
        board = edit_board(board, candidate_move)
        check = checking(turn, board)
        # make a deep copy of the board to check for checkmates
        c_board = copy.deepcopy(board)
        game_status = end_game(c_board, turn)
        # swap turns and clear possible en passant
        if turn == "w":
            turn = "b"
            en_passant[1] = []
        elif turn == "b":
            turn = "w"
            en_passant[0] = []
