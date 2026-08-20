import chess.pgn
from .engine import board_eval, best_move, get_engine

def parse_pgn(file):
    game = chess.pgn.read_game(file)
    board = game.board()
    game_data = {
        "White": game.headers["White"], 
        "Black": game.headers["Black"], 
        "Result": game.headers["Result"], 
        "Moves" : [] 
    }

    engine = get_engine()
    
    for move in game.mainline_moves():
        evalBefore = board_eval(engine, board)
        bestMove = best_move(engine, board)
        san = board.san(move)
        uci = move.uci()
        move_num = board.fullmove_number
        color = "WHITE" if board.turn == chess.WHITE else "BLACK"

        board.push(move)
        evalAfter = board_eval(engine, board)

        #evalLoss represents how much worse a player's position becomes
        if color == "WHITE":
            evalLoss = evalBefore - evalAfter
        else:
            evalLoss = evalAfter - evalBefore

        #0 evalLoss if the position improves
        evalLoss = max(0, evalLoss)

        move_data = {
            "San": san, 
            "Uci": uci, 
            "Move": move_num, 
            "Color": color, 
            "EvalBefore": evalBefore, 
            "EvalAfter": evalAfter, 
            "BestMove": bestMove, 
            "EvalLoss": evalLoss
        }
        game_data["Moves"].append(move_data)

        
    engine.quit()

    return game_data







