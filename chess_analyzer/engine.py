import os
import chess.engine

ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "bin", "stockfish.exe")

def get_engine():
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


# Returns int in centipawns of evaluation of the position (positive -> white is better)
# Mate is represented by a large number (10000)
def board_eval(engine, board) -> int:
    info = engine.analyse(board, chess.engine.Limit(depth=15))
    score = info["score"].white().score(mate_score=10000)
    
    return score

# Returns str of Stockfish's chosen best move in UCI notation (e.g. "e2e4"), 
# found within the specified time
def best_move(engine, board) -> str:
    result = engine.play(board, chess.engine.Limit(time=0.5))
    
    return result.move.uci()


