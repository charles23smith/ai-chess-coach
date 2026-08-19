import chess.pgn

def parse_pgn(file):
    game = chess.pgn.read_game(file)
    board = game.board()
    game_data = {
        "White": game.headers["White"], 
        "Black": game.headers["Black"], 
        "Result": game.headers["Result"], 
        "Moves" : [] 
    }
    
    for move in game.mainline_moves():
        san = board.san(move)
        uci = move.uci()
        move_num = board.fullmove_number
        color = "WHITE" if board.turn == chess.WHITE else "BLACK"

        move_data = {
            "San": san, 
            "Uci": uci, 
            "Move": move_num, 
            "Color": color
        }

        game_data["Moves"].append(move_data)
        board.push(move)

    return game_data







