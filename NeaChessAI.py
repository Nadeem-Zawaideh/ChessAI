import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3.3, "N": 3.2, "p": 1}

knight_positional_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.0]]

bishop_positional_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.2, 0.2, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.45, 0.4, 0.4, 0.45, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_positional_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.8, 0.8, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.3, 0.5, 0.5, 0.3, 0.25, 0.25]]

queen_positional_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.45, 0.45, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.55, 0.55, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.55, 0.6, 0.6, 0.55, 0.4, 0.3],
                [0.2, 0.4, 0.5, 0.55, 0.55, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_positional_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.35, 0.4, 0.5, 0.5, 0.4, 0.35, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.25, 0.3, 0.4, 0.4, 0.3, 0.25, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.25, 0.3, 0.35, 0.35, 0.3, 0.25, 0.2]]

piece_positional_scores = {"wN": knight_positional_scores,
                         "bN": knight_positional_scores[::-1],
                         "wB": bishop_positional_scores,
                         "bB": bishop_positional_scores[::-1],
                         "wQ": queen_positional_scores,
                         "bQ": queen_positional_scores[::-1],
                         "wR": rook_positional_scores,
                         "bR": rook_positional_scores[::-1],
                         "wp": pawn_positional_scores,
                         "bp": pawn_positional_scores[::-1]}

MATE = 1000
DRAW = 0
DEPTH = 3

def is_piece_hanging(state_of_game, row, col):
    original_turn = state_of_game.white_next_move
    target_square = (row, col)
    
    state_of_game.white_next_move = not original_turn
    opponent_moves = state_of_game.GetAllAvailableMoves()
    state_of_game.white_next_move = original_turn

    for move in opponent_moves:
        if (move.row_end, move.col_end) == target_square:
            return True
    return False

def is_attacked_by_weaker(state_of_game, row, col, piece_code):
    original_turn = state_of_game.white_next_move
    state_of_game.white_next_move = not original_turn 
    opponent_moves = state_of_game.GetAllAvailableMoves()
    state_of_game.white_next_move = original_turn

    for move in opponent_moves:
        if (move.row_end, move.col_end) == (row, col):
            attacker = move.moved_piece
            if piece_score.get(attacker[1], 0) < piece_score.get(piece_code[1], 0):
                return True
    return False


def Quiescence(state_of_game, alpha, beta, round_multiplier, depth):
    if depth == 0:
        return round_multiplier * ScoreChessBoard(state_of_game)

    stand_pat = round_multiplier * ScoreChessBoard(state_of_game)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    captures = [
        m for m in state_of_game.GetAllAvailableMoves()
        if m.piece_taken != "--" and piece_score.get(m.piece_taken[1], 0) >= 1
    ]

    captures.sort(key=lambda m: piece_score.get(m.piece_taken[1], 0), reverse=True)

    for move in captures:
        state_of_game.MoveMake(move)
        score = -Quiescence(state_of_game, -beta, -alpha, -round_multiplier, depth - 1)

        state_of_game.UndoMove()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    print("Q-depth:", depth)
    return alpha




def BestMove_Player(state_of_game, available_moves, return_queue):
    global next_move
    next_move = None
    FindBestMove(state_of_game, available_moves, DEPTH, -MATE, MATE,
                             1 if state_of_game.white_next_move else -1)
    return_queue.put(next_move)

def FindBestMove(state_of_game, available_moves, depth, alpha, beta, round_multiplier):
    global next_move
    next_move = None
    NegaMaxRoot(state_of_game, available_moves, depth, alpha, beta, round_multiplier)
    print("Chosen move:", next_move)
    return next_move

def NegaMax(state_of_game, depth, alpha, beta, round_multiplier):
    if depth == 0:
        QUIESCENCE_DEPTH = 3
        return Quiescence(state_of_game, alpha, beta, round_multiplier, QUIESCENCE_DEPTH)

    max_score = -MATE
    moves = state_of_game.GetAvailableMoves()

    moves.sort(
        key=lambda m: (
            piece_score.get(m.piece_taken[1], 0) if m.piece_taken != "--" else 0,
            piece_score.get(m.moved_piece[1], 0)
        ),
        reverse=True
    )

    for move in moves:
        state_of_game.MoveMake(move)
        score = -NegaMax(state_of_game, depth - 1, -beta, -alpha, -round_multiplier)
        state_of_game.UndoMove()

        if score > max_score:
            max_score = score
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score

def NegaMaxRoot(state_of_game, available_moves, depth, alpha, beta, round_multiplier):
    global next_move
    max_score = -MATE
    print("DEPTH:", depth)

    available_moves.sort(
        key=lambda m: (
            piece_score.get(m.piece_taken[1], 0) if m.piece_taken != "--" else 0,
            piece_score.get(m.moved_piece[1], 0)
        ),
        reverse=True
    )

    for move in available_moves:
        state_of_game.MoveMake(move)
        score = -NegaMax(state_of_game, depth - 1, -beta, -alpha, -round_multiplier)
        state_of_game.UndoMove()

        if score > max_score:
            max_score = score
            next_move = move
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    print(f"Evaluated move {next_move.getChessNotation()} → Score: {max_score}")
    print(f"Final best move: {next_move}, Score: {max_score}")
    return max_score


def ScoreChessBoard(state_of_game):
    if state_of_game.mate:
        return -MATE if state_of_game.white_next_move else MATE
    if state_of_game.draw:
        return DRAW

    moves = state_of_game.GetAvailableMoves()
    if len(moves) == 0:
        return -MATE if state_of_game.white_next_move else MATE

    score = 0
    for row in range(len(state_of_game.chessboard)):
        for col in range(len(state_of_game.chessboard[row])):
            piece = state_of_game.chessboard[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_positional_scores[piece][row][col]

                base_value = piece_score[piece[1]] + piece_position_score
                bonus = 0

                if piece[1] != "K" and 2 <= row <= 5 and 2 <= col <= 5:
                    bonus += 0.1

                if piece[1] == "K" and (row, col) in [(0, 6), (0, 2), (7, 6), (7, 2)]:
                    bonus += 0.2

                if piece[1] == "K":
                    if row not in (0, 7): 
                        bonus -= 0.3
                    if col in (3, 4):
                        bonus += 0.1

                if is_piece_hanging(state_of_game, row, col) and piece[1] != "K":
                    base_value -= 0.8

                if is_attacked_by_weaker(state_of_game, row, col, piece):
                    base_value -= 0.6

                if piece[0] == "w":
                    score += base_value + bonus
                else:
                    score -= base_value + bonus

    if state_of_game.InCheck():
        if state_of_game.white_next_move:
            score -= 0.5
        else:
            score += 0.5

    state_of_game.white_next_move = not state_of_game.white_next_move
    if state_of_game.InCheck():
        score += 0.3 if state_of_game.white_next_move else -0.3
    state_of_game.white_next_move = not state_of_game.white_next_move

    print("Score:", score) 
    return score



def FindRandomMove(available_moves):
    return random.choice(available_moves)