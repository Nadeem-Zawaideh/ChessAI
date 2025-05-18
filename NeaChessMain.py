import pygame as p
import NeaChessEngine, NeaChessAI
import sys
import time
from multiprocessing import Process, Queue

WIDTH_OF_CHESSBOARD = HEIGHT_OF_CHESSBOARD = 512
WIDTH_OF_MOVE_LOG_PANEL = 250
HEIGHT_OF_MOVE_LOG_PANEL = HEIGHT_OF_CHESSBOARD
DIMENSIONS = 8
SIZE_OF_SQAURE = HEIGHT_OF_CHESSBOARD // DIMENSIONS
FPS_LIMIT = 15
IMAGES = {}


def ImageLoad():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SIZE_OF_SQAURE, SIZE_OF_SQAURE)
        )

def Main():
    p.init()
    display = p.display.set_mode((WIDTH_OF_CHESSBOARD + WIDTH_OF_MOVE_LOG_PANEL, HEIGHT_OF_CHESSBOARD))
    clock = p.time.Clock()
    display.fill(p.Color("white"))
    state_of_game = NeaChessEngine.State_of_game()
    available_moves = state_of_game.GetAvailableMoves()
    move_made = False
    ImageLoad()
    playing = True
    selected_square = ()
    player_clicks = []
    game_end = False
    ai_thinking = False
    finding_move_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    def get_yes_no(prompt):
        while True:
            try:
                response = input(prompt).strip().lower()
                if response in ("y", "yes"):
                    return True
                elif response in ("n", "no"):
                    return False
                else:
                    print("Please enter 'y' or 'n'.")
            except Exception as e:
                print(f"Input error: {e}. Try again.")

    player_one_white = get_yes_no("Do you want to be white? Computer will play as white if no is typed (y/n): ")
    if player_one_white:
        with open("Move_log.txt", "a+") as file_object:
            file_object.write("white\n")

    player_one_black = get_yes_no("Do you want to be black? Computer will play as black if no is typed (y/n): ")
    if player_one_black:
        with open("Move_log.txt", "a+") as file_object:
            file_object.write("black\n")

    while playing:
        human_move = (state_of_game.white_next_move and player_one_white) or (not state_of_game.white_next_move and player_one_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_end:
                    location = p.mouse.get_pos() 
                    col = location[0] // SIZE_OF_SQAURE
                    row = location[1] // SIZE_OF_SQAURE
                    if selected_square == (row, col) or col >= 8:
                        selected_square = () 
                        player_clicks = [] 
                    else:
                        selected_square = (row, col)
                        player_clicks.append(selected_square)  
                    if len(player_clicks) == 2 and human_move:  
                        move = NeaChessEngine.Move(player_clicks[0], player_clicks[1], state_of_game.chessboard)
                        for i in range(len(available_moves)):
                            if move == available_moves[i]:
                                state_of_game.MoveMake(available_moves[i])
                                move_made = True
                                selected_square = ()  
                                player_clicks = []
                        if not move_made:
                            player_clicks = [selected_square]

        if not game_end and not human_move:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()
                start_time = time.time()
                finding_move_process = Process(target=NeaChessAI.BestMove_Player, args=(state_of_game, available_moves, return_queue))
                finding_move_process.start()

            if not finding_move_process.is_alive():
                ai_move = return_queue.get()
                elapsed_time = time.time() - start_time
                print(f"AI move took {elapsed_time:.2f} seconds")
                if ai_move is None:
                    ai_move = NeaChessAI.FindRandomMove(available_moves)
                state_of_game.MoveMake(ai_move)
                print(f"AI played: {ai_move}")
                move_made = True
                ai_thinking = False

        if move_made:
            available_moves = state_of_game.GetAvailableMoves()
            move_made = False

        DrawStateOfGame(display, state_of_game, available_moves, selected_square)

        if not game_end:
            DrawMoveLog(display, state_of_game, move_log_font)

        if state_of_game.mate:
            game_end = True
            if state_of_game.white_next_move:
                DrawText(display, "Checkmate Black wins!")
            else:
                DrawText(display, "Checkmate White wins! ")
                
        elif state_of_game.draw:
            game_end = True
            DrawText(display, "Stalemate")

        clock.tick(FPS_LIMIT)
        p.display.flip()

     
def DrawStateOfGame(display, state_of_game, available_moves, selected_square):
    DrawChessBoard(display)
    HiglightingSquares(display, state_of_game, available_moves, selected_square)
    DrawPieces(display, state_of_game.chessboard) 

def DrawChessBoard(display):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = colors[((row + column) % 2)]
            p.draw.rect(display, color, p.Rect(column * SIZE_OF_SQAURE, row * SIZE_OF_SQAURE, SIZE_OF_SQAURE, SIZE_OF_SQAURE))


def HiglightingSquares(display, state_of_game, available_moves, selected_square):
    if (len(state_of_game.move_log)) > 0:
        last_move = state_of_game.move_log[-1]
        s = p.Surface((SIZE_OF_SQAURE, SIZE_OF_SQAURE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        display.blit(s, (last_move.col_end * SIZE_OF_SQAURE, last_move.row_end * SIZE_OF_SQAURE))
    if selected_square != ():
        row, col = selected_square
        if state_of_game.chessboard[row][col][0] == ('w' if state_of_game.white_next_move else 'b'):  
            s = p.Surface((SIZE_OF_SQAURE, SIZE_OF_SQAURE))
            s.set_alpha(100) 
            s.fill(p.Color('blue'))
            display.blit(s, (col * SIZE_OF_SQAURE, row * SIZE_OF_SQAURE))
            s.fill(p.Color('yellow'))
            for move in available_moves:
                if move.row_start == row and move.col_start == col:
                    display.blit(s, (move.col_end * SIZE_OF_SQAURE, move.row_end * SIZE_OF_SQAURE))


def DrawPieces(display, chessboard):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            piece = chessboard[row][column]
            if piece != "--":
                display.blit(IMAGES[piece], p.Rect(column * SIZE_OF_SQAURE, row * SIZE_OF_SQAURE, SIZE_OF_SQAURE, SIZE_OF_SQAURE))

def DrawMoveLog(display, state_of_game, font):
    move_log_rectangle = p.Rect(WIDTH_OF_CHESSBOARD, 0, WIDTH_OF_MOVE_LOG_PANEL, HEIGHT_OF_MOVE_LOG_PANEL)
    p.draw.rect(display, p.Color('black'), move_log_rectangle)
    move_log = state_of_game.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        string_move = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            string_move += str(move_log[i + 1]) + "  "
        move_texts.append(string_move)
        file_object = open('Move_log.txt','a+')
        file_object.write(string_move)
        file_object.close

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rectangle.move(padding, text_y)
        display.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def DrawText(display, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("grey"))
    text_location = p.Rect(0, 0, WIDTH_OF_CHESSBOARD, HEIGHT_OF_CHESSBOARD).move(WIDTH_OF_CHESSBOARD / 2 - text_object.get_width() / 2,
                                                                 HEIGHT_OF_CHESSBOARD / 2 - text_object.get_height() / 2)
    display.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    display.blit(text_object, text_location.move(2, 2))


if __name__ == "__main__":
    Main()