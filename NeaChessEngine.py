class State_of_game:
    def __init__(self):
        self.chessboard = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.piecemovement = {"B": self.Getbishopsquares, "Q": self.Getqueensquares, "K": self.Getkingsquares,
                              "p": self.Getpawnsquares, "R": self.Getrooksquares, "N": self.Getknightsquares}
        self.possible_enpassant = () 
        self.possible_enpassant_log = [self.possible_enpassant]
        self.present_castling_privilages = CastlePrivilages(True, True, True, True)
        self.castle_privilages_log = [CastlePrivilages(self.present_castling_privilages.wks, self.present_castling_privilages.bks,
                                               self.present_castling_privilages.wqs, self.present_castling_privilages.bqs)]
        self.white_next_move = True
        self.move_log = []
        self.location_of_white_king = (7, 4)
        self.location_of_black_king = (0, 4)
        self.mate = False
        self.draw = False
        self.in_check = False
        self.blocked_move = []
        self.checks = []

    def MoveMake(self, move):
        self.chessboard[move.row_start][move.col_start] = "--"
        self.chessboard[move.row_end][move.col_end] = move.moved_piece
        self.move_log.append(move)  
        self.white_next_move = not self.white_next_move  
        if move.moved_piece == "wK":
            self.location_of_white_king = (move.row_end, move.col_end)
        elif move.moved_piece == "bK":
            self.location_of_black_king = (move.row_end, move.col_end)
        if move.is_promotion_of_pawn:
            self.chessboard[move.row_end][move.col_end] = move.moved_piece[0] + "Q"
        if move.move_is_enpassant:
            self.chessboard[move.row_start][move.col_end] = "--" 
        if move.moved_piece[1] == "p" and abs(move.row_start - move.row_end) == 2:  
            self.possible_enpassant = ((move.row_start + move.row_end) // 2, move.col_start)
        else:
            self.possible_enpassant = ()
        if move.move_is_castle:
            if move.col_end - move.col_start == 2:  
                self.chessboard[move.row_end][move.col_end - 1] = self.chessboard[move.row_end][
                    move.col_end + 1]  
                self.chessboard[move.row_end][move.col_end + 1] = '--'  
            else:  
                self.chessboard[move.row_end][move.col_end + 1] = self.chessboard[move.row_end][
                    move.col_end - 2]  
                self.chessboard[move.row_end][move.col_end - 2] = '--' 

        self.possible_enpassant_log.append(self.possible_enpassant)
        self.UpdateCastlePrivilages(move)
        self.castle_privilages_log.append(CastlePrivilages(self.present_castling_privilages.wks, self.present_castling_privilages.bks,
                                                   self.present_castling_privilages.wqs, self.present_castling_privilages.bqs))

    def UpdateCastlePrivilages(self, move):
        if move.piece_taken == "wR":
            if move.col_end == 0:  
                self.present_castling_privilages.wqs = False
            elif move.col_end == 7:  
                self.present_castling_privilages.wks = False
        elif move.piece_taken == "bR":
            if move.col_end == 0:  
                self.present_castling_privilages.bqs = False
            elif move.col_end == 7: 
                self.present_castling_privilages.bks = False

        if move.moved_piece == 'wK':
            self.present_castling_privilages.wqs = False
            self.present_castling_privilages.wks = False
        elif move.moved_piece == 'bK':
            self.present_castling_privilages.bqs = False
            self.present_castling_privilages.bks = False
        elif move.moved_piece == 'wR':
            if move.row_start == 7:
                if move.col_start == 0: 
                    self.present_castling_privilages.wqs = False
                elif move.col_start == 7:  
                    self.present_castling_privilages.wks = False
        elif move.moved_piece == 'bR':
            if move.row_start == 0:
                if move.col_start == 0:  
                    self.present_castling_privilages.bqs = False
                elif move.col_start == 7:  
                    self.present_castling_privilages.bks = False

    def GetAvailableMoves(self):
        temporary_castle_privilages = CastlePrivilages(self.present_castling_privilages.wks, self.present_castling_privilages.bks,
                                          self.present_castling_privilages.wqs, self.present_castling_privilages.bqs)
        moves = []
        self.in_check, self.blocked_move, self.checks = self.CheckForBlockedmovesAndChecks()

        if self.white_next_move:
            row_king = self.location_of_white_king[0]
            col_king = self.location_of_white_king[1]
        else:
            row_king = self.location_of_black_king[0]
            col_king = self.location_of_black_king[1]
        if self.in_check:
            if len(self.checks) == 1:  
                moves = self.GetAllAvailableMoves()
                check = self.checks[0]
                check_rows = check[0]
                check_columns = check[1]
                checking_piece = self.chessboard[check_rows][check_columns]
                available_squares = []
                if checking_piece[1] == "N":
                    available_squares = [(check_rows, check_columns)]
                else:
                    for i in range(1, 8):
                        Available_square = (row_king + check[2] * i,
                                        col_king + check[3] * i)  
                        available_squares.append(Available_square)
                        if Available_square[0] == check_rows and Available_square[
                            1] == check_columns:  
                            break
                for i in range(len(moves) - 1, -1, -1):  
                    if moves[i].moved_piece[1] != "K":  
                        if not (moves[i].row_end,
                                moves[i].col_end) in available_squares: 
                            moves.remove(moves[i])
            else:  
                self.Getkingsquares(row_king, col_king, moves)
        else:  
            moves = self.GetAllAvailableMoves()
            if self.white_next_move:
                self.GetMoveswhichCastle(self.location_of_white_king[0], self.location_of_white_king[1], moves)
            else:
                self.GetMoveswhichCastle(self.location_of_black_king[0], self.location_of_black_king[1], moves)

        if len(moves) == 0:
            if self.InCheck():
                self.mate = True
            else:
                self.draw = True
        else:
            self.mate = False
            self.draw = False

        self.present_castling_privilages = temporary_castle_privilages
        return moves
    
    def UndoMove(self):
        if not self.move_log:
            return
        move = self.move_log.pop()
        self.chessboard[move.row_start][move.col_start] = move.moved_piece
        self.chessboard[move.row_end][move.col_end] = move.piece_taken
        self.white_next_move = not self.white_next_move

    def InCheck(self):
        if self.white_next_move:
            return self.UnderAttackSquare(self.location_of_white_king[0], self.location_of_white_king[1])
        else:
            return self.UnderAttackSquare(self.location_of_black_king[0], self.location_of_black_king[1])

    def UnderAttackSquare(self, row, col):
        self.white_next_move = not self.white_next_move  
        enemies_moves = self.GetAllAvailableMoves()
        self.white_next_move = not self.white_next_move
        for move in enemies_moves:
            if move.row_end == row and move.col_end == col:  
                return True
        return False

    def GetAllAvailableMoves(self):
        moves = []
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard[row])):
                round = self.chessboard[row][col][0]
                if (round == "w" and self.white_next_move) or (round == "b" and not self.white_next_move):
                    piece = self.chessboard[row][col][1]
                    self.piecemovement[piece](row, col, moves)  
        return moves

    def CheckForBlockedmovesAndChecks(self):
        blockedmoves = []  
        checks = []  
        in_check = False
        if self.white_next_move:
            opposite_color = "b"
            true_color = "w"
            row_start = self.location_of_white_king[0]
            col_start = self.location_of_white_king[1]
        else:
            opposite_color = "w"
            true_color = "b"
            row_start = self.location_of_black_king[0]
            col_start = self.location_of_black_king[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_blockedmove = ()
            for i in range(1, 8):
                row_end = row_start + direction[0] * i
                col_end = col_start + direction[1] * i
                if 0 <= row_end <= 7 and 0 <= col_end <= 7:
                    piece_end = self.chessboard[row_end][col_end]
                    if piece_end[0] == true_color and piece_end[1] != "K":
                        if possible_blockedmove == ():
                            possible_blockedmove = (row_end, col_end, direction[0], direction[1])
                        else:  
                            break
                    elif piece_end[0] == opposite_color:
                        enemy_type = piece_end[1]
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (opposite_color == "w" and 6 <= j <= 7) or (opposite_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_blockedmove == ():  
                                in_check = True
                                checks.append((row_end, col_end, direction[0], direction[1]))
                                break
                            else:  
                                blockedmoves.append(possible_blockedmove)
                                break
                        else:  
                            break
                else:
                    break  
        knight_squares = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_squares:
            row_end = row_start + move[0]
            col_end = col_start + move[1]
            if 0 <= row_end <= 7 and 0 <= col_end <= 7:
                piece_end = self.chessboard[row_end][col_end]
                if piece_end[0] == opposite_color and piece_end[1] == "N":  
                    in_check = True
                    checks.append((row_end, col_end, move[0], move[1]))
        return in_check, blockedmoves, checks

    def Getpawnsquares(self, row, col, moves):
        piece_blocked = False
        blockedmove_direction = ()
        for i in range(len(self.blocked_move) - 1, -1, -1):
            if self.blocked_move[i][0] == row and self.blocked_move[i][1] == col:
                piece_blocked = True
                blockedmove_direction = (self.blocked_move[i][2], self.blocked_move[i][3])
                self.blocked_move.remove(self.blocked_move[i])
                break

        if self.white_next_move:
            amount_moved = -1
            row_start = 6
            opposite_color = "b"
            row_king, col_king = self.location_of_white_king
        else:
            amount_moved = 1
            row_start = 1
            opposite_color = "w"
            row_king, col_king = self.location_of_black_king

        if self.chessboard[row + amount_moved][col] == "--": 
            if not piece_blocked or blockedmove_direction == (amount_moved, 0):
                moves.append(Move((row, col), (row + amount_moved, col), self.chessboard))
                if row == row_start and self.chessboard[row + 2 * amount_moved][col] == "--":
                    moves.append(Move((row, col), (row + 2 * amount_moved, col), self.chessboard))
        if col - 1 >= 0:  
            if not piece_blocked or blockedmove_direction == (amount_moved, -1):
                if self.chessboard[row + amount_moved][col - 1][0] == opposite_color:
                    moves.append(Move((row, col), (row + amount_moved, col - 1), self.chessboard))
                if (row + amount_moved, col - 1) == self.possible_enpassant:
                    piece_attacking = piece_blocking = False
                    if row_king == row:
                        if col_king < col:  
                            inside_possible_range = range(col_king + 1, col - 1)
                            outside_possible_range = range(col + 1, 8)
                        else: 
                            inside_possible_range = range(col_king - 1, col, -1)
                            outside_possible_range = range(col - 2, -1, -1)
                        for i in inside_possible_range:
                            if self.chessboard[row][i] != "--":  
                                piece_blocking = True
                        for i in outside_possible_range:
                            square = self.chessboard[row][i]
                            if square[0] == opposite_color and (square[1] == "R" or square[1] == "Q"):
                                piece_attacking = True
                            elif square != "--":
                                piece_blocking = True
                    if not piece_attacking or piece_blocking:
                        moves.append(Move((row, col), (row + amount_moved, col - 1), self.chessboard, move_is_enpassant=True))
        if col + 1 <= 7:  
            if not piece_blocked or blockedmove_direction == (amount_moved, +1):
                if self.chessboard[row + amount_moved][col + 1][0] == opposite_color:
                    moves.append(Move((row, col), (row + amount_moved, col + 1), self.chessboard))
                if (row + amount_moved, col + 1) == self.possible_enpassant:
                    piece_attacking = piece_blocking = False
                    if row_king == row:
                        if col_king < col:  
                            inside_possible_range = range(col_king + 1, col)
                            outside_possible_range = range(col + 2, 8)
                        else:
                            inside_possible_range = range(col_king - 1, col + 1, -1)
                            outside_possible_range = range(col - 1, -1, -1)
                        for i in inside_possible_range:
                            if self.chessboard[row][i] != "--":
                                piece_blocking = True
                        for i in outside_possible_range:
                            square = self.chessboard[row][i]
                            if square[0] == opposite_color and (square[1] == "R" or square[1] == "Q"):
                                piece_attacking = True
                            elif square != "--":
                                piece_blocking = True
                    if not piece_attacking or piece_blocking:
                        moves.append(Move((row, col), (row + amount_moved, col + 1), self.chessboard, move_is_enpassant=True))

    def Getrooksquares(self, row, col, moves):
        
        piece_blocked = False
        blockedmove_direction = ()
        for i in range(len(self.blocked_move) - 1, -1, -1):
            if self.blocked_move[i][0] == row and self.blocked_move[i][1] == col:
                piece_blocked = True
                blockedmove_direction = (self.blocked_move[i][2], self.blocked_move[i][3])
                if self.chessboard[row][col][
                    1] != "Q":  
                    self.blocked_move.remove(self.blocked_move[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) 
        opposite_color = "b" if self.white_next_move else "w"
        for direction in directions:
            for i in range(1, 8):
                row_end = row + direction[0] * i
                col_end = col + direction[1] * i
                if 0 <= row_end <= 7 and 0 <= col_end <= 7:  
                    if not piece_blocked or blockedmove_direction == direction or blockedmove_direction == (
                            -direction[0], -direction[1]):
                        piece_end = self.chessboard[row_end][col_end]
                        if piece_end == "--":  
                            moves.append(Move((row, col), (row_end, col_end), self.chessboard))
                        elif piece_end[0] == opposite_color:  
                            moves.append(Move((row, col), (row_end, col_end), self.chessboard))
                            break
                        else:  
                            break
                else:  
                    break

    def Getknightsquares(self, row, col, moves):
        piece_blocked = False
        for i in range(len(self.blocked_move) - 1, -1, -1):
            if self.blocked_move[i][0] == row and self.blocked_move[i][1] == col:
                piece_blocked = True
                self.blocked_move.remove(self.blocked_move[i])
                break

        knight_squares = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  
        true_color = "w" if self.white_next_move else "b"
        for move in knight_squares:
            row_end = row + move[0]
            col_end = col + move[1]
            if 0 <= row_end <= 7 and 0 <= col_end <= 7:
                if not piece_blocked:
                    piece_end = self.chessboard[row_end][col_end]
                    if piece_end[0] != true_color:  
                        moves.append(Move((row, col), (row_end, col_end), self.chessboard))

    def Getbishopsquares(self, row, col, moves):
        piece_blocked = False
        blockedmove_direction = ()
        for i in range(len(self.blocked_move) - 1, -1, -1):
            if self.blocked_move[i][0] == row and self.blocked_move[i][1] == col:
                piece_blocked = True
                blockedmove_direction = (self.blocked_move[i][2], self.blocked_move[i][3])
                self.blocked_move.remove(self.blocked_move[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1)) 
        opposite_color = "b" if self.white_next_move else "w"
        for direction in directions:
            for i in range(1, 8):
                row_end = row + direction[0] * i
                col_end = col + direction[1] * i
                if 0 <= row_end <= 7 and 0 <= col_end <= 7: 
                    if not piece_blocked or blockedmove_direction == direction or blockedmove_direction == (
                            -direction[0], -direction[1]):
                        piece_end = self.chessboard[row_end][col_end]
                        if piece_end == "--":  
                            moves.append(Move((row, col), (row_end, col_end), self.chessboard))
                        elif piece_end[0] == opposite_color:  
                            moves.append(Move((row, col), (row_end, col_end), self.chessboard))
                            break
                        else:  
                            break
                else:  
                    break

    def Getqueensquares(self, row, col, moves):
        self.Getbishopsquares(row, col, moves)
        self.Getrooksquares(row, col, moves)

    def Getkingsquares(self, row, col, moves):
        
        moves_in_row = (-1, -1, -1, 0, 0, 1, 1, 1)
        moves_in_col = (-1, 0, 1, -1, 1, -1, 0, 1)
        true_color = "w" if self.white_next_move else "b"
        for i in range(8):
            row_end = row + moves_in_row[i]
            col_end = col + moves_in_col[i]
            if 0 <= row_end <= 7 and 0 <= col_end <= 7:
                piece_end = self.chessboard[row_end][col_end]
                if piece_end[0] != true_color:  
                    if true_color == "w":
                        self.location_of_white_king = (row_end, col_end)
                    else:
                        self.location_of_black_king = (row_end, col_end)
                    in_check, blockedmoves, checks = self.CheckForBlockedmovesAndChecks()
                    if not in_check:
                        moves.append(Move((row, col), (row_end, col_end), self.chessboard))
                    if true_color == "w":
                        self.location_of_white_king = (row, col)
                    else:
                        self.location_of_black_king = (row, col)

    def GetMoveswhichCastle(self, row, col, moves):
        if self.UnderAttackSquare(row, col):
            return
        if (self.white_next_move and self.present_castling_privilages.wks) or (
                not self.white_next_move and self.present_castling_privilages.bks):
            self.GetCastleMovesOnKingside(row, col, moves)
        if (self.white_next_move and self.present_castling_privilages.wqs) or (
                not self.white_next_move and self.present_castling_privilages.bqs):
            self.GetCastleMovesOnQueenside(row, col, moves)

    def GetCastleMovesOnKingside(self, row, col, moves):
        if self.chessboard[row][col + 1] == '--' and self.chessboard[row][col + 2] == '--':
            if not self.UnderAttackSquare(row, col + 1) and not self.UnderAttackSquare(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.chessboard, move_is_castle=True))

    def GetCastleMovesOnQueenside(self, row, col, moves):
        if self.chessboard[row][col - 1] == '--' and self.chessboard[row][col - 2] == '--' and self.chessboard[row][col - 3] == '--':
            if not self.UnderAttackSquare(row, col - 1) and not self.UnderAttackSquare(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.chessboard, move_is_castle=True))


class CastlePrivilages:
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, square_start, square_end, chessboard, move_is_enpassant=False, move_is_castle=False):
        self.row_start = square_start[0]
        self.col_start = square_start[1]
        self.row_end = square_end[0]
        self.col_end = square_end[1]
        self.moved_piece = chessboard[self.row_start][self.col_start]
        self.piece_taken = chessboard[self.row_end][self.col_end]
        self.is_promotion_of_pawn = (self.moved_piece == "wp" and self.row_end == 0) or (
                self.moved_piece == "bp" and self.row_end == 7)
        self.move_is_enpassant = move_is_enpassant
        if self.move_is_enpassant:
            self.piece_taken = "wp" if self.moved_piece == "bp" else "bp"
        self.move_is_castle = move_is_castle

        self.is_capture = self.piece_taken != "--"
        self.IDOfMove = self.row_start * 1000 + self.col_start * 100 + self.row_end * 10 + self.col_end

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.IDOfMove == other.IDOfMove
        return False

    def getChessNotation(self):
        if self.is_promotion_of_pawn:
            return self.getRankFile(self.row_end, self.col_end) + "Q"
        if self.move_is_castle:
            if self.col_end == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.move_is_enpassant:
            return self.getRankFile(self.row_start, self.col_start)[0] + "x" + self.getRankFile(self.row_end,
                                                                                                self.col_end) + " e.p."
        if self.piece_taken != "--":
            if self.moved_piece[1] == "p":
                return self.getRankFile(self.row_start, self.col_start)[0] + "x" + self.getRankFile(self.row_end,
                                                                                                    self.col_end)
            else:
                return self.moved_piece[1] + "x" + self.getRankFile(self.row_end, self.col_end)
        else:
            if self.moved_piece[1] == "p":
                return self.getRankFile(self.row_end, self.col_end)
            else:
                return self.moved_piece[1] + self.getRankFile(self.row_end, self.col_end)

    def getRankFile(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self):
        if self.move_is_castle:
            return "0-0" if self.col_end == 6 else "0-0-0"

        square_end = self.getRankFile(self.row_end, self.col_end)

        if self.moved_piece[1] == "p":
            if self.is_capture:
                return self.cols_to_files[self.col_start] + "x" + square_end
            else:
                return square_end + "Q" if self.is_promotion_of_pawn else square_end

        move_string = self.moved_piece[1]
        if self.is_capture:
            move_string += "x"
        return move_string + square_end