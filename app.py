from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

import chess
import chess.engine
import uuid

app = Flask(__name__)

app.secret_key = "andika_catur"

CORS(app)

# =====================================================
# STOCKFISH
# =====================================================

engine = chess.engine.SimpleEngine.popen_uci(
    "stockfish-windows-x86-64.exe"
)

# =====================================================
# MULTI PLAYER BOARD
# =====================================================

games = {}

# =====================================================
# GET PLAYER BOARD
# =====================================================

def get_player_board():

    # session unik tiap user
    if "player_id" not in session:

        session["player_id"] = str(uuid.uuid4())

    player_id = session["player_id"]

    # buat board baru jika belum ada
    if player_id not in games:

        games[player_id] = chess.Board()

    return games[player_id]

# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    board = get_player_board()

    return render_template("index.html")

# =====================================================
# RESET GAME
# =====================================================

@app.route("/reset")
def reset():

    player_id = session["player_id"]

    games[player_id] = chess.Board()

    return jsonify({
        "success": True
    })

# =====================================================
# GET BOARD STATE
# =====================================================

@app.route("/state")
def state():

    board = get_player_board()

    return jsonify({

        "fen": board.fen(),

        "turn": "white" if board.turn else "black",

        "game_over": board.is_game_over()
    })

# =====================================================
# MOVE
# =====================================================

@app.route("/move", methods=["POST"])
def move():

    board = get_player_board()

    data = request.json

    from_square = data["from"]
    to_square = data["to"]

    move = chess.Move.from_uci(
        from_square + to_square
    )

    # =============================================
    # LEGAL MOVE
    # =============================================

    if move in board.legal_moves:

        board.push(move)

        # =========================================
        # PLAYER CHECKMATE
        # =========================================

        if board.is_checkmate():

            return jsonify({

                "success": True,

                "game_over": True,

                "winner": "PLAYER"
            })

        # =========================================
        # STALEMATE
        # =========================================

        if board.is_stalemate():

            return jsonify({

                "success": True,

                "game_over": True,

                "winner": "DRAW"
            })

        # =========================================
        # AI MOVE
        # =========================================

        depth = int(data.get("depth", 3))

        result = engine.play(

            board,

            chess.engine.Limit(
                depth=depth
            )
        )

        ai_move = result.move

        board.push(ai_move)

        # =========================================
        # AI CHECKMATE
        # =========================================

        if board.is_checkmate():

            return jsonify({

                "success": True,

                "ai_from": ai_move.uci()[0:2],

                "ai_to": ai_move.uci()[2:4],

                "game_over": True,

                "winner": "AI"
            })

        # =========================================
        # AI STALEMATE
        # =========================================

        if board.is_stalemate():

            return jsonify({

                "success": True,

                "ai_from": ai_move.uci()[0:2],

                "ai_to": ai_move.uci()[2:4],

                "game_over": True,

                "winner": "DRAW"
            })

        # =========================================
        # NORMAL MOVE
        # =========================================

        return jsonify({

            "success": True,

            "ai_from": ai_move.uci()[0:2],

            "ai_to": ai_move.uci()[2:4],

            "fen": board.fen(),

            "game_over": False
        })

    # =============================================
    # ILLEGAL
    # =============================================

    return jsonify({

        "success": False
    })

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=False,
        host="0.0.0.0",
        port=5003,
        threaded=True
    )