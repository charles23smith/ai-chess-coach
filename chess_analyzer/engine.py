import os
import chess.engine

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "bin", "stockfish.exe")

def get_engine():
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


def analyze_position(engine, board):
    info = engine.analyse(
        board, 
        chess.engine.Limit(time=0.1)
    )

    evaluation = info["score"].pov(chess.WHITE).score(mate_score = 100000)
    best_move = info["pv"][0].uci()

    return evaluation, best_move