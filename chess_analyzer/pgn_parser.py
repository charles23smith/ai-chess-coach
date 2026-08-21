import chess.pgn
from .engine import get_engine, analyze_position
from .classifier import classify_move

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
    evalBefore, bestMove = analyze_position(engine, board)
    
    for move in game.mainline_moves():
        san = board.san(move)
        uci = move.uci()
        move_num = board.fullmove_number
        color = "WHITE" if board.turn == chess.WHITE else "BLACK"

        board.push(move)
        evalAfter, next_best_move = analyze_position(engine, board)

        #evalLoss represents how much worse a player's position becomes
        if color == "WHITE":
            evalLoss = evalBefore - evalAfter
        else:
            evalLoss = evalAfter - evalBefore

        #0 evalLoss if the position improves
        evalLoss = max(0, evalLoss)
        classification = classify_move(uci, bestMove, evalLoss)

        #String notation to rebuild the entire board 
        fen = board.fen()


        move_data = {
            "San": san, 
            "Uci": uci, 
            "Move": move_num, 
            "Color": color, 
            "EvalBefore": evalBefore, 
            "EvalAfter": evalAfter, 
            "BestMove": bestMove, 
            "EvalLoss": evalLoss, 
            "Classification": classification, 
            "Fen": fen
        }
        game_data["Moves"].append(move_data)

        evalBefore = evalAfter
        bestMove = next_best_move


    engine.quit()

    return game_data







