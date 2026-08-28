import chess.pgn
from .engine import get_engine, analyze_position
from .classifier import classify_move, calculate_material_loss

def parse_pgn(file):
    game = chess.pgn.read_game(file)
    board = game.board()

    whiteBrilliant = 0
    whiteBest = 0 
    whiteGood = 0 
    whiteInaccuracies = 0
    whiteMistakes = 0 
    whiteBlunders = 0 
    blackBrilliant = 0
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
                    "Brilliant": whiteBrilliant, 
                    "BestCount": whiteBest, 
                    "GoodCount": whiteGood, 
                    "Inaccuracies": whiteInaccuracies, 
                    "Mistakes": whiteMistakes, 
                    "Blunders": whiteBlunders
                },
                "Black": {
                    "Brilliant": blackBrilliant, 
                    "BestCount": blackBest, 
                    "GoodCount": blackGood, 
                    "Inaccuracies": blackInaccuracies, 
                    "Mistakes": blackMistakes, 
                    "Blunders": blackBlunders
                }
        }
    }

    engine = get_engine()
    evalBefore, bestMove, mateBefore, _ = analyze_position(engine, board)
    
    
    for move in game.mainline_moves():
        san = board.san(move)
        uci = move.uci()
        move_num = board.fullmove_number
        color = "WHITE" if board.turn == chess.WHITE else "BLACK"
        bestMove_obj = chess.Move.from_uci(bestMove)
        bestMove_San = board.san(bestMove_obj)

        board.push(move)
        evalAfter, next_best_move, mateAfter, continuation = analyze_position(engine, board)

        #evalLoss represents how much worse a player's position becomes
        if color == "WHITE":
            evalLoss = evalBefore - evalAfter
        else:
            evalLoss = evalAfter - evalBefore

        #0 evalLoss if the position improves
        evalLoss = max(0, evalLoss)
        player_color = chess.WHITE if color == "WHITE" else chess.BLACK
        materialLoss = calculate_material_loss(
            board, 
            player_color, 
            continuation[:4]
        )
        classification = classify_move(
            uci, 
            bestMove, 
            evalLoss, 
            materialLoss, 
            mateBefore, 
            mateAfter
        )

        if color == "WHITE":
            if classification == "Brilliant":
                whiteBrilliant += 1 
            elif classification == "Best":
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
            if classification == "Brilliant":
                whiteBrilliant += 1 
            elif classification == "Best":
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
            "BestMove": bestMove_San, 
            "EvalLoss": evalLoss, 
            "Classification": classification, 
            "Fen": fen, 
            "MateBefore": mateBefore, 
            "MateAfter": mateAfter, 
            "MaterialLoss": materialLoss
        }
        game_data["Moves"].append(move_data)

        evalBefore = evalAfter
        bestMove = next_best_move
        mateBefore = mateAfter

    game_data["Stats"]["White"]["Brilliant"] = whiteBrilliant
    game_data["Stats"]["White"]["BestCount"] = whiteBest
    game_data["Stats"]["White"]["GoodCount"] = whiteGood
    game_data["Stats"]["White"]["Inaccuracies"] = whiteInaccuracies
    game_data["Stats"]["White"]["Mistakes"] = whiteMistakes
    game_data["Stats"]["White"]["Blunders"] = whiteBlunders

    game_data["Stats"]["Black"]["Brilliant"] = blackBrilliant
    game_data["Stats"]["Black"]["BestCount"] = blackBest
    game_data["Stats"]["Black"]["GoodCount"] = blackGood
    game_data["Stats"]["Black"]["Inaccuracies"] = blackInaccuracies
    game_data["Stats"]["Black"]["Mistakes"] = blackMistakes
    game_data["Stats"]["Black"]["Blunders"] = blackBlunders
    

    engine.quit()

    return game_data







