
import pygame
import chess
import chess.engine
import winsound
import sys
import time

# =====================================================
# INPUT NAMA PEMAIN
# =====================================================

import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

player_name = simpledialog.askstring(
    "Nama Pemain",
    "Masukkan nama pemain :"
)

if not player_name:
    player_name = "Player"
# =====================================================
# KONFIGURASI WINDOW
# =====================================================

BOARD_SIZE = 640
SIDEBAR_WIDTH = 260

WIDTH = BOARD_SIZE + SIDEBAR_WIDTH
HEIGHT = 640

SQ_SIZE = BOARD_SIZE // 8

# =====================================================
# WARNA
# =====================================================

WHITE_TILE = (240, 217, 181)
BROWN_TILE = (181, 136, 99)

WHITE = (255,255,255)
BLACK = (0,0,0)

GREEN = (0,255,0)
RED = (255,0,0)

SIDEBAR = (35,35,35)

# =====================================================
# STOCKFISH
# =====================================================

STOCKFISH_PATH = "stockfish-windows-x86-64.exe"

engine = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_PATH
)

# =====================================================
# PYGAME
# =====================================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Kaprodi PGSD UPI SERANG Chess AI"
)

# =====================================================
# FONT
# =====================================================

piece_font = pygame.font.SysFont(
    "Segoe UI Symbol",
    52
)

small_font = pygame.font.SysFont(
    "arial",
    28
)

big_font = pygame.font.SysFont(
    "arial",
    34
)

winner_font = pygame.font.SysFont(
    "arial",
    44
)

# =====================================================
# CLOCK
# =====================================================

clock = pygame.time.Clock()

last_time = time.time()

last_eval_time = 0

# =====================================================
# CHESS
# =====================================================

board = chess.Board()

selected_square = None

player_clicks = []

# =====================================================
# AI
# =====================================================

ai_depth = 6

# =====================================================
# TIMER
# =====================================================

white_time = 600
black_time = 600

# =====================================================
# EVALUASI
# =====================================================

eval_text = "0"

# =====================================================
# BUTTON
# =====================================================

restart_rect = pygame.Rect(
    690,
    320,
    150,
    55
)

# =====================================================
# UNICODE PIECES
# =====================================================

piece_unicode = {

    "P": "♙",
    "R": "♖",
    "N": "♘",
    "B": "♗",
    "Q": "♕",
    "K": "♔",

    "p": "♟",
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
}

# =====================================================
# DRAW BOARD
# =====================================================

def draw_board():

    for row in range(8):

        for col in range(8):

            color = (
                WHITE_TILE
                if (row + col) % 2 == 0
                else BROWN_TILE
            )

            pygame.draw.rect(

                screen,

                color,

                pygame.Rect(
                    col * SQ_SIZE,
                    row * SQ_SIZE,
                    SQ_SIZE,
                    SQ_SIZE
                )
            )

# =====================================================
# HIGHLIGHT
# =====================================================

def draw_highlight():

    if selected_square is not None:

        row = 7 - chess.square_rank(
            selected_square
        )

        col = chess.square_file(
            selected_square
        )

        s = pygame.Surface(
            (SQ_SIZE, SQ_SIZE)
        )

        s.set_alpha(120)

        s.fill((0,255,0))

        screen.blit(

            s,

            (
                col * SQ_SIZE,
                row * SQ_SIZE
            )
        )

# =====================================================
# LEGAL MOVES
# =====================================================

def draw_legal_moves():

    if selected_square is not None:

        for move in board.legal_moves:

            if move.from_square == selected_square:

                row = 7 - chess.square_rank(
                    move.to_square
                )

                col = chess.square_file(
                    move.to_square
                )

                pygame.draw.circle(

                    screen,

                    GREEN,

                    (
                        col * SQ_SIZE + SQ_SIZE // 2,
                        row * SQ_SIZE + SQ_SIZE // 2
                    ),

                    12
                )

# =====================================================
# DRAW PIECES
# =====================================================

def draw_pieces():

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece:

            row = 7 - chess.square_rank(square)

            col = chess.square_file(square)

            text = piece_unicode[
                piece.symbol()
            ]

            color = (
                WHITE
                if piece.color == chess.WHITE
                else BLACK
            )

            piece_surface = piece_font.render(

                text,

                True,

                color
            )

            screen.blit(

                piece_surface,

                (
                    col * SQ_SIZE + 18,
                    row * SQ_SIZE + 10
                )
            )

# =====================================================
# GET SQUARE
# =====================================================

def get_square(pos):

    x, y = pos

    col = x // SQ_SIZE

    row = y // SQ_SIZE

    return chess.square(
        col,
        7 - row
    )

# =====================================================
# AI MOVE
# =====================================================

def ai_move():

    global black_time

    minimum_think = 2

    start_ai = time.time()

    result = engine.play(

        board,

        chess.engine.Limit(
            depth=ai_depth
        )
    )

    thinking_time = time.time() - start_ai

    while thinking_time < minimum_think:

        draw_board()
        draw_highlight()
        draw_legal_moves()
        draw_pieces()
        draw_sidebar()

        pygame.display.flip()

        thinking_time = time.time() - start_ai

    black_time -= thinking_time

    board.push(result.move)

    winsound.Beep(500,120)

# =====================================================
# DRAW SIDEBAR
# =====================================================

def draw_sidebar():

    pygame.draw.rect(

        screen,

        SIDEBAR,

        pygame.Rect(
            BOARD_SIZE,
            0,
            SIDEBAR_WIDTH,
            HEIGHT
        )
    )

    pygame.draw.line(

        screen,

        WHITE,

        (BOARD_SIZE,0),

        (BOARD_SIZE,HEIGHT),

        3
    )

    # TURN

    if board.turn == chess.WHITE:

        turn_text = "YOUR TURN"

    else:

        turn_text = "AI THINKING"

    turn_surface = big_font.render(

        turn_text,

        True,

        RED
    )

    screen.blit(
        turn_surface,
        (680, 40)
    )

    # EVALUASI

    eval_surface = small_font.render(

        f"Eval : {eval_text}",

        True,

        RED
    )

    screen.blit(
        eval_surface,
        (680, 110)
    )

    # TIMER

    white_surface = small_font.render(

        f"{player_name} : {int(white_time)}",

        True,

        WHITE
    )

    black_surface = small_font.render(

        f"Chess AI : {int(black_time)}",

        True,

        WHITE
    )

    screen.blit(
        white_surface,
        (680, 190)
    )

    screen.blit(
        black_surface,
        (680, 240)
    )

    # BUTTON

    pygame.draw.rect(

        screen,

        (220,220,220),

        restart_rect,

        border_radius=8
    )

    restart_text = small_font.render(

        "RESTART",

        True,

        BLACK
    )

    screen.blit(
        restart_text,
        (705, 335)
    )

# =====================================================
# WINNER SCREEN
# =====================================================

def draw_winner(text):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    overlay.set_alpha(180)

    overlay.fill((0,0,0))

    screen.blit(overlay,(0,0))

    win_surface = winner_font.render(

        text,

        True,

        (255,255,0)
    )

    screen.blit(
        win_surface,
        (180,280)
    )

    pygame.display.flip()

    pygame.time.delay(4000)

# =====================================================
# MAIN LOOP
# =====================================================

running = True

while running:

    current_time = time.time()

    delta = current_time - last_time

    last_time = current_time

    # =================================================
    # TIMER
    # =================================================

    if board.turn == chess.WHITE:

        white_time -= delta

    else:

        black_time -= delta

    white_time = max(0, white_time)

    black_time = max(0, black_time)

    # =================================================
    # EVENTS
    # =================================================

    for event in pygame.event.get():

        # EXIT

        if event.type == pygame.QUIT:

            running = False

        # KEYBOARD

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:

                ai_depth = 2

            if event.key == pygame.K_2:

                ai_depth = 6

            if event.key == pygame.K_3:

                ai_depth = 8

        # MOUSE

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # RESTART

            if restart_rect.collidepoint(mouse_pos):

                board.reset()

                white_time = 600
                black_time = 600

                eval_text = "0"

                selected_square = None

                player_clicks = []

            # PAPAN

            elif mouse_pos[0] < BOARD_SIZE:

                if board.turn == chess.WHITE:

                    square = get_square(
                        mouse_pos
                    )

                    selected_square = square

                    player_clicks.append(
                        square
                    )

                    if len(player_clicks) == 2:

                        move = chess.Move(

                            player_clicks[0],

                            player_clicks[1]
                        )

                        if move in board.legal_moves:

                            board.push(move)

                            winsound.Beep(
                                800,
                                120
                            )

                            if not board.is_game_over():

                                ai_move()

                        player_clicks = []

    # =================================================
    # EVALUASI STOCKFISH
    # =================================================

    if time.time() - last_eval_time > 600:

        info = engine.analyse(

            board,

            chess.engine.Limit(
                depth=3
            )
        )

        score = info["score"].white()

        eval_text = "OFF"

        last_eval_time = time.time()

    # =================================================
    # DRAW
    # =================================================

    screen.fill(BLACK)

    draw_board()

    draw_highlight()

    draw_legal_moves()

    draw_pieces()

    draw_sidebar()

    # =================================================
    # GAME OVER
    # =================================================

    if white_time <= 0:

        draw_winner(
            "CHESS AI MENANG!"
        )

        running = False

    if black_time <= 0:

        draw_winner(
            f"{player_name} MENANG!"
        )

        running = False

    if board.is_checkmate():

        if board.turn == chess.WHITE:

            draw_winner(
                "CHESS AI CHECKMATE!"
            )

        else:

            draw_winner(
                f"{player_name} CHECKMATE!"
            )

        running = False

    pygame.display.flip()

    clock.tick(10)

# =====================================================
# EXIT
# =====================================================

engine.quit()

pygame.quit()

sys.exit()

