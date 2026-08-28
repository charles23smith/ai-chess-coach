import os
import chess.engine

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "bin", "stockfish.exe")

def get_engine():
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


def analyze_position(engine, board):
    info = engine.analyse(
        board, 
        chess.engine.Limit(time=0.5)
    )

    score = info["score"].pov(chess.WHITE)

    if score.is_mate():
        mate = score.mate()
    else:
        mate = None

    evaluation = score.score(mate_score =100000)
    continuation = info.get("pv", [])

    if continuation:
        best_move = continuation[0].uci()
    else:
        best_move = None
   

    return evaluation, best_move, mate, continuation