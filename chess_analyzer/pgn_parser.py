import chess.pgn
from .engine import get_engine, analyze_position
from .classifier import classify_move

def parse_pgn(file):
    game = chess.pgn.read_game(file)
    board = game.board()

    whiteBest = 0 
    whiteGood = 0 
    whiteInaccuracies = 0
    whiteMistakes = 0 
    whiteBlunders = 0 
    blackBest = 0
    blackGood = 0
    blackInaccuracies = 0 
    blackMistakes = 0
    blackBlunders = 0

    game_data = {
        "White": game.headers["White"], 
        "Black": game.headers["Black"], 
        "Result": game.headers["Result"], 
        "Moves" : [], 
        "Stats": {
                "White": {
                    "BestCount": whiteBest, 
                    "GoodCount": whiteGood, 
                    "Inaccuracies": whiteInaccuracies, 
                    "Mistakes": whiteMistakes, 
                    "Blunders": whiteBlunders
                },
                "Black": {
                    "BestCount": blackBest, 
                    "GoodCount": blackGood, 
                    "Inaccuracies": blackInaccuracies, 
                    "Mistakes": blackMistakes, 
                    "Blunders": blackBlunders
                }
        }
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

        if color == "WHITE":
            if classification == "Best":
                whiteBest += 1 
            elif classification == "Good":
                whiteGood += 1 
            elif classification == "Inaccuracy":
                whiteInaccuracies += 1 
            elif classification == "Mistake":
                whiteMistakes += 1 
            else:
                whiteBlunders += 1 
        else:
            if classification == "Best":
                blackBest += 1 
            elif classification == "Good":
                blackGood += 1 
            elif classification == "Inaccuracy":
                blackInaccuracies += 1 
            elif classification == "Mistake":
                blackMistakes += 1 
            else:
                blackBlunders += 1 
        
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

    game_data["Stats"]["White"]["BestCount"] = whiteBest
    game_data["Stats"]["White"]["GoodCount"] = whiteGood
    game_data["Stats"]["White"]["Inaccuracies"] = whiteInaccuracies
    game_data["Stats"]["White"]["Mistakes"] = whiteMistakes
    game_data["Stats"]["White"]["Blunders"] = whiteBlunders

    game_data["Stats"]["Black"]["BestCount"] = blackBest
    game_data["Stats"]["Black"]["GoodCount"] = blackGood
    game_data["Stats"]["Black"]["Inaccuracies"] = blackInaccuracies
    game_data["Stats"]["Black"]["Mistakes"] = blackMistakes
    game_data["Stats"]["Black"]["Blunders"] = blackBlunders
    

    engine.quit()

    return game_data







